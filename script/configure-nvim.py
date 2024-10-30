import os
import sys
import shutil

WINDOWS = sys.platform == "win32"

if WINDOWS:
    NVIM_HOME = "~\\\\AppData\\\\Local\\\\nvim"
else:
    NVIM_HOME = "~/.config/nvim"
NVIM_HOME = os.path.expanduser(NVIM_HOME)

DOTBIN_CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dotconfig")

def copy_config_file(src, dst, ignore_keep=False):
    """
        Copy src to dst

        If ignore_keep, don't respect @keep-start or @keep-end
    """
    dir_path = os.path.dirname(dst)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    # if dst doesn't exist, just copy src to dst
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        return

    # always process keep sections, for validation
    keep_sections = []
    with open(dst, "r", encoding="utf-8") as f:
        current_keep_section = []
        in_keep_scope = False
        for line in f:
            if not in_keep_scope:
                if line.startswith("-- @keep-start"):
                    in_keep_scope = True
                    current_keep_section = []
            else:
                if line.startswith("-- @keep-end"):
                    in_keep_scope = False
                    keep_sections.append(current_keep_section)
                else:
                    current_keep_section.append(line.rstrip())
        if in_keep_scope:
            raise ValueError("Keep section not closed")

    lines = []
    if ignore_keep:
        with open(src, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip())

    else:
        with open(src, "r", encoding="utf-8") as f:
            current_keep_section_i = -1
            in_keep_scope = False
            for line in f:
                if not in_keep_scope:
                    lines.append(line.rstrip())
                    if line.startswith("-- @keep-start"):
                        current_keep_section_i += 1
                        # only process section if it exists in dst
                        # otherwise use the one from src
                        if current_keep_section_i < len(keep_sections):
                            in_keep_scope = True
                            lines.extend(keep_sections[current_keep_section_i])
                else:
                    if line.startswith("-- @keep-end"):
                        in_keep_scope = False
                        lines.append(line.rstrip())

            if in_keep_scope:
                raise ValueError("Keep section not closed")

    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(lines)+ "\n")


def copy_config_dir(src, dst, path, ignore_keep=False):
    src_path = os.path.join(src, path)
    for entry in os.listdir(src_path):
        sub_path = os.path.join(path, entry)
        src_path = os.path.join(src, sub_path)
        if os.path.isdir(src_path):
            copy_config_dir(src, dst, sub_path, ignore_keep)
        else:
            dst_path = os.path.join(dst, sub_path)
            print(f"cp {src_path} {dst_path}")
            copy_config_file(src_path, dst_path, ignore_keep=ignore_keep)

def comment_out_file(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # is it already commented out?
    if all(line.startswith("--") for line in lines):
        return

    with open(file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write("-- " + line)

def comment_out_extra_files(src, dst, path):
    dst_path = os.path.join(dst, path)
    for entry in os.listdir(dst_path):
        sub_path = os.path.join(path, entry)
        src_path = os.path.join(src, sub_path)
        dst_path = os.path.join(dst, sub_path)
        if os.path.isdir(dst_path):
            comment_out_extra_files(src, dst, sub_path)
        elif not os.path.exists(src_path):
            print(f"commenting out {dst_path}")
            comment_out_file(dst_path)

FILES = [
    # init entry point
    "init.lua",
]
DIRS = [
    "lua",
    "after"
]

def copy_to_dotbin(dotbin_nvim):
    print("updating dotconfig/nvim using user config")
    if os.path.exists(dotbin_nvim):
        shutil.rmtree(dotbin_nvim)
    for f in FILES:
        copy_config_file(os.path.join(NVIM_HOME, f), os.path.join(dotbin_nvim, f), ignore_keep=True)
    for d in DIRS:
        copy_config_dir(NVIM_HOME, dotbin_nvim, d, ignore_keep=True)

def copy_to_user(dotbin_nvim):
    print("updating user config with dotconfig/nvim")
    for f in FILES:
        copy_config_file(os.path.join(dotbin_nvim, f), os.path.join(NVIM_HOME, f), ignore_keep=False)
    for d in DIRS:
        comment_out_extra_files(dotbin_nvim, NVIM_HOME, d)
        copy_config_dir(dotbin_nvim, NVIM_HOME, d, ignore_keep=False)

if __name__ == "__main__":
    dotbin_nvim = os.path.join(DOTBIN_CONFIG, "nvim")
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        copy_to_dotbin(dotbin_nvim)
    else:
        copy_to_user(dotbin_nvim)
