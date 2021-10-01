import builtins
import os
import glob
import re
import sys

if len(sys.argv) > 1 and sys.argv[1] == "-x":
    missing_only = True
    sys.argv.pop()
else:
    missing_only = False

orig = os.path.dirname(os.path.abspath(__file__))
os.chdir(orig)
file = open("missing.txt", "w+")

def print(*values, sep=" ", end="\n"):
    out = sep.join(map(str, values)) + end
    file.write(out)
    # if len(values) > 1 and len(sys.argv) > 1:
    #     if not any(values[1].startswith(item) for item in sys.argv[1:]):
    #         return out
    # elif len(sys.argv) > 1:
    #     return out
    sys.stdout.write(out)
    return out

def check_folder(folder, ext):
    os.chdir(folder)
    files = glob.glob("**/*." + ext, recursive=True)
    files = list(filter(lambda x: not x.startswith("examples"), files))

    class_find = re.compile("(?<=^class )(\\w+)(?=(\(.*?\))?:)")
    method_find = re.compile("(?<=    def )(\\w+)")
    func_find = re.compile("(?<=^def )(\\w+)")
    attr_find = re.compile("([a-zA-Z]\w+)(?= ?(?:\: .*?)?= ?)")

    classes = []
    functions = []
    attrs = []

    for file in files:
        if missing_only and ext == "py" and not os.path.isfile(
                os.path.join(orig, "pyunity", file + "i")):
            continue
        with open(file, "r") as f:
            content = f.read().rstrip().splitlines()
        
        module = "pyunity." + os.path.splitext(file)[0].replace(os.path.sep, ".")
        if not any(module.startswith(item) for item in sys.argv[1:]):
            continue
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

def check_classes(a, b, c, d, e, f, name):
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
        print("Class " + name + ":", class_["name"])
        for method in class_["methods"]:
            print("    Method " + name + ":", method)
    print()
    for func in functions:
        print("Function " + name + ":", func)
    print()
    for attr in attrs:
        print("Variable " + name + ":", attr)

check_classes(a, b, c, d, e, f, "missing")
sys.stdout.write("\n\n")
check_classes(d, e, f, a, b, c, "extra")
file.close()
print = builtins.print