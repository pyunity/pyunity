import os, sys

assert len(sys.argv) > 1
assert sys.argv[1].endswith(".c")
name = sys.argv[1][:-2]

os.system("md build")
os.system("g++ -c " + name + ".c -o build/" + name + ".o")
os.system("g++ -c unity.c -o build/unity.o")
os.system("ar rcs libs/libunity.a build/unity.o")
os.system("g++ build/" + name + ".o -Llibs -lunity -o " + name + ".exe")
os.system("rmdir /s /q build")
os.system(name + ".exe")