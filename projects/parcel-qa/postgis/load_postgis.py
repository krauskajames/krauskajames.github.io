"""Load the county layers into PostGIS and run every QA check as SQL.

    python load_postgis.py ../config/sheboygan.json
    python load_postgis.py ../config/sheboygan.json --compare ../out/qa_summary.csv

Downloads the layers first if the GeoPackages named in the config's "inputs" are missing. Connects to
localhost:5432 as postgres (set PGHOST / PGPORT / PGUSER / PGPASSWORD to change; it asks for the
password if PGPASSWORD is not set), creates the database parcel_qa if needed, writes the raw layers to
schema src, then runs sql/01_schema.sql, 02_core.sql, the check files and 20_report.sql.
Needs: geopandas, sqlalchemy, psycopg2, geoalchemy2.
"""
import argparse, csv, getpass, json, os, subprocess, sys, time
import geopandas as gpd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

HERE = os.path.dirname(os.path.abspath(__file__))
SQL = ["01_schema.sql", "02_core.sql", "10_parcel_checks.sql", "11_road_checks.sql", "12_address_checks.sql", "20_report.sql"]
KEEP = {   # raw columns each layer needs (lowercased); everything else is left out of the database
    "parcels": ["parcelid", "siteaddress", "muni", "ownernme1"],
    "addresses": ["siteaddid", "addrnum", "fullname", "fulladdr", "unitid", "parcelid", "rdclid", "municipality", "esn", "msag", "status"],
    "roads": ["centerlineid", "fromleft", "toleft", "fromright", "toright", "fullname", "munileft", "roadclass", "rdstatus"],
    "municipalities": ["name", "munitype"],
}


def engine(db):
    pw = os.environ.get("PGPASSWORD") or getpass.getpass("postgres password: ")
    os.environ["PGPASSWORD"] = pw
    url = URL.create("postgresql+psycopg2", username=os.environ.get("PGUSER", "postgres"), password=pw,
                     host=os.environ.get("PGHOST", "localhost"), port=int(os.environ.get("PGPORT", 5432)), database=db)
    return create_engine(url)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--db", default="parcel_qa")
    ap.add_argument("--skip-load", action="store_true", help="reuse the src.* tables already in the database")
    ap.add_argument("--compare", help="qa_summary.csv from the Python run, to print the counts side by side")
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    base = os.path.dirname(os.path.abspath(a.config))
    paths = {k: os.path.join(base, v.partition("::")[0]) for k, v in cfg["inputs"].items() if k in KEEP}

    missing = [k for k, p in paths.items() if not os.path.exists(p)]
    if missing:
        raw = os.path.dirname(paths[missing[0]])
        print(f"Downloading {', '.join(missing)} into {raw} (a few minutes)...", flush=True)
        sub = {"sources": {k: cfg["sources"][k] for k in missing}}
        tmp = os.path.join(HERE, "_sources.json")
        json.dump(sub, open(tmp, "w"))
        subprocess.run([sys.executable, os.path.join(HERE, "..", "fetch_arcgis.py"), tmp, raw], check=True)
        os.remove(tmp)

    eng0 = engine("postgres")
    with eng0.connect().execution_options(isolation_level="AUTOCOMMIT") as c:
        if not c.execute(text("SELECT 1 FROM pg_database WHERE datname = :d"), {"d": a.db}).scalar():
            c.execute(text(f'CREATE DATABASE "{a.db}"'))
            print(f"Created database {a.db}")
    eng = engine(a.db)
    with eng.begin() as c:
        c.execute(text("CREATE EXTENSION IF NOT EXISTS postgis; CREATE SCHEMA IF NOT EXISTS src;"))

    for k, p in ({} if a.skip_load else paths).items():
        t = time.time()
        g = gpd.read_file(p).to_crs(3071)
        g.columns = [c.lower() for c in g.columns]
        g = g[[c for c in KEEP[k] if c in g.columns] + ["geometry"]].rename_geometry("geom")
        for c in KEEP[k]:
            if c in g.columns and g[c].dtype != object and not str(g[c].dtype).startswith("string"):
                continue
            if c in g.columns:
                g[c] = g[c].astype("string")
        g.insert(0, "src_oid", range(len(g)))
        g.to_postgis(k, eng, schema="src", if_exists="replace", index=False, chunksize=5000)
        print(f"src.{k}: {len(g):,} rows ({time.time() - t:.0f} s)", flush=True)

    for f in SQL:
        t = time.time()
        raw = eng.raw_connection()          # plain psycopg2 cursor: SQL files contain % (modulo), no parameters
        try:
            with raw.cursor() as cur:
                cur.execute(open(os.path.join(HERE, "sql", f), encoding="utf-8").read())
            raw.commit()
        finally:
            raw.close()
        print(f"{f}: {time.time() - t:.0f} s", flush=True)

    with eng.connect() as c:
        rows = c.execute(text("SELECT check_code, title, count, checked FROM qa.summary")).all()
    py = {}
    if a.compare:
        py = {r["check"]: int(r["count"]) for r in csv.DictReader(open(a.compare))}
    print(f"\n{'check':6}{'title':30}{'SQL':>7}" + (f"{'Python':>8}  match" if py else ""))
    for code, title, n, _ in rows:
        line = f"{code:6}{title:30}{n:>7}"
        if py:
            p = py.get(code, 0)
            line += f"{p:>8}  {'yes' if p == n else 'NO'}"
        print(line)
    print(f"{'total':36}{sum(r[2] for r in rows):>7}" + (f"{sum(py.values()):>8}" if py else ""))


if __name__ == "__main__":
    main()
