import os, sys

assert len(sys.argv) > 1
assert sys.argv[1].endswith(".c")
name = sys.argv[1][:-2]

cmds = [
    "md build", "g++ -c " + name + ".c -o build/" + name + ".o",
    "g++ -c unity.c -o build/unity.o", "g++ -c unity.c -o build/unity.o",
    "ar rcs libs/libunity.a build/unity.o",
    "g++ build/" + name + ".o -Llibs -lunity -o " + name + ".exe", name + ".exe"
]

for cmd in cmds:
    result = os.system(cmd)
    if result: break

if os.path.isdir("build"): os.system("rmdir /s /q build")