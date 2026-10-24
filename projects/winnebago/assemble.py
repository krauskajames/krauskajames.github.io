"""Build winnebago.html from the shared site head (pollinator.html lines 1-780: fonts, tokens, Leaflet CSS) + page_body.html."""
import re, sys
root = sys.argv[1] if len(sys.argv) > 1 else "../.."
src = open(f"{root}/pollinator.html", encoding="utf-8").read()
head = src[: src.index("<body>") + len("<body>")]
head = re.sub(r"<title>.*?</title>", "<title>Winnebago County Community Profile – James Krauska</title>", head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="An interactive demographic and economic profile of Winnebago County, Wisconsin: population change by municipality, projections, age structure, economic base, commuting and housing.">', head)
body = open(f"{root}/projects/winnebago/page_body.html", encoding="utf-8").read()
open(f"{root}/winnebago.html", "w", encoding="utf-8").write(head + "\n" + body)
print("ok")
