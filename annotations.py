import os
import glob
import re

os.chdir("pyunity")
files = glob.glob("**/*.py", recursive=True)
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
            current_class["methods"].append(module + current_class["name"] + \
                "." + re.search(method_find, line).group())
        elif re.search(func_find, line):
            functions.append(module + re.search(func_find, line).group())
        elif re.match(attr_find, line):
            attrs.append(module + re.match(attr_find, line).group())
    
    if current_class != {}:
        classes.append(current_class)

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
