from subprocess import run

dependency_file_path = "../tracker/components/basicComponents.py"
local_dependency_code = """import sys\nsys.path.insert(0, "C:/Repos/tkcomponents")"""

is_live = "tkComponents" in str(run("pip list", capture_output=True).stdout)

print("Current environment: {0}".format("live" if is_live else "test"))
while True:
    inp = input("Switch to {0}? (y/n) :".format("test" if is_live else "live"))

    if inp in ("y", "yes"):
        break
    elif inp in ("n", "no"):
        raise SystemExit
    else:
        print("\nUnrecognised input.")

with open(dependency_file_path, "r") as file:
    file_contents = file.read()

if is_live:
    run("pip uninstall tkComponents", text=True, input="y")

    if local_dependency_code not in file_contents:
        with open(dependency_file_path, "w") as new_file:
            new_file.write(local_dependency_code+"\n\n"+file_contents)
else:
    run("pip install tkComponents")

    with open(dependency_file_path, "w") as new_file:
        new_file.write(file_contents.replace(local_dependency_code, "").lstrip("\n"))

input("\nEnter to quit :")
raise SystemExit
