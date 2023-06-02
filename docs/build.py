import subprocess
import sys
import os
import shutil

if os.path.isdir("docs/source/api"):
    shutil.rmtree("docs/source/api")

providers = []
for folder in os.listdir("pyunity/window/providers"):
    path = os.path.join("pyunity/window/providers", folder)
    if os.path.isdir(path):
        providers.append(path)

result = subprocess.call(["sphinx-apidoc", "-e", "-f", "-T", "-o",
                "docs/source/api/", "pyunity", "pyunity/config.py", "pyunity/examples/", *providers],
                env={**os.environ, "SPHINX_APIDOC_OPTIONS": "members,undoc-members,show-inheritance"})

if result != 0:
    exit(result)

with open("docs/source/api/pyunity.rst") as f:
    lines = f.read().splitlines()[:-8]

lines[0] = "API Documentation"
lines[1] = "================="
lines.insert(2, "")
lines.insert(3, "Information on specific functions, classes, and methods in")
lines.insert(4, "the PyUnity project.")
lines.insert(0, "=================")
for i in range(len(lines)):
    if lines[i].startswith("   pyunity"):
        lines[i] = "   api/" + lines[i][3:]

lines.append("")
lines.append("Module contents")
lines.append("---------------")
lines.append("")
lines.append(".. automodule:: pyunity")
lines.append("")

with open("docs/source/api.rst", "w") as f:
    f.write("\n".join(lines))

if len(sys.argv) > 1:
    result = subprocess.call(["sphinx-build", "-b", "html", "-a", "-E", "-v", "docs/source/", "docs/en/"])
    if result != 0:
        exit(result)
    os.system("start docs/index.html")
    exit(result)
