import functools
import inspect
import typing
import types as _types
import os
import sys
import ast
import glob
from pathlib import Path
os.environ["PYUNITY_CHANGE_MODULE"] = "0"

ignored = ["pyunity.examples.", "pyunity.window.providers."]
origdir = os.getcwd()
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
modules = {}
functions = {}
classes = {}

def formatannotation(annotation):
    if isinstance(annotation, typing._UnionGenericAlias):
        return " | ".join(map(formatannotation, annotation.__args__))
    elif isinstance(annotation, type):
        return annotation.__name__
    elif isinstance(annotation, (typing._BaseGenericAlias, typing._SpecialForm)):
        return annotation._name
    return repr(annotation)
inspect.formatannotation = formatannotation

def gettype(obj):
    if obj is None:
        return None
    t = type(obj)
    if t is list:
        types = set(map(type, obj))
        if len(types) == 1:
            return list[types.pop()]
    elif t is dict:
        keytypes = set(map(type, obj.keys()))
        if len(keytypes) == 1:
            keytype = keytypes.pop()
        else:
            keytype = typing.Any
        valuetypes = set(map(type, obj.values()))
        if len(valuetypes) == 1:
            valuetype = valuetypes.pop()
        else:
            valuetype = typing.Any
        if keytype != typing.Any or valuetype != typing.Any:
            return dict[keytype, valuetype]
    elif isinstance(obj, (type(print), _types.FunctionType)):
        return typing.Callable
    elif isinstance(obj, type(a for a in "")):
        return typing.Generator
    elif issubclass(t, Path):
        return typing.Union[str, Path]
    return t

def mostCommon(l):
    return sorted(l, key=l.count, reverse=True)[0]

def relativeTo(mod, current, ispkg=False):
    modparts = mod.split(".")
    currentparts = current.split(".")
    if ispkg:
        currentparts.append("__init__")
    if modparts[0] != currentparts[0]:
        # No common parent package
        return mod

    # Remove all common parent packages
    while (len(modparts) and len(currentparts) and
            modparts[0] == currentparts[0]):
        modparts.pop(0)
        currentparts.pop(0)

    module = "." * len(currentparts) + ".".join(modparts)
    return module

def correctModule(module):
    if module == "_io":
        return "io"
    if module.startswith("pyunity.physics"):
        return "pyunity.physics"
    if module.startswith("pyunity.scenes"):
        return "pyunity.scenes"
    if module.startswith("pyunity.values"):
        return "pyunity.values"
    return module

class Wrapper:
    def __init__(self, func, name):
        self.func = func
        self.name = name
        self.signature = inspect.signature(self.func)

    def __get__(self, instance, owner):
        @functools.wraps(self.func)
        def inner(*args, **kwargs):
            return self(instance, *args, **kwargs)
        return inner

    def __call__(self, *args, **kwargs):
        try:
            allargs = self.signature.bind(*args, **kwargs)
        except:
            print(args)
            raise
        allargs.apply_defaults()
        allargs.arguments.pop("self", None)

        result = self.func(*args, **kwargs)
        for argname, argval in allargs.arguments.items():
            if argname not in functions[self.name].seen_args:
                functions[self.name].seen_args[argname] = []
            functions[self.name].seen_args[argname].append(gettype(argval))
        restype = gettype(result)
        functions[self.name].seen_results.append(restype)
        return result

class Function:
    def __init__(self, module, funcname, wrapper, class_=None, isMethod=False):
        self.module = module
        self.funcname = funcname
        self.class_ = class_
        self.wrapper = wrapper
        self.isMethod = isMethod
        self.seen_args = {}
        self.seen_results = []

    @property
    def called(self):
        return len(self.seen_results) != 0

    def getPythonSig(self):
        modifiedSig = self.wrapper.signature.replace()
        if self.called:
            parameters = dict(modifiedSig.parameters)
            for argname in self.seen_args:
                # if parameters[argname].annotation != inspect.Parameter.empty:
                #     continue
                argtype = mostCommon(self.seen_args[argname])
                param = parameters[argname]
                parameters[argname] = param.replace(annotation=argtype)
            if True or modifiedSig.return_annotation == inspect.Signature.empty:
                restype = mostCommon(self.seen_results)
                modifiedSig = modifiedSig.replace(return_annotation=restype)
            modifiedSig = modifiedSig.replace(parameters=parameters.values())

        signature = "def "
        signature += self.funcname
        signature += str(modifiedSig)

        # signature += "("
        # if self.isMethod:
        #     if len(self.wrapper.signature.parameters) == 1:
        #         signature += "self"
        #     else:
        #         signature += "self, "

        # i = 0
        # total = len(self.wrapper.signature.parameters)
        # if self.isMethod:
        #     total -= 1 # Remove self
        # for argname in self.wrapper.signature.parameters:
        #     if argname == "self" and self.isMethod:
        #         continue
        #     param = self.wrapper.signature.parameters[argname]
        #     if param.kind == inspect.Parameter.VAR_POSITIONAL:
        #         signature += "*"
        #     elif param.kind == inspect.Parameter.VAR_KEYWORD:
        #         signature += "**"
        #     signature += argname
        #     if self.called:
        #         argtype = mostCommon(self.seen_args[argname])
        #         signature += ": "
        #         if argtype is None:
        #             signature += "None"
        #         else:
        #             signature += argtype.__name__
        #     if i < total - 1:
        #         signature += ", "
        #     i += 1
        # signature += ")"
        # if self.called:
        #     signature += " -> "
        #     restype = mostCommon(self.seen_results)
        #     if restype is None:
        #         signature += "None"
        #     else:
        #         signature += restype.__name__

        signature += ": ..."
        return signature

    def getDependencies(self):
        dependencies = []
        for arg in self.seen_args:
            if not len(self.seen_args[arg]):
                continue
            argtype = mostCommon(self.seen_args[arg])
            if argtype is not None:
                dependencies.append(argtype)
        if len(self.seen_results):
            restype = mostCommon(self.seen_results)
            dependencies.append(restype)
        return dependencies

class Class:
    def __init__(self, name, bases, metaclass, methods):
        self.name = name
        self.bases = bases
        self.metaclass = metaclass
        self.methods = methods

    def getPythonSig(self):
        sig = "class " + self.name
        bases = []
        for base in self.bases:
            bases.append(base.__name__)
        if self.metaclass is not type:
            bases.append("metaclass=" + self.metaclass.__name__)
        if bases != ["object"]:
            sig += "(" + ", ".join(bases)
            sig += ")"
        sig += ":"
        return sig

    def getDependencies(self):
        return list(self.bases) + [self.metaclass]

class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def getDependencies(self):
        return [self.type]

    def getPythonSig(self):
        return f"{self.name}: {formatannotation(self.type)} = ..."

class Module:
    def __init__(self, name, ispkg=False):
        self.name = name
        self.module = sys.modules[self.name]
        self.variables = []
        self.functions = []
        self.classes = []
        self.ispkg = ispkg

def loadAll():
    os.chdir(rootdir)

    for file in glob.glob("pyunity/**/*.py", recursive=True):
        qualname = file[:-3].replace(os.path.sep, ".")
        ispkg = False
        if qualname.endswith(".__init__"):
            qualname = qualname[:-9]
            ispkg = True

        if qualname.endswith("__main__"):
            continue
        skip = False
        for module in ignored:
            if qualname.startswith(module):
                skip = True
                break
        if skip:
            continue

        __import__(qualname)
        assert qualname in sys.modules
        modules[qualname] = Module(qualname, ispkg)
    os.chdir(origdir)

def wrapAll():
    def resolve(token):
        while not isinstance(token, ast.Name):
            token = token.value
        return token.id

    deferred = {} # Put functions first, classes last
    for modulename in modules:
        module = sys.modules[modulename]

        with open(module.__file__) as f:
            code = f.read()
        tree = ast.parse(code)
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                var = resolve(target)
                if var == "__all__":
                    continue
                assert hasattr(module, var)
                vartype = gettype(getattr(module, var))
                modules[modulename].variables.append(Variable(var, vartype))

        for objname, obj in vars(module).items():
            if getattr(obj, "__module__", "") != modulename:
                continue
            if isinstance(obj, type):
                classname = f"{modulename}.{objname}"
                cls = Class(objname, obj.__bases__, type(obj), [])
                classes[classname] = cls
                for attrname, attr in vars(obj).items():
                    if callable(attr):
                        print(obj, attrname, attr)
                        if attr.__qualname__ != obj.__qualname__ + "." + attrname:
                            # Not defined in class
                            continue
                        if isinstance(attr, Wrapper):
                            continue
                        qualname = f"{modulename}.{objname}.{attrname}"
                        wraps = functools.wraps(attr)
                        wrapper = wraps(Wrapper(attr, qualname))
                        setattr(obj, attrname, wrapper)
                        f = Function(modulename, attrname, wrapper, obj, True)
                        deferred[qualname] = f
                        cls.methods.append(f)
                modules[modulename].classes.append(cls)
            elif callable(obj):
                qualname = f"{modulename}.{objname}"
                wrapper = Wrapper(obj, qualname)
                setattr(module, objname, wrapper)
                f = Function(modulename, objname, wrapper)
                functions[qualname] = f
                modules[modulename].functions.append(f)
    functions.update(deferred)

def printModule(module, file=sys.stdout):
    dependencies = []
    for var in module.variables:
        dependencies.extend(var.getDependencies())
        file.write(var.getPythonSig() + "\n")

    for function in module.functions:
        dependencies.extend(function.getDependencies())
        file.write(function.getPythonSig() + "\n")

    if len(module.functions):
        file.write("\n")

    i = 0
    for cls in module.classes:
        dependencies.extend(cls.getDependencies())
        file.write(cls.getPythonSig())
        if len(cls.methods) == 0:
            file.write(" ...")
        file.write("\n")
        for method in cls.methods:
            dependencies.extend(method.getDependencies())
            file.write("    " + method.getPythonSig() + "\n")
        if i < len(module.classes) - 1:
            file.write("\n")
    file.flush()
    return dependencies

def printAll():
    for module in modules.values():
        printModule(module)

def runTests():
    import _pytest

    print(rootdir)
    os.environ["full"] = "1"
    os.chdir(os.path.join(rootdir))
    for file in glob.glob("tests/**/test*.py", recursive=True):
        qualname = file[:-3].replace(os.path.sep, ".")
        __import__(qualname)
        module = sys.modules[qualname]
        for objname, obj in vars(module).items():
            if objname == "TestCase":
                continue
            if objname.startswith("Test") and isinstance(obj, type):
                suite = None
                for attrname, attr in vars(obj).items():
                    if attrname.startswith("test") and callable(attr):
                        print(f"{objname}.{attrname}")
                        if suite is None:
                            suite = obj()
                        try:
                            attr(suite)
                        except _pytest.outcomes.Skipped:
                            pass
    os.chdir(origdir)

def writeAll():
    for modname in modules:
        module = modules[modname]
        file = os.path.join("out", *module.name.split("."))
        if module.ispkg:
            file = os.path.join(file, "__init__")
        file += ".pyi"
        os.makedirs(os.path.dirname(file), exist_ok=True)

        with open(file, "w+") as f:
            dependencies = printModule(module, f)

        deps = list(set(dependencies))
        for i in range(len(deps) - 1, -1, -1):
            t = deps[i]
            if hasattr(t, "__args__"):
                for type_ in t.__args__:
                    if type_.__module__ != "builtins":
                        deps.append(type_)
                if t.__origin__.__module__ != "builtins":
                    deps.append(t.__origin__)
                deps.remove(t)
            elif t is None or t.__module__ == "builtins":
                deps.remove(t)

        imports = {}
        for dep in deps:
            if dep.__module__ not in imports:
                imports[dep.__module__] = []
            imports[dep.__module__].append(dep)

        importlines = []
        for targetmod in imports:
            if targetmod == module.name:
                continue
            variables = []
            for var in imports[targetmod]:
                variables.append(formatannotation(var))
            mod = relativeTo(correctModule(targetmod), module.name, module.ispkg)
            line = f"from {mod} import "
            line += ", ".join(variables)
            importlines.append(line)

        with open(file) as f:
            contents = f.read()
            if contents.endswith("\n\n"):
                contents = contents[:-1]

        with open(file, "w") as f:
            text = ""
            if hasattr(module.module, "__all__"):
                indent = 11
                limit = 79 - indent
                text += "__all__ = ["
                length = 0
                for item in module.module.__all__:
                    length += len(item) + 4
                    if length > limit:
                        text += "\n" + " " * indent
                        length = len(item) + 4
                    text += "\"" + item + "\", "
                if len(module.module.__all__):
                    text = text[:-2]
                text += "]"
                f.write(text + "\n\n")

            f.write("\n".join(importlines))
            if len(importlines):
                f.write("\n\n")
            f.write(contents)

    copies = {
        "../pyunity/scenes/__init__.py": "out/pyunity/scenes/__init__.pyi",
        "../pyunity/physics/__init__.py": "out/pyunity/physics/__init__.pyi",
        "../pyunity/values/__init__.py": "out/pyunity/values/__init__.pyi",
    }
    for src in copies:
        dest = copies[src]
        with open(dest, "w+") as f:
            with open(src) as f2:
                f.write(f2.read().split("\"\"\"", 2)[-1].lstrip())

    os.chdir(rootdir)
    import prepare
    prepare.checkLicense()
    os.chdir(origdir)

if __name__ == "__main__":
    loadAll()
    wrapAll()
    runTests()

    from pyunity import examples
    examples.loadExample(0)

    printAll()
    writeAll()
