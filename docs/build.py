import subprocess
import sys
import os

subprocess.call(["sphinx-apidoc", "-e", "-f", "-T", "-o",
                "docs/source/api/", "pyunity", "pyunity/config.py", "pyunity/examples/"],
                env={**os.environ, "SPHINX_APIDOC_OPTIONS": "members,inherited-members,show-inheritance"})

with open("docs/source/api/pyunity.rst") as f:
    lines = f.read().splitlines()[:-8]

lines[0] = "API Documentation"
lines[1] = "================="
lines.insert(2, "Information on specific functions, classes, and methods.")
lines.insert(2, "")
for i in range(len(lines)):
    if lines[i].startswith("   pyunity"):
        lines[i] = "   api/" + lines[i][3:]

lines.append("")

with open("docs/source/api.rst", "w") as f:
    f.write("\n".join(lines))

if len(sys.argv) > 1:
    subprocess.call(["sphinx-build", "-b", "html", "-a", "-E", "-v", "docs/source/", "docs/en/"])
