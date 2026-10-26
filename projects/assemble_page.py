"""Build a case-study page from the shared site head (pollinator.html: fonts, tokens, Leaflet CSS) + a body file.
Usage: python3 assemble_page.py BODY.html OUT.html "Title" "Description" """
import re, sys
body, out, title, desc = sys.argv[1:5]
src = open("pollinator.html", encoding="utf-8").read()
head = src[: src.index("<body>") + len("<body>")]
head = re.sub(r"<title>.*?</title>", f"<title>{title} – James Krauska</title>", head)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head)
open(out, "w", encoding="utf-8").write(head + "\n" + open(body, encoding="utf-8").read())
print("ok", out)
