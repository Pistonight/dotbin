import os
import sys

def is_windows():
    return os.name == "nt"

def find_scripts():
    scripts = []
    bin_home = os.path.dirname(os.path.dirname(__file__))
    for script in os.listdir(bin_home):
        if script.endswith(".py"):
            scripts.append((script[:-3], os.path.join(bin_home, script)))
    return scripts

def add_script_lines(scripts, lines, tag):
    lines.append(tag)
    script_lines = []
    if is_windows():
        for (script, path) in scripts:
            script_lines.append(f"function {script} {{ python {path} $args}}")
    else:
        for (script, path) in scripts:
            script_lines.append(f"alias {script}={path}")
    for line in script_lines:
        lines.append(line)
        print(line)
    lines.append(tag)

def inject_to(scripts, file):
    lines = []
    TAG = "# Pistonight/dotbin"
    appended = 0
    with open(file, "r") as f:
        for l in f:
            if appended == 0 and l.strip() == TAG:
                add_script_lines(scripts, lines, TAG)
                appended = 1
            elif appended == 1:
                if l.strip() == TAG:
                    appended = 2
            else:
                lines.append(l.rstrip())
    if appended == 0:
        add_script_lines(scripts, lines, TAG)
    elif appended == 1:
        print(f"Error: {TAG} is not closed. Please fix {file} manually")
        return
    with open(file, "w") as f:
        for l in lines:
            f.write(l + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python _setup.py <file>")
        sys.exit(1)
    file = sys.argv[1]
    inject_to(find_scripts(), file)