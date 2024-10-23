#!usr/bin/env python
"""
    Manager for dotbin/extra

    You will put any portable software package in `dotbin/extra/portable`
    and any single-binary portable software in `dotbin/extra/bin`

    `dotbin/extra/bin` and `dotbin/extra/symlink` should be added to PATH

    `dotbin-link [--force]` will create symlinks from `portable` to `symlink`.
    The links are configured by `dotbin/extra/portable/link` text file.

    The file contains one configuration entry per line. Each entry is of the form:

        (alias=ALIASES)?(shim:)?PATH
    or
        alias=ALIASES(shim:)?which:PATH
    
    PATH should be the relative path or a glob pattern from `dotbin/extra/portable`.

    A symbolic link will be created in `dotbin/extra/symlink` pointing to the original
    file, unless `shim:` is specified, in which case a `.cmd` shim (no extension on non-Windows)
    will be created to invoke the original file. Use `shim` when the executable has local
    dependencies.

    `alias=ALIASES` will create additional symbolic links to the link/shim created.
    Alternatively, you can put the aliases in the shell profile, which will only make
    them available for that shell. Use `,` to separate multiple aliases.

    `alias` can only be used for path or glob pattern that matches exactly 1 file

    `which` can be used to create aliases to other programs. In this case, `shim` determines
    if a symbolic or shim is created for that alias.

    --force will delete existing symlinks/shims
"""

import sys
import subprocess
import os
import shutil
import glob

WINDOWS = os.name == "nt"

def find_extra_dir():
    return os.path.join(os.path.dirname(__file__), "extra")

def create_batch_shim(symlink_dir, path, shim_name):
    name = shim_name + ".cmd"
    shim_path = os.path.join(symlink_dir, name)
    if os.path.exists(shim_path):
        return
    print(f"shim: {shim_path}")
    with open(shim_path, "w", encoding="utf-8") as f:
        f.write("@echo off\r\n")
        executable = os.path.abspath(path)
        f.write(f"\"{executable}\" %*")

def create_bash_shim(symlink_dir, path, shim_name):
    name = shim_name
    shim_path = os.path.join(symlink_dir, name)
    if os.path.exists(shim_path):
        return
    print(f"shim: {shim_path}")
    with open(shim_path, "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/bash\n")
        executable = os.path.abspath(path)
        f.write(f"exec \"{executable}\" \"$@\"")
    subprocess.run(["chmod", "+x", shim_path], check=True)

def create_shim(symlink_dir, path, shim_name):
    if WINDOWS:
        create_batch_shim(symlink_dir, path, shim_name)
    else:
        create_bash_shim(symlink_dir, path, shim_name)

def create_link(symlink_dir, path):
    name = os.path.basename(path)
    symlink_path = os.path.join(symlink_dir, name)
    if os.path.exists(symlink_path):
        return
    print(f"ln -s {path} {symlink_path}")
    subprocess.run(["ln", "-s", path, symlink_path], check=True, shell=WINDOWS)


def create_alias(symlink_dir, target, aliases, shim):
    if not os.path.exists(target):
        print(f"warning: alias target {target} doesn't exist, skipping")
        return
    for alias in aliases:
        if shim:
            create_shim(symlink_dir, target, alias)
        else:
            _, ext = os.path.splitext(target)
            alias_path = os.path.join(symlink_dir, alias+ext)
            if os.path.exists(alias_path):
                continue
            print(f"ln -s {target} {alias_path}")
            subprocess.run(["ln", "-s", target, alias_path], check=True, shell=WINDOWS)

def add_link(symlink_dir, portable_dir, config: str):
    original_config = config
    if config.startswith("alias="):
        config = config[6:]
        colon = config.find(":")
        if colon < 0:
            print(f"error: invalid alias config {original_config}")
            sys.exit(1)
        aliases = config[:colon]
        config = config[colon+1:]
        aliases = [x.strip() for x in aliases.split(",") if x.strip()]
    else:
        aliases = []
    
    if config.startswith("shim:"):
        shim = True
        config = config[5:]
    else:
        shim = False

    if config.startswith("which:"):
        if not aliases:
            print(f"warning: `which` used without `alises`, skipping")
            return
        config = config[6:]
        result = subprocess.run(["which", config], capture_output=True, shell=WINDOWS)
        if result.returncode != 0:
            print(f"warning: no match for \"which:{config}\"")
            return
        target = result.stdout.decode().strip()
    else:
        files = glob.glob(config, root_dir=portable_dir, recursive=True)
        if not files:
            print(f"warning: no match for \"{config}\"")
            return
        if len(files) > 1 and aliases:
            raise ValueError("`alias` can only be used for glob patterns that match 1 file")
        files = [os.path.join(portable_dir, x) for x in files]
        for path in files:
            if shim:
                name = os.path.basename(path)
                name, _ = os.path.splitext(name)
                create_shim(symlink_dir, path, name)
            else:
                create_link(symlink_dir, path)
        target = files[0]

    create_alias(symlink_dir, target, aliases, shim)

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
        return

    with open(link_file, "r", encoding="utf-8") as f:
        for line in f:
            add_link(symlink_dir, portable_dir, line.strip())
    
if __name__ == "__main__":
    force = len(sys.argv) > 1 and sys.argv[1] == "--force"
    link(force)
