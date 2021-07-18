import os
import glob
import re
import sys

orig = os.path.dirname(os.path.abspath(__file__))
os.chdir(orig)
open("missing.txt", "w+").close()

def print(*values, sep=" ", end="\n"):
    out = sep.join(values) + end
    sys.stdout.write(out)
    with open("missing.txt", "a+") as f:
        f.write(out)
    return out

def check_folder(folder, ext):
    os.chdir(folder)
    files = glob.glob("**/*." + ext, recursive=True)
    files = list(filter(lambda x: not x.startswith("examples"), files))

    class_find = re.compile("(?<=^class )(\\w+)(?=(\(.*?\))?:)")
    method_find = re.compile("(?<=    def )(\\w+)")
    func_find = re.compile("(?<=^def )(\\w+)")
    attr_find = re.compile("([a-zA-Z]\w+)(?= ?= ?)")

    classes = []
    functions = []
    attrs = []

    for file in files:
        with open(file, "r") as f:
            content = f.read().rstrip().splitlines()
        
        module = "pyunity." + os.path.splitext(file)[0].replace(os.path.sep, ".")
        module = module.replace(".__init__", "") + "."
        current_class = {}
        for line in content:
            if re.search(class_find, line):
                if current_class != {}:
                    current_class["name"] = current_class["name"]
                    classes.append(current_class)
                current_class = {"name": module + re.search(class_find, line).group(),
                                "methods": []}
            elif re.search(method_find, line):
                current_class["methods"].append(current_class["name"] + \
                    "." + re.search(method_find, line).group())
            elif re.search(func_find, line):
                functions.append(module + re.search(func_find, line).group())
            elif re.match(attr_find, line):
                attrs.append(module + re.match(attr_find, line).group())
        
        if current_class != {}:
            classes.append(current_class)
    os.chdir(orig)
    return classes, functions, attrs

a, b, c = check_folder("../pyunity", "py")
d, e, f = check_folder("pyunity", "pyi")
classes = []
for class_ in a:
    for class2 in d:
        if class2["name"] == class_["name"]:
            break
    else:
        classes.append(class_)
        continue

    if class_["methods"] == []:
        continue
    current = {"name": class_["name"]}
    current["methods"] = [item for item in class_["methods"] if item not in class2["methods"]]
    if current["methods"] == []:
        continue
    classes.append(current)

functions = [item for item in b if item not in e]
attrs = [item for item in c if item not in f]

for class_ in classes:
    print("Class missing: " + class_["name"])
    for method in class_["methods"]:
        print("    Method missing: " + method)
print()
for func in functions:
    print("Function missing: " + func)
print()
for attr in attrs:
    print("Variable missing: " + attr)
