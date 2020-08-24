import pyunity

desc = pyunity.__doc__.split("\n")
desc_new = [
    "# PyUnity", "",
    "[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)]" + \
        "(https://pyunity.readthedocs.io/en/latest/?badge=latest)"
]
skip = 0
for i in range(len(desc)):
    if skip: skip = 0; continue
    if i != len(desc) - 1 and len(set(desc[i + 1])) == 1:
        if desc[i + 1][0] == "-":
            desc_new.append("### " + desc[i])
            skip = 1
        elif desc[i + 1][0] == "=":
            desc_new.append("## " + desc[i])
            skip = 1
    else:
        if "create a new pull request" in desc[i]:
            desc[i] = desc[i].replace(
                "create a new pull request",
                "[create a new pull request)[https://github.com/rayzchen/pyunity/pulls]"
            )
        desc_new.append(desc[i])

with open("README.md", "w") as f:
    for line in desc_new:
        f.write(line + "\n")