#!usr/bin/env python
"""
    Manager for dotbin/extra

    `dotbin-extra setup` Will create the extra directories to get started.
    You will put any portable software package in `dotbin/extra/portable`
    and any single-binary portable software in `dotbin/extra/bin`

    `dotbin/extra/bin` and `dotbin/extra/symlink` should be added to PATH

    `dotbin-extra link [--force]` will create symlinks from `portable` to `symlink`.
    Create `dotbin/extra/portable/link` text file and put glob patterns relative
      to `dotbin/extra/portable`, one per line. One symlink will be created per glob file
    
    On windows, adding a `shim:` prefix to the link will create a BATCH shortcut instead of a symlink
      that calls the underlying executable with absolute path. On Linux, bash shortcut is created

    --force will delete existing symlinks/shims

    So you can install new portable software with
        cp -r <folder> ~/dotbin/extra
        vi ~/dotbin/extra/portable/link # add link
        dotbin-extra link

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

def setup():
    extra_dir = find_extra_dir()
    bin_dir = os.path.join(extra_dir, "bin")
    portable_dir = os.path.join(extra_dir, "portable")
    symlink_dir = os.path.join(extra_dir, "symlink")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(portable_dir, exist_ok=True)
    os.makedirs(symlink_dir, exist_ok=True)

def create_batch_shim(symlink_dir, path):
    name = os.path.basename(path)
    name, _ = os.path.splitext(name)
    name = name + ".bat"
    shim_path = os.path.join(symlink_dir, name)
    if os.path.exists(shim_path):
        return
    print(f"shim: {shim_path}")
    with open(shim_path, "w", encoding="utf-8") as f:
        f.write("@echo off\r\n")
        executable = os.path.abspath(path)
        f.write(f"call \"{executable}\" %*")

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
    subprocess.run(["ln", "-s", path, symlink_path], check=True)

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


def link(force):
    extra_dir = find_extra_dir()
    symlink_dir = os.path.join(extra_dir, "symlink")
    if force:
        if os.path.exists(symlink_dir):
            shutil.rmtree(symlink_dir)
        os.makedirs(symlink_dir)
    portable_dir = os.path.join(extra_dir, "portable")
    link_file = os.path.join(portable_dir, "link")
    with open(link_file, "r", encoding="utf-8") as f:
        for line in f:
            link_glob(symlink_dir, portable_dir, line.strip())
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: dotbin-extra setup")
        print("       dotbin-extra link [--force]")
        sys.exit(1)
    command = sys.argv[1]
    if command == "setup":
        setup()
    elif command == "link":
        force = len(sys.argv) > 2 and sys.argv[2] == "--force"
        link(force)