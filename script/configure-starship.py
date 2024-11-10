
import os
import sys

WINDOWS = sys.platform == "win32"
# config path is same on windows and unix
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "starship.toml")

DOTBIN_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dotconfig", "starship.toml")

# --FLAG to enable and --no-FLAG to disable
# --none to disable all
# --all to enable all
# --force to overwrite existing config
# --list to list all available flags
FORMAT_FLAGS = {
    "git": "git",
    "cmake": "cmake",
    "rust": "rust",
    "node": "nodejs",
    "python": "python",
    "go": "golang",
}

HEADER = """# Starship configuration
# Note: Format is managed by dotbin-cfg starship. Do not edit manually.
# FORMAT"""

def print_help(just_list):
    if not just_list:
        print("dotbin-cfg starship [OPTIONS]")
        print("")
        print("MODE")
        print("  --reverse      Copy from user to dotbin, instead of dotbin to user")
        print("")
        print("PROGRAMS")
    for key in FORMAT_FLAGS:
        print(f"  --{key:<12}  Enable {FORMAT_FLAGS[key]}")
    if not just_list:
        print("")
        print("  --list          Just print the program list")
        print("  --no-PROGRAM    Disable a program (e.g. --no-git)")
        print("  --none          Disable all programs")
        print("  --all           Enable all programs")
        print("  --force         Overwrite existing enabled/disabled state")

def parse_command():
    force = False
    config = {}
    for arg in sys.argv[1:]:
        if arg == "--list":
            print_help(True)
            sys.exit(0)
        if arg == "--reverse":
            copy_to_dotbin()
            sys.exit(0)
        if arg == "--force":
            force = True
            continue
        if arg == "--none":
            for key in FORMAT_FLAGS:
                config[key] = False
            break
        if arg == "--all":
            for key in FORMAT_FLAGS:
                config[key] = True
            break
        found = False
        for key in FORMAT_FLAGS:
            if arg == f"--{key}":
                config[key] = True
                found = True
                break
            if arg == f"--no-{key}":
                config[key] = False
                found = True
                break
        if not found:
            print_help(False)
            sys.exit(1)
    return config, force

def parse_prompt(prompt):
    """Parse the prompt in the existing config"""
    prompt = prompt.lower()
    config = {}
    for key, value in FORMAT_FLAGS.items():
        config[key] = f"${value}" in prompt
    return config

def create_prompt(config):
    """Create prompt string from config (key -> bool)"""
    format = "$shell://$directory"
    if config["git"]:
        format += "$git_branch$git_commit$git_state$git_status"
    format += " "
    del config["git"]
    for key in ["cmake", "rust", "go", "node", "python"]:
        if config[key]:
            format += f"${FORMAT_FLAGS[key]}"
    format += "\\n$time$jobs$character"
    return format

def read_format(path):
    format = ""
    with open(path, "r", encoding="utf-8") as f:
        found = False
        for line in f:
            if not found:
                if line.startswith("# FORMAT"):
                    found = True
                continue
            format += line.rstrip()
    return format

def read_styles(path):
    out = []
    with open(path, "r", encoding="utf-8") as f:
        found = False
        for line in f:
            if not found:
                if line.startswith("# STYLES"):
                    found = True
                continue
            out.append(line.rstrip())
    return out


def copy_to_user(config, force): # config is key -> bool, non-exhaustive
    if not os.path.exists(CONFIG_PATH):
        force = True
        parent = os.path.dirname(CONFIG_PATH)
        if not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
    print("copying starship config to user")
    if force:
        print("overwriting existing config")
        for key in FORMAT_FLAGS:
            if key not in config: # enable by default
                config[key] = True
            elif not config[key]:
                print(f"disabling {FORMAT_FLAGS[key]}")
                config[key] = False
            else:
                config[key] = True
    else:
        existing_config = parse_prompt(read_format(CONFIG_PATH) )
        # update existing
        for key in config:
            if existing_config[key] == config[key]:
                continue
            print(f"updating {FORMAT_FLAGS[key]} -> {config[key]}")
            existing_config[key] = config[key]
        config = existing_config
    styles = read_styles(DOTBIN_CONFIG_PATH)
    write_config(config, styles, CONFIG_PATH)

def copy_to_dotbin():
    print("copying starship config to dotbin")
    config = {}
    for key in FORMAT_FLAGS: # enable all in template
        config[key] = True
    styles = read_styles(CONFIG_PATH)
    write_config(config, styles, DOTBIN_CONFIG_PATH)

def write_config(config, styles, path):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HEADER + "\nformat=\"" + create_prompt(config) + "\"\n")
        f.write("# STYLES\n")
        f.write("\n".join(styles) + "\n")

if __name__ == "__main__":
    config, force = parse_command()
    copy_to_user(config, force)
    print("done")
