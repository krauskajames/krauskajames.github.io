"""Legal description reader for county tax-roll descriptions (TAXDSCRP).

Reads the metes-and-bounds part of a description written in tax-roll shorthand, e.g.

    PRT SW SE,SEC 20, COM AT NE COR OF SD SW SE,TH S89 DEG 08'58"W 835.44',S28 DEG 53'33"E 478.49',
    N62 DEG 04'46"E 6.55',N28 DEG 13'W 129.48',N80 DEG 15'E 670.59' TH N0 DEG 22'33"W 200.61'TO BEG.

and returns the tie courses (point of commencement -> point of beginning), the boundary courses,
the misclosure, a review table (each call's source text next to what was read) and flags for
anything it was unsure of. Parsing is deterministic: every course can be traced to its text.

Bearings and distances are used as written. In Sheboygan County's tax roll they are grid bearings
in US survey feet (WISCRS Kewaunee, Manitowoc and Sheboygan).

    python3 ldreader.py "COM AT NE COR, TH N89 DEG 41'W 485.6', ... TO BEG."
"""
from __future__ import annotations
import math, re, sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------- normalizing
def normalize(text: str) -> str:
    s = (text or "").upper()
    s = s.replace("’", "'").replace("‘", "'").replace("”", '"').replace("“", '"').replace("′", "'").replace("″", '"')
    s = s.replace("''", '"')
    s = re.sub(r"\s*°\s*", " DEG ", s)
    s = re.sub(r"(?<=\d)\s*\*\s*(?=\d|[EW]\b)", " DEG ", s)
    s = re.sub(r"(?<=\d)-\s+(?=DEG\b)", " ", s)
    s = re.sub(r"\bDEGREES?\b|\bDEG\.", "DEG", s)
    # N-89-DEG-57'- 13"E  ->  N 89 DEG 57' 13"E
    s = re.sub(r"(?<=[NS0-9'])-(?=\s*\d)", " ", s)
    s = re.sub(r"(?<=\d)-(?=DEG)|(?<=DEG)-", " ", s)
    s = re.sub(r"(?<=['\"])\s*-\s*(?=\d|[EW]\b)", " ", s)
    s = re.sub(r"\bTHENCE\b", "TH", s)
    s = re.sub(r"(?<=\d)\.\s(?=\d+\s?')", ".", s)          # 410. 75' -> 410.75'
    s = re.sub(r"(?<=\d)DEG\b", " DEG", s)
    s = re.sub(r"\bFEET\b|\bFT\b\.?", "'", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# ---------------------------------------------------------------- tokens
NUM = r"\d+(?:\.\d+)?"
FRAC = r"(?:\s+1/2|\s+1/4|\s+3/4)?"
BEARING = re.compile(
    rf"\b(?P<ns>[NS])\s?(?P<d>\d{{1,3}}{FRAC})\s?DEG\b"
    rf"(?:\s?(?P<m>\d{{1,2}})(?:\s?'|\s(?=\d)))?"
    rf"(?:\s?(?P<s>\d{{1,2}}(?:\.\d+)?)\s?(?:\"|(?=\s?[EW]\b)))?"
    rf"\s?(?P<ew>[EW])(?![A-Z])")
# Same, without DEG: S89 43 40 W (degree sign already turned into DEG, so this is the rare
# space-separated form) or N0 22'33"W
BEARING2 = re.compile(rf"\b(?P<ns>[NS])\s?(?P<d>\d{{1,3}})\s(?P<m>\d{{1,2}})'\s?(?P<s>\d{{1,2}}(?:\.\d+)?)?\"?\s?(?P<ew>[EW])(?![A-Z])")
CARD = re.compile(r"\b(?P<c>N|S|E|W|NE|NW|SE|SW|NLY|SLY|ELY|WLY|NELY|NWLY|SELY|SWLY|NORTH|SOUTH|EAST|WEST|NORTHERLY|SOUTHERLY|EASTERLY|WESTERLY|NORTHEASTERLY|NORTHWESTERLY|SOUTHEASTERLY|SOUTHWESTERLY)\b(?!\s?(?:1/4|1/2|LINE|LN|COR|R/W|\d/))")
DIST = re.compile(rf"(?P<v>{NUM}(?:\s(?:1/2|1/4|3/4))?)\s?(?P<u>'|RODS?\b|CHAINS?\b|CH\b)")
SEP = re.compile(r",|;|\bTH\b|\bAND TH\b")
POBMARK = re.compile(r"(?:\bTO\s?|\bAND\s|&\s?|\bBEING\s|\bAT\s)(?:THE\s|A\s)?(?:P\.?O\.?B\.?(?![A-Z])|(?:POINT|PNT|PT|PLACE) OF BEG(?:INNING)?\b)|\bTO\s?BEG(?:INNING)?\b|\bTO B\.?$")
END = re.compile(r"\bTO\s?(?:THE\s)?(?:P\.?O\.?B\.?|POB|BEG(?:INNING)?\b|PT OF BEG|POINT OF BEG(?:INNING)?|PLACE OF BEG(?:INNING)?)|\bTO B\.?$")
START = re.compile(r"\b(COM|COMM|COMMENCING|BEG|BEGINNING|BEG AT)\b")
CURVE = re.compile(r"\bCURVE|\bARC\b|\bRADIUS|\bCHORD|\bCHD\b")

DUE = {"N": 0, "E": 90, "S": 180, "W": 270, "NORTH": 0, "EAST": 90, "SOUTH": 180, "WEST": 270}
VAGUE = {"NE": 45, "SE": 135, "SW": 225, "NW": 315, "NLY": 0, "ELY": 90, "SLY": 180, "WLY": 270,
         "NELY": 45, "SELY": 135, "SWLY": 225, "NWLY": 315, "NORTHERLY": 0, "EASTERLY": 90, "SOUTHERLY": 180,
         "WESTERLY": 270, "NORTHEASTERLY": 45, "SOUTHEASTERLY": 135, "SOUTHWESTERLY": 225, "NORTHWESTERLY": 315}
UNIT_FT = {"'": 1.0, "ROD": 16.5, "RODS": 16.5, "CHAIN": 66.0, "CHAINS": 66.0, "CH": 66.0}

def _deg(txt):
    txt = txt.strip(); f = 0.0
    for fr, v in ((" 1/2", .5), (" 1/4", .25), (" 3/4", .75)):
        if txt.endswith(fr): txt, f = txt[: -len(fr)], v
    return float(txt) + f

@dataclass
class Course:
    text: str                    # the source text of this call
    azimuth: float | None = None # degrees clockwise from grid north
    bearing: str = ""            # quadrant bearing as read, N 89-08-58 E style
    dist: float | None = None    # US survey feet
    kind: str = "line"           # line | curve | tie
    confidence: str = "ok"       # ok | vague | missing
    note: str = ""

    def dxdy(self):
        a = math.radians(self.azimuth); return self.dist * math.sin(a), self.dist * math.cos(a)

@dataclass
class Result:
    source: str
    ties: list = field(default_factory=list)
    courses: list = field(default_factory=list)
    flags: list = field(default_factory=list)
    status: str = ""             # parsed | no_bearings | partial
    misclose: float | None = None
    misclose_dir: float | None = None
    perimeter: float | None = None
    area_sqft: float | None = None

    @property
    def precision(self):
        if self.misclose is None or not self.perimeter: return None
        return math.inf if self.misclose < 1e-6 else self.perimeter / self.misclose

    def coords(self, x0=0.0, y0=0.0, include_ties=False):
        pts = [(x0, y0)]; x, y = x0, y0
        for c in (self.ties if include_ties else []) + self.courses:
            dx, dy = c.dxdy(); x += dx; y += dy; pts.append((x, y))
        return pts

def _bearing(m):
    ns, ew = m["ns"], m["ew"]
    d = _deg(m["d"]); mi = float(m["m"] or 0); se = float(m["s"] or 0)
    ang = d + mi / 60 + se / 3600
    if ang > 90.0001 or mi >= 60 or se >= 60: return None, None
    az = {("N", "E"): ang, ("S", "E"): 180 - ang, ("S", "W"): 180 + ang, ("N", "W"): 360 - ang}[(ns, ew)] % 360
    txt = f"{ns} {m['d'].strip()}-{int(mi):02d}-{se:05.2f} {ew}".replace(".00 ", " ")
    return az, txt

def _scan(seg: str):
    """Yield (pos, kind, payload, text) tokens in order."""
    toks = []; taken = []
    def free(a, b): return all(b <= x or a >= y for x, y in taken)
    for rx in (BEARING, BEARING2):
        for m in rx.finditer(seg):
            if not free(*m.span()): continue
            az, txt = _bearing(m)
            if az is None: continue
            toks.append((m.start(), "BRG", (az, txt), m.group(0))); taken.append(m.span())
    for m in DIST.finditer(seg):
        if not free(*m.span()): continue
        u = m["u"].rstrip("S") if m["u"] != "'" else "'"
        toks.append((m.start(), "DIST", _deg(m["v"]) * UNIT_FT.get(u, UNIT_FT.get(m["u"], 1.0)), m.group(0))); taken.append(m.span())
    for m in CARD.finditer(seg):
        if not free(*m.span()): continue
        c = m["c"]
        before = seg[max(0, m.start() - 6): m.start()]
        after = seg[m.end(): m.end() + 8]
        # a letter that names a road, a line or a side is not a direction: CTH N, R/W, TO E LN, OF W 1/2
        on_line = re.match(r"\s(?:ON|ALG|ALONG)\b", after)
        if re.search(r"[A-Z]'$", before) or not on_line and re.search(r"(?:/|\bTO |\bOF |\bON |\bIN |\bAT |\bSD |\bCTH ?\"?|\bSTH ?\"?|\bHWY ?|\bUSH ?|\bLOT |\bBLK |\bST |\bAVE |\bRD |\bLN |\bTHE |\bMOST |\bALG )$", before) \
                or re.match(r"\s?(?:LN|LINE|LI\b|R/W|COR|BANK|SIDE|END|HALF|PRT|PART|BDRY|BOUNDARY|SHORE|[0-9]/|\"|&\s?[NSEW]\b)", after):
            continue
        # aliquot parts (SW SW, NE NE, SW1/4) are places, not directions
        if c in ("NE", "NW", "SE", "SW") and (re.match(r"\s?(?:NE|NW|SE|SW)\b", after) or re.search(r"\b(?:NE|NW|SE|SW|LINE|LN|OF|SD|IN|PRT)\s?$", before)):
            continue
        toks.append((m.start(), "CARD", c, c)); taken.append(m.span())
    for m in re.finditer(r"(?<![0-9])\.(?=\s?(?:[NS]\s?-?\d|[NSEW]\s?\d|(?:N|S|E|W|NE|NW|SE|SW)(?:LY)?\s))", seg):
        if free(*m.span()): toks.append((m.start(), "SEP", None, "."))
    for m in SEP.finditer(seg):
        if free(*m.span()): toks.append((m.start(), "SEP", None, m.group(0)))
    for m in re.finditer(r"\bFROM\b|\bOF\b", seg):
        if free(*m.span()): toks.append((m.start(), "REF", m.group(0), m.group(0)))
    for m in re.finditer(r"\bTO\b", seg):
        if free(*m.span()): toks.append((m.start(), "TO", None, "TO"))
    for m in re.finditer(r"&|\bAND\b", seg):
        if free(*m.span()): toks.append((m.start(), "AMP", None, m.group(0)))
    return sorted(toks)

def _courses(seg: str, flags: list, tie=False):
    """Turn a run of calls into Course objects. A new course starts at a separator, or at a
    direction that follows a direction+distance already read (descriptions often drop commas)."""
    out = []; cur = {"az": None, "brg": "", "dist": None, "conf": "ok", "a": None, "b": None, "dir_after_dist": False}
    def flush(end):
        if cur["a"] is None: return
        text = seg[cur["a"]:end].strip(" ,;")
        if cur["az"] is None and cur["dist"] is None:
            if not tie and re.search(r"\b(?:ALG|ALONG|DOWNSTREAM|UPSTREAM|MEANDERS?|FOLLOWING)\b", text):
                out.append(Course(text, confidence="missing", note="follows a line or bank with no direction or distance"))
        elif CURVE.search(text) and not tie:
            out.append(_curve(text, flags))
        else:
            c = Course(text, cur["az"], cur["brg"], cur["dist"], "tie" if tie else "line", cur["conf"])
            if c.azimuth is None: c.confidence = "missing"; c.note = "no direction"
            elif c.dist is None: c.confidence = "missing"; c.note = "no distance (runs to a line or corner by reference)"
            out.append(c)
        cur.update(az=None, brg="", dist=None, conf="ok", a=None, b=None)
    toks = _scan(seg); skip = False
    for i, (pos, k, val, txt) in enumerate(toks):
        if k == "TO":
            # words after TO name a target (TO A PNT 5' FROM SHORE...), not a new call
            if cur["a"] is not None and not CURVE.search(seg[cur["a"]:pos]): skip = True
            continue
        if skip and k == "CARD" and cur["az"] is not None and cur["dist"] is not None and re.match(r"\s(?:ON|ALG|ALONG)\b", seg[pos + len(txt): pos + len(txt) + 7]):
            flush(pos); skip = False
        if skip and k == "BRG" and cur["az"] is not None and cur["dist"] is not None \
                and not re.search(r"\b(?:FROM|OF)\b", re.split(r"[,;]|\bTH\b", seg[pos:])[0]):
            flush(pos); skip = False
        if skip and k != "SEP": continue
        if k == "SEP":
            skip = False
            ahead = re.split(r"[,;]|\bTH\b", seg[pos + len(txt):])[0]
            if not tie and re.match(r"\s?(?:UPSTREAM|DOWNSTREAM|MEANDERING|FOLLOWING|ALG|ALONG)\b", ahead):
                flush(pos)
                out.append(Course(ahead.strip(" ,;"), confidence="missing", note="follows a line, bank or creek with no direction or distance"))
                skip = True
                continue
            # a comma inside a curve call ("...RADIUS OF 131', THE CHORD...") does not end it
            nxt = seg[pos:pos + 60]
            if cur["a"] is not None and CURVE.search(seg[cur["a"]:pos] + nxt[:40]) and re.match(r",\s?(THE\s)?(CHORD|CHD|RADIUS|ARC|LONG CHORD|DELTA|CENTRAL)", nxt):
                continue
            flush(pos)
            # a call made only of words: "DOWNSTREAM ALG SD RIGHT BANK TO E LINE OF SEC"
            nxt_tok = next((t for t in toks[i + 1:] if t[1] not in ("TO", "REF", "AMP")), None)
            piece = seg[pos + len(txt): nxt_tok[0] if nxt_tok else len(seg)]
            if not tie and nxt_tok and nxt_tok[1] == "SEP" and re.search(r"\b(?:ALG|ALONG|DOWNSTREAM|UPSTREAM|MEANDERS?)\b", piece):
                out.append(Course(piece.strip(" ,;"), confidence="missing", note="follows a line or bank with no direction or distance"))
            continue
        if k in ("BRG", "CARD"):
            if cur["az"] is not None and cur["dist"] is not None and not (cur["a"] is not None and CURVE.search(seg[cur["a"]:pos])):
                flush(pos)
            if cur["az"] is None:
                if cur["a"] is None: cur["a"] = pos
                if k == "BRG": cur["az"], cur["brg"] = val
                elif val in DUE: cur["az"], cur["brg"] = DUE[val], {"NORTH": "N", "EAST": "E", "SOUTH": "S", "WEST": "W"}.get(val, val)
                else: cur["az"], cur["brg"], cur["conf"] = VAGUE[val], val, "vague"
            elif cur["a"] is not None and CURVE.search(seg[cur["a"]:pos]) and k == "BRG":
                pass  # chord bearing inside a curve call; _curve reads it
        elif k == "DIST":
            if cur["a"] is None: cur["a"] = pos
            if cur["dist"] is None: cur["dist"] = val
            elif cur["az"] is not None and not CURVE.search(seg[cur["a"]:pos]):
                flush(pos); cur["a"] = pos; cur["dist"] = val
    flush(len(seg))
    return out

def _curve(text, flags):
    c = Course(text, kind="curve")
    chord = re.search(r"CHORD[^0-9NS]{0,40}?(?:BEARS|BEARING|OF)?\s?(?P<b>[NS].{0,30}?[EW])(?![A-Z])[ ,]{0,3}(?P<d>" + NUM + r")\s?'", text) \
        or re.search(r"CHORD[^0-9]{0,40}?(?P<d>" + NUM + r")\s?'[^NS]{0,30}(?P<b>[NS].{0,30}?[EW])(?![A-Z])", text)
    if chord:
        m = BEARING.search(chord["b"] + " ") or BEARING2.search(chord["b"] + " ")
        if m:
            c.azimuth, c.bearing = _bearing(m); c.dist = float(chord["d"])
            c.note = "curve: closure uses the chord"
            r = re.search(r"RADIUS (?:OF )?(" + NUM + r")", text)
            if r: c.note += f" (radius {float(r[1]):,.2f} ft)"
            return c
    c.confidence = "missing"; c.note = "curve without a readable chord bearing and length"
    return c

# ---------------------------------------------------------------- main entry
RECORD = re.compile(r"\((?:REC(?:D|ORDED)?|R|DEED|PER DEED)\.?\b[^)]*\)|\([^)]{0,40}\b(?:DEED|RECD?|RECORD)\)")

def parse(text: str) -> Result:
    src = normalize(text); R = Result(src)
    src = re.sub(r",?\s?(?:SD|SAID) (?:PNT|POINT|PT) (?:ALSO )?BEING [^,;]*", "", src)
    if RECORD.search(src):
        src = RECORD.sub(" ", src); R.flags.append("record values in parentheses set aside; measured values used")
    has_brg = bool(BEARING.search(src) or BEARING2.search(src) or re.search(r"\b[NSEW]\s?" + NUM + r"\s?'|" + NUM + r"\s?'\s?[NSEW]\b", src))
    st = START.search(src)
    if not st or not has_brg:
        R.status = "no_bearings"; return R
    head = src[: st.start()]
    if re.search(r"\b(?:FOLL|FOLLOWING) (?:DESC|DESCRIBED) (?:LN|LINE)\b|\bDESC LN\b", src):
        R.status = "line"; R.flags.append("describes a dividing line, not a parcel outline"); return R
    if re.search(r"\bLOTS?\b.{0,80}?(?:&|\bAND\b)\s?(?:ALSO\s)?(?:PRT|PART|ALL|UNPLATTED|THAT|THOSE)\b|\bAND UNPLATTED\b|\bADJ(?:ACENT|OINING)?\b", head):
        R.flags.append("lot plus a described piece: the courses cover only part of the parcel")
    if re.search(r"(?:&|\bAND\b|\bALSO\b)\s?(?:ALSO\s)?(?:THAT PRT[^,]*)?$", head.strip(" ,;")) and re.search(r"\b(?:SEC|LOT|CSM|THE [NSEW] \d)", head):
        R.flags.append("a whole aliquot part or lot plus a described piece: the courses cover only part of the parcel")
    if re.search(r"\bEXC(EPT)?\b", head):
        R.flags.append("exception: the courses describe land taken OUT of the parcel")
    # Find the end ("TO BEG"). A "POINT OF BEG" that is followed by more calls is a mid-text point of
    # beginning: what comes before it is the tie from the point of commencement.
    pob_mid = None; end = None
    for mk in POBMARK.finditer(src, st.end()):
        after = src[mk.end(): mk.end() + 60]
        if re.match(r"\.?\s?(?:OF (?:THIS|THE) (?:DESC\w*|PARCEL)[A-Z ]{0,25}|HEREIN DESC\w*|OF PARCEL TO BE DESC\w*)?\.?\s?[,;.]{0,2}\s?(?:TH\b|THENCE\b)", after) and DIST.search(after):
            pob_mid = pob_mid or mk
            continue
        end = mk; break
    if not end:
        R.flags.append("no 'TO BEG' found; read to the end of the text")
        seg_end = len(src)
    else:
        seg_end = end.start()
        if end.group(0).rstrip(".").endswith("TO B"): R.flags.append("description is cut off in the tax roll")
    tail = src[end.end():] if end else ""
    if re.search(r"\b(COM|BEG)\b.*\bTH\b", tail) or re.search(r"&\s?(ALSO\s)?(INCL|EXC)|\bALSO (INCL|EXC)", tail):
        R.flags.append("more than one tract: only the first is read")
    elif re.search(r"\bEXC(EPT)?\b", tail):
        R.flags.append("land excepted after the description: the mapped parcel should be smaller")
    elif re.search(r"\bINCL(UDING)?\b|\bALSO\b", tail):
        R.flags.append("land added after the description: the mapped parcel may be larger")
    seg = src[st.end(): seg_end]
    # point of commencement -> point of beginning
    word = st.group(1)
    if word.startswith("BEG"):
        body = seg
    elif pob_mid:
        k = pob_mid.start() - st.end()
        tie_txt, body = seg[:k], seg[pob_mid.end() - st.end():]
        R.ties = [t for t in _courses(re.sub(r"\bTH\b", ",", tie_txt), R.flags, tie=True) if t.dist is not None]
        for t in R.ties:
            if t.confidence != "ok": R.flags.append(f"tie call unclear: {t.text!r}")
        body = re.sub(r"^[\s,;.]*(?:OF (?:THIS|THE) (?:DESC\w*|PARCEL)[A-Z ]{0,25}?(?=[.,; ]*TH\b)|HEREIN DESC\w*|OF PARCEL TO BE DESC\w*)?[\s,;.]*", "", body)
        body = re.sub(r"^\s?(?:TH|THENCE)\b", "", body)
    else:
        m = re.search(r"\bTH\b", seg)
        if not m: R.status = "partial"; R.flags.append("no 'TH' after the point of commencement"); return R
        tie_txt, body = seg[: m.start()], seg[m.end():]
        # some descriptions skip the TH ("COM 231.25'E OF SW COR SD1/4,E 50.5',N 107.5',...,TH S 204'"),
        # or name the line first ("COM ON THE N LINE OF ..., S89 DEG 44'E 420.50' OF THE NW COR, TH ...").
        # The tie ends at the first comma-chunk with a distance followed by FROM/OF.
        pos = 0
        for chunk in re.split(r"(?<=[,;])", tie_txt):
            dm = DIST.search(chunk)
            if dm and re.search(r"\b(FROM|OF)\b", chunk[dm.end():]):
                cut = pos + len(chunk)
                rest = tie_txt[cut:]
                if DIST.search(rest):
                    tie_txt, body = tie_txt[:cut].rstrip(",;"), rest + ", " + body
                break
            pos += len(chunk)
        # "COM AT <corner>" has no tie; "COM <dir> <dist> FROM <corner>" or "COM <dist> <dir> OF <corner>" does
        if DIST.search(tie_txt):
            R.ties = _courses(tie_txt, R.flags, tie=True)
        R.ties = [t for t in R.ties if t.dist is not None or t.azimuth is not None]
        for t in R.ties:
            if t.confidence != "ok": R.flags.append(f"tie call unclear: {t.text!r}")
        body = re.sub(r"^\s?CONT\b", "", body.strip())
    R.courses = _courses(body, R.flags)
    if not R.courses:
        R.status = "partial"; R.flags.append("no boundary courses read"); return R
    bad = [c for c in R.courses if c.confidence == "missing"]
    vague = [c for c in R.courses if c.confidence == "vague"]
    if vague: R.flags.append(f"{len(vague)} course(s) with only a general direction (e.g. NELY)")
    if bad:
        R.status = "partial"
        last_ok = bad == [R.courses[-1]] and R.courses[-1].azimuth is not None
        R.flags.append("last course runs 'to the beginning' with no distance, so it closes by definition" if last_ok
                       else f"{len(bad)} course(s) without a direction or distance")
        if last_ok:
            # closing course by reference: use the remaining vector, but it proves nothing about closure
            pts = [(0.0, 0.0)]; xx = yy = 0.0
            for c in R.courses[:-1]:
                dx, dy = c.dxdy(); xx += dx; yy += dy; pts.append((xx, yy))
            c = R.courses[-1]; c.dist = math.hypot(xx, yy)
            gap_az = math.degrees(math.atan2(-xx, -yy)) % 360
            turn = abs((gap_az - c.azimuth + 180) % 360 - 180)
            c.note += f"; length taken from the gap ({c.dist:,.2f} ft, {turn:.1f}° off the stated direction)"
            c._by_ref = True
        else:
            return R
    else:
        R.status = "parsed"
    def _mis(cs):
        x = sum(c.dxdy()[0] for c in cs); y = sum(c.dxdy()[1] for c in cs); return math.hypot(x, y), sum(c.dist for c in cs)
    if R.status == "parsed" and not R.ties and len(R.courses) >= 5:
        m0, p0 = _mis(R.courses)
        if m0 > 1 and p0 / m0 < 5000:
            for k in (1, 2):
                mk, pk = _mis(R.courses[k:])
                if mk <= 1 or pk / mk >= 5000 or mk < 0.1 * m0 and m0 > 50:
                    R.ties = R.courses[:k]
                    for t in R.ties: t.kind = "tie"; t.note = "treated as the tie: the text does not mark the point of beginning"
                    R.courses = R.courses[k:]
                    R.flags.append(f"first {k} call(s) treated as the tie: the text does not mark the point of beginning, and without them the misclosure drops from {m0:,.2f} ft to {mk:,.2f} ft")
                    break
    # courses that end back at the point of commencement: the tie line is also the last side
    if R.status == "parsed" and R.ties and all(t.dist is not None and t.azimuth is not None for t in R.ties):
        m0, _ = _mis(R.courses)
        tx = sum(t.dxdy()[0] for t in R.ties); ty = sum(t.dxdy()[1] for t in R.ties)
        ex = sum(c.dxdy()[0] for c in R.courses); ey = sum(c.dxdy()[1] for c in R.courses)
        if m0 > 1 and len(R.ties) == 1 and math.hypot(ex + tx, ey + ty) <= max(1.0, 0.0002 * m0):
            t = R.ties[0]
            R.courses.append(Course(t.text, t.azimuth, t.bearing, t.dist, "line", "ok",
                                    "the tie line again: the courses end at the point of commencement"))
            R.flags.append("the courses end at the point of commencement, so the tie line closes the parcel")
    pts = R.coords()
    dx, dy = pts[-1][0] - pts[0][0], pts[-1][1] - pts[0][1]
    R.misclose = math.hypot(dx, dy); R.perimeter = sum(c.dist for c in R.courses)
    R.misclose_dir = math.degrees(math.atan2(dx, dy)) % 360
    ring = pts[:-1] + [pts[0]]
    R.area_sqft = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:]))) / 2
    if R.status == "partial" and getattr(R.courses[-1], "_by_ref", False): R.misclose = None
    return R

# ---------------------------------------------------------------- outputs
def _qb(az):
    az %= 360
    if az <= 90: ns, ew, a = "N", "E", az
    elif az <= 180: ns, ew, a = "S", "E", 180 - az
    elif az <= 270: ns, ew, a = "S", "W", az - 180
    else: ns, ew, a = "N", "W", 360 - az
    d = int(a); m = int((a - d) * 60); s = round(((a - d) * 60 - m) * 60, 2)
    if s >= 60: s -= 60; m += 1
    if m >= 60: m -= 60; d += 1
    return f"{ns}{d}-{m}-{s:g}{ew}"

def traverse_file(R: Result, sp_x: float, sp_y: float, include_ties=True) -> str:
    """ArcMap-format traverse file, loadable in ArcGIS Pro's Traverse pane (Load traverse).
    SP is the point of commencement when ties are included, otherwise the point of beginning."""
    lines = ["DT QB", "DU DMS", f"SP {sp_x:.3f} {sp_y:.3f}"]
    for c in (R.ties if include_ties else []) + R.courses:
        lines.append(f"DD {_qb(c.azimuth)} {c.dist:.2f}")
    return "\r\n".join(lines) + "\r\n"

def review(R: Result):
    rows = []
    for i, c in enumerate(R.ties, 1):
        rows.append({"n": f"T{i}", "role": "tie (POC to POB)", "source": c.text, "read_as": f"{c.bearing} {c.dist:,.2f} ft" if c.dist else c.bearing, "check": c.confidence, "note": c.note})
    for i, c in enumerate(R.courses, 1):
        rd = f"{c.bearing} {c.dist:,.2f} ft" if c.dist is not None and c.bearing else (c.bearing or "?")
        rows.append({"n": str(i), "role": c.kind, "source": c.text, "read_as": rd, "check": c.confidence, "note": c.note})
    return rows

def summary(R: Result) -> str:
    out = [f"status: {R.status}"]
    for r in review(R): out.append(f"  {r['n']:>3} {r['role']:<16} {r['read_as']:<28} {r['check']:<7} <- {r['source']}" + (f"   [{r['note']}]" if r["note"] else ""))
    if R.misclose is not None:
        p = R.precision
        out.append(f"misclose {R.misclose:.2f} ft toward azimuth {R.misclose_dir:.0f}, precision " + ("exact" if p == math.inf else f"1:{p:,.0f}") + f", perimeter {R.perimeter:,.2f} ft, area {R.area_sqft / 43560:.2f} ac")
    for f in R.flags: out.append(f"flag: {f}")
    return "\n".join(out)

if __name__ == "__main__":
    print(summary(parse(" ".join(sys.argv[1:]) or sys.stdin.read())))
