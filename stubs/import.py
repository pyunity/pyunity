import os
import glob
import shutil

orig = os.path.dirname(os.path.abspath(__file__))
os.chdir(orig)

if os.path.isdir("copied"):
    shutil.rmtree("copied")

for file in glob.glob("pyunity/**/*.pyi", recursive=True):
    new = os.path.join("copied", file[:-1])
    os.makedirs(os.path.dirname(new), exist_ok=True)
    print(new)
    shutil.copy(file, new)
    with open(new) as f:
        content = f.read()

    if content.startswith('"""'):
        newContent = content.replace('"""\n\n','"""\n\nfrom __future__ import annotations\n\n')
    else:
        newContent = "from __future__ import annotations\n\n" + content

    with open(new, "w") as f:
        f.write(newContent)
