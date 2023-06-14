import builtins
import os
import glob
import re
import sys

if len(sys.argv) > 1 and sys.argv[1] == "-x":
    missingOnly = True
    sys.argv.pop()
else:
    missingOnly = False

orig = os.path.dirname(os.path.abspath(__file__))
os.chdir(orig)
file = open("missing.txt", "w+")

def print(*values, sep=" ", end="\n"):
    out = sep.join(map(str, values)) + end
    file.write(out)
    sys.stdout.write(out)
    return out

def checkFolder(folder, ext):
    os.chdir(folder)
    files = glob.glob("**/*." + ext, recursive=True)
    files = [x for x in files if not x.startswith("examples") and not x.endswith("Window.py")]

    classFind = re.compile("(?<=^class )(\\w+)(?=(\(.*?\))?:)")
    methodFind = re.compile("(?<=    def )(\\w+)")
    funcFind = re.compile("(?<=^def )(\\w+)")
    attrFind = re.compile("([a-zA-Z]\w+)(?= ?(?:\: .*?)?= ?)")

    classes = []
    functions = []
    attrs = []

    for file in files:
        if missingOnly and ext == "py" and not os.path.isfile(
                os.path.join(orig, "pyunity", file + "i")):
            continue
        with open(file, "r") as f:
            content = f.read().rstrip().splitlines()

        module = "pyunity." + os.path.splitext(file)[0].replace(os.path.sep, ".")
        if (len(sys.argv) > 1 and
                not any(module.startswith(item) for item in sys.argv[1:])):
            continue
        module = module.replace(".__init__", "") + "."
        currentClass = {}
        for line in content:
            if re.search(classFind, line):
                if currentClass != {}:
                    classes.append(currentClass)
                name = module + re.search(classFind, line).group()
                currentClass = {"name": name, "methods": []}
            elif re.search(methodFind, line) and currentClass != {}:
                qualname = currentClass["name"] + "." + re.search(methodFind, line).group()
                currentClass["methods"].append(qualname)
            elif re.search(funcFind, line):
                functions.append(module + re.search(funcFind, line).group())
            elif re.match(attrFind, line):
                attrs.append(module + re.match(attrFind, line).group())

        if currentClass != {}:
            classes.append(currentClass)
    os.chdir(orig)
    return classes, functions, attrs

a, b, c = checkFolder("../pyunity", "py")
d, e, f = checkFolder("pyunity", "pyi")

def checkClasses(a, b, c, d, e, f, name):
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

def checkDocstrings():
    os.chdir("../pyunity")
    files = glob.glob("**/*.py", recursive=True)
    files = [x for x in files if not x.startswith("examples") and not x.endswith("Window.py")]

    a = {}
    for file in files:
        with open(file) as f:
            content = f.read()
        if not content.startswith('"""'):
            continue
        docstring = content.split('"""')
        a[file] = docstring[1]

    os.chdir("../stubs/pyunity")
    files = glob.glob("**/*.pyi", recursive=True)
    files = [x for x in files if not x.startswith("examples") and not x.endswith("Window.py")]

    b = {}
    for file in files:
        with open(file) as f:
            content = f.read()
        if not content.startswith('"""'):
            continue
        docstring = content.split('"""')
        b[file] = docstring[1]

    for file in a:
        if file + "i" not in b:
            print("Docstring missing: " + file + "i")
        elif a[file] != b[file + "i"]:
            print("Docstring differs: " + file + "i")

    for file in b:
        if file[:-1] not in a:
            print("Docstring extra: " + file)

    os.chdir(orig)

checkClasses(a, b, c, d, e, f, "missing")
sys.stdout.write("\n\n")
checkClasses(d, e, f, a, b, c, "extra")
sys.stdout.write("\n\n")
checkDocstrings()

file.close()
print = builtins.print
