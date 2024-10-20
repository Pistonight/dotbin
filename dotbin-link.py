#!usr/bin/env python
"""
    Manager for dotbin/extra

    You will put any portable software package in `dotbin/extra/portable`
    and any single-binary portable software in `dotbin/extra/bin`

    `dotbin/extra/bin` and `dotbin/extra/symlink` should be added to PATH

    `dotbin-link [--force]` will create symlinks from `portable` to `symlink`.
    Create `dotbin/extra/portable/link` text file and put glob patterns relative
      to `dotbin/extra/portable`, one per line. One symlink will be created per glob file
    
    On windows, adding a `shim:` prefix to the link will create a BATCH shortcut instead of a symlink
      that calls the underlying executable with absolute path. On Linux, bash shortcut is created

    Create `dotbin/extra/portable/windows-alias` text file for adding alias for Windows
    The format is:
      <target>:<alias>,<alias>...
      ...
    Like: nvim.exe:vi.exe,vim.exe
    Spaces are trimmed

    --force will delete existing symlinks/shims

    So you can install new portable software with
        cp -r <folder> ~/dotbin/extra
        vi ~/dotbin/extra/portable/link # add link
        dotbin-link

    Admin privilege and `ln` is required for `ln` on windows (`cargo install uu_ln`)
"""

import sys
import subprocess
import os
import shutil
import glob

WINDOWS = os.name == "nt"

def find_extra_dir():
    return os.path.join(os.path.dirname(__file__), "extra")

def create_batch_shim(symlink_dir, path):
    name = os.path.basename(path)
    name, _ = os.path.splitext(name)
    name = name + ".cmd"
    shim_path = os.path.join(symlink_dir, name)
    if os.path.exists(shim_path):
        return
    print(f"shim: {shim_path}")
    with open(shim_path, "w", encoding="utf-8") as f:
        f.write("@echo off\r\n")
        executable = os.path.abspath(path)
        f.write(f"\"{executable}\" %*")

def create_bash_shim(symlink_dir, path):
    name = os.path.basename(path)
    name, _ = os.path.splitext(name)
    name = name + ".sh"
    shim_path = os.path.join(symlink_dir, name)
    if os.path.exists(shim_path):
        return
    print(f"shim: {shim_path}")
    with open(shim_path, "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/bash\n")
        executable = os.path.abspath(path)
        f.write(f"exec \"{executable}\" \"$@\"")
    subprocess.run(["chmod", "+x", shim_path], check=True, shell=True)

def create_shim(symlink_dir, path):
    if WINDOWS:
        create_batch_shim(symlink_dir, path)
    else:
        create_bash_shim(symlink_dir, path)

def create_link(symlink_dir, path):
    name = os.path.basename(path)
    symlink_path = os.path.join(symlink_dir, name)
    if os.path.exists(symlink_path):
        return
    print(f"ln -s {path} {symlink_path}")
    subprocess.run(["ln", "-s", path, symlink_path], check=True, shell=True)

def link_glob(symlink_dir, portable_dir, glob_pattern):
    if glob_pattern.startswith("shim:"):
        shim = True
        glob_pattern = glob_pattern[5:]
    else:
        shim = False
    files = glob.glob(glob_pattern, root_dir=portable_dir, recursive=True)
    if not files:
        print(f"warning: no match for \"{glob_pattern}\"")
        return
    for rel_path in files:
        if shim:
            create_shim(symlink_dir, os.path.join(portable_dir, rel_path))
        else:
            create_link(symlink_dir, os.path.join(portable_dir, rel_path))

def create_alias(symlink_dir, target, aliases):
    target_path = os.path.join(symlink_dir, target)
    if not os.path.exists(target_path):
        print(f"warning: alias target {target_path} doesn't exist, skipping")
        return
    for alias in aliases:
        alias_path = os.path.join(symlink_dir, alias)
        if os.path.exists(alias_path):
            continue
        print(f"ln -s {target_path} {alias_path}")
        subprocess.run(["ln", "-s", target_path, alias_path], check=True, shell=True)


def link(force):
    extra_dir = find_extra_dir()
    symlink_dir = os.path.join(extra_dir, "symlink")
    if force:
        if os.path.exists(symlink_dir):
            shutil.rmtree(symlink_dir)
        os.makedirs(symlink_dir)
    portable_dir = os.path.join(extra_dir, "portable")
    link_file = os.path.join(portable_dir, "link")
    if not os.path.exists(link_file):
        print(f"warning: link file {link_file} doesn't exist, skipping")
    else:
        with open(link_file, "r", encoding="utf-8") as f:
            for line in f:
                link_glob(symlink_dir, portable_dir, line.strip())
    if WINDOWS:
        alias_file = os.path.join(portable_dir, "windows-alias")
        if not os.path.exists(alias_file):
            print(f"warning: alias file {alias_file} doesn't exist, skipping")
        else:
            with open(alias_file, "r", encoding="utf-8") as f:
                for line in f:
                    if ":" not in line:
                        print("warning: missing `:` in line in alias file, skipping")
                        continue
                    target, rest = line.split(":", 1)
                    aliases = [x.strip() for x in rest.split(",")]
                    create_alias(symlink_dir, target.strip(), aliases)

    
if __name__ == "__main__":
    force = len(sys.argv) > 1 and sys.argv[1] == "--force"
    link(force)