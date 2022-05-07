import functools
import inspect
import os
import sys
import glob
os.environ["PYUNITY_CHANGE_MODULE"] = "1"

ignored = ["pyunity.examples.", "pyunity.window.providers."]
origdir = os.getcwd()
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
modules = []
functions = {}

def gettype(obj):
    if obj is None:
        return None
    return type(obj)

def mostCommon(l):
    return sorted(l, key=l.count, reverse=True)[0]

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
        restype = gettype(result)
        for argname, argval in allargs.arguments.items():
            if argname not in functions[self.name].seen_args:
                functions[self.name].seen_args[argname] = []
            functions[self.name].seen_args[argname].append(gettype(argval))
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
        signature = "def "
        signature += self.funcname
        signature += "("
        if self.isMethod:
            if len(self.wrapper.signature.parameters) == 1:
                signature += "self"
            else:
                signature += "self, "

        i = 0
        total = len(self.wrapper.signature.parameters)
        if self.isMethod:
            total -= 1 # Remove self
        for argname in self.wrapper.signature.parameters:
            if argname == "self" and self.isMethod:
                continue
            param = self.wrapper.signature.parameters[argname]
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                signature += "*"
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                signature += "**"
            signature += argname
            if self.called:
                argtype = mostCommon(self.seen_args[argname])
                signature += ": "
                if argtype is None:
                    signature += "None"
                else:
                    signature += argtype.__name__
            if i < total - 1:
                signature += ", "
            i += 1
        signature += ")"
        if self.called:
            signature += " -> "
            restype = mostCommon(self.seen_results)
            if restype is None:
                signature += "None"
            else:
                signature += restype.__name__
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

def loadAll():
    os.chdir(rootdir)

    for file in glob.glob("pyunity/**/*.py", recursive=True):
        qualname = file[:-3].replace(os.path.sep, ".")
        if qualname.endswith(".__init__"):
            qualname = qualname[:-9]

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
        modules.append(qualname)
    os.chdir(origdir)

def wrapAll():
    deferred = {} # Put functions first, classes last
    for modulename in modules:
        module = sys.modules[modulename]
        for objname, obj in vars(module).items():
            if getattr(obj, "__module__", "") != modulename:
                continue
            if isinstance(obj, type):
                for attrname, attr in vars(obj).items():
                    if callable(attr):
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
            elif callable(obj):
                qualname = f"{modulename}.{objname}"
                wrapper = Wrapper(obj, qualname)
                setattr(module, objname, wrapper)
                functions[qualname] = Function(modulename, objname, wrapper)
    functions.update(deferred)

def printAll():
    for name, function in functions.items():
        signature = function.getPythonSig()
        if function.called:
            signature += " # " + name
        print(signature)

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
    files = {}
    for function in functions.values():
        filename = os.path.join(
            "out",
            function.module.replace(".", os.path.sep) + ".pyi")
        if filename not in files:
            files[filename] = []
        files[filename].append(function)

    for file in files:
        currentClass = None
        dependencies = []
        os.makedirs(os.path.dirname(file), exist_ok=True)
        functionWritten = False
        with open(file, "w+") as f:
            for function in files[file]:
                dependencies.extend(function.getDependencies())
                if not function.isMethod:
                    f.write(function.getPythonSig() + "\n")
                    functionWritten = True
                else:
                    if currentClass is None and functionWritten:
                        f.write("\n")
                    if function.class_ is not currentClass:
                        if currentClass is not None:
                            f.write("\n")
                        f.write("class " + function.class_.__name__)
                        bases = []
                        for base in function.class_.__bases__:
                            bases.append(base.__name__)
                            dependencies.append(base)
                        if bases != ["object"]:
                            f.write("(" + ", ".join(bases))
                            metaclass = type(function.class_)
                            if metaclass is not type:
                                f.write(", metaclass=" + metaclass.__name__)
                            f.write(")")
                        f.write(":\n")
                        currentClass = function.class_
                    f.write("    " + function.getPythonSig() + "\n")

if __name__ == "__main__":
    loadAll()
    wrapAll()
    runTests()

    # from pyunity import examples
    # examples.loadExample(0)

    printAll()
    writeAll()
