import pyunity
import inspect

f = open("missing_annotations.txt", "w+")

for item in pyunity.__all__:
    obj = getattr(pyunity, item)
    if not isinstance(obj, type):
        continue
    annotations = getattr(obj, "__annotations__", {})
    functions = [name for name, value in vars(obj).items() if inspect.isroutine(value)]
    attributes = [name for name, value in vars(obj).items() if not (inspect.isroutine(value) or name.startswith("__"))]

    for function in functions:
        if function not in annotations:
            print(item + "." + function + " is not annotated (FUNCTION)")
            f.write(item + "." + function + " is not annotated (FUNCTION)\n")
    for attribute in attributes:
        if attribute not in annotations:
            print(item + "." + attribute + " is not annotated (ATTRIBUTE)")
            f.write(item + "." + attribute + " is not annotated (ATTRIBUTE)\n")

f.close()
