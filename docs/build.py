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

command = [
    "sphinx-apidoc",
    "-e",
    "-f",
    "-T",
    "-o",
    "docs/source/api/",
    "pyunity",
    "pyunity/config.py",
    "pyunity/examples/",
    *providers
]
apidocOpts = ",".join(["members", "undoc-members", "show-inheritance"])
result = subprocess.call(command, env={**os.environ, "SPHINX_APIDOC_OPTIONS": apidocOpts})

if result != 0:
    exit(result)

with open("docs/source/api/pyunity.rst") as f:
    lines = f.read().splitlines()[:-8]

lines[0] = "================="
lines[1] = "API Documentation"
lines.insert(2, "=================")
lines.insert(3, "")
lines.insert(4, "Information on specific functions, classes, and methods in")
lines.insert(5, "the PyUnity project.")
for i in range(len(lines)):
    if lines[i].startswith("   pyunity"):
        lines[i] = "   api/" + lines[i].lstrip()

lines.append("")
lines.append("Module contents")
lines.append("---------------")
lines.append("")
lines.append(".. automodule:: pyunity")
lines.append("")

with open("docs/source/api.rst", "w") as f:
    f.write("\n".join(lines))

if len(sys.argv) > 1:
    command = [
        "sphinx-build",
        "-b",
        "html",
        "-a",
        "-E",
        "-v",
        "docs/source/",
        "docs/en/"
    ]
    result = subprocess.call(command)
    if result != 0:
        exit(result)
    os.system("start docs/index.html")
    exit(result)
