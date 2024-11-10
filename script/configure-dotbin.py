import os
import sys
import shutil
import subprocess
from multiprocessing import Pool

WINDOWS = os.name == "nt"
PWSH = shutil.which("pwsh")
CHMOD = shutil.which("chmod")
CARGO = shutil.which("cargo")

def pwsh():
    if not PWSH:
        raise ValueError("pwsh not found")
    return PWSH

def chmod():
    if not CHMOD:
        raise ValueError("chmod not found")
    return CHMOD

def cargo():
    if not CARGO:
        raise ValueError("cargo not found")
    return CARGO

def get_arg(name, default=None):
    for i, arg in enumerate(sys.argv):
        if arg == name:
            if i + 1 < len(sys.argv):
                return sys.argv[i + 1]
            return True
    return default

def get_dotbin_home():
    return os.path.dirname(os.path.dirname(__file__))

def find_scripts(dotbin_home):
    scripts = []
    for script in os.listdir(dotbin_home):
        if script.endswith(".py"):
            scripts.append(os.path.join(dotbin_home, script))
    return scripts

def create_script_shim(dotbin_bin, script_path, get_script):
    name = os.path.basename(script_path)
    name, _ = os.path.splitext(name)
    if WINDOWS:
        name = name + ".cmd"
    shim_path = os.path.join(dotbin_bin, name)
    print(f"shim: {shim_path}")
    with open(shim_path, "w", encoding="utf-8") as f:
        executable = os.path.abspath(script_path)
        if WINDOWS:
            f.write("@echo off\r\n")
        else:
            f.write("#!/usr/bin/bash\n")
        f.write(get_script(executable))
    if not WINDOWS:
        subprocess.run([chmod(), "+x", shim_path], check=True)

def ps_probe_command(command):
    result = subprocess.run([pwsh(), "-NoLogo", "-NoProfile", "-Command", "Test-Path Alias:"+command], capture_output=True)
    if result.returncode == 0 and result.stdout.decode().strip() != "False":
        return "alias", command
    result = subprocess.run([pwsh(), "-NoLogo", "-NoProfile", "-Command", "Get-Command "+command], capture_output=True)
    if result.returncode == 0:
        return "command", command
    return None, command

def setup_coreutils(dotbin_home, dotbin_bin):
    if not WINDOWS:
        return
    
    # extra utils
    dotbin_windows = os.path.join(dotbin_home, "windows")
    subprocess.run([cargo(), "build", "--bin", "which", "--release"], check=True, cwd=dotbin_windows)
    shutil.copy(os.path.join(dotbin_windows, "target", "release", "which.exe"), dotbin_bin)

    # extra scripts
    for script in os.listdir(dotbin_windows):
        if not script.endswith(".ps1"):
            continue
        print(f"windows script: {script}")
        target=os.path.join(dotbin_bin, script)
        shutil.copyfile(os.path.join(dotbin_windows, script), target)

    # uutils/coreutils
    ps_profile = get_arg("--ps-profile", "AllUsersCurrentHost")
    if ps_profile not in ["CurrentUserCurrentHost", "CurrentUserAllHosts", "AllUsersCurrentHost", "AllUsersAllHosts"]:
        print(f"Invalid --ps-profile: {ps_profile}")
        print("Execute '$Profile | select *' to get the valid profiles")
        sys.exit(1)
    try:
        coreutils = shutil.which("coreutils")
        if not coreutils:
            raise ValueError("coreutils not found")
        result = subprocess.run([coreutils, "--list"], check=True, capture_output=True)
    except:
        subprocess.run([cargo(), "install", "coreutils"], check=True)
        coreutils = shutil.which("coreutils")
        if not coreutils:
            raise ValueError("coreutils not found after cargo install!!!")
        result = subprocess.run([coreutils, "--list"], check=True, capture_output=True)

    util_names = list(set(line.strip() for line in result.stdout.decode().splitlines() if line.strip() != "["))

    # need to probe the commands first, then add the shims
    # otherwise we might find the shims instead
    to_add = set()
    to_probe = util_names
    with Pool() as p:
        for cmd_type, util in p.imap_unordered(ps_probe_command, to_probe):
            if cmd_type is not None:
                print(f"remove {cmd_type}: {util}")
                to_add.add((cmd_type, util))
    for util in util_names:
        if util == "ls":
            ok, _ = ps_probe_command("eza")
            if ok is not None:
                # use eza for ls
                create_script_shim(dotbin_bin, util, lambda _: "eza %*")
                continue
        create_script_shim(dotbin_bin, util, lambda x: f"coreutils {os.path.basename(x)} %*")
    ps_profile_dir = os.path.dirname(subprocess.run([pwsh(), "-NoLogo", "-NoProfile", "-Command", f"echo $PROFILE.{ps_profile}"], check=True, capture_output=True).stdout.decode().strip())
    os.makedirs(ps_profile_dir, exist_ok=True)

    # special utils
    # curl: PS5.1 has an alias, remove it so we use curl.exe
    curl_type, _ = ps_probe_command("curl")
    if curl_type == "alias":
        to_add.add(("alias", "curl"))

    with open(os.path.join(ps_profile_dir, "Initialize-Coreutils.ps1"), "w") as f:
        f.write("# This file is generated by Pistonight/dotbin\n")
        for typ, util in sorted(to_add):
            if typ == "alias":
                f.write(f"Remove-Item Alias:{util} -Force\n")
            else:
                f.write(f"Set-Alias -Name {util} -Value \"{os.path.join(dotbin_bin, util)}.cmd\"\n")
    
    print(f"Add the following to your PowerShell profile (`vipwsh`) to enable the coreutils")
    print()
    print("# Coreutils")
    print(". $PSScriptRoot\\Initialize-Coreutils.ps1")

def setup_archlinux_utils(dotbin_home, dotbin_bin):
    if WINDOWS:
        return
    dotbin_archlinux = os.path.join(dotbin_home, "archlinux")
    for script in os.listdir(dotbin_archlinux):
        print(f"arch script: {script}")
        target=os.path.join(dotbin_bin, script)
        shutil.copyfile(os.path.join(dotbin_archlinux, script), target)
        subprocess.run([chmod(), "+x", target], check=True)

def main():
    dotbin_home = get_dotbin_home()
    dotbin_bin = os.path.join(dotbin_home, "bin")
    if os.path.exists(dotbin_bin):
        shutil.rmtree(dotbin_bin)
    os.makedirs(dotbin_bin)
    scripts = find_scripts(dotbin_home)
    for script in scripts:
        create_script_shim(dotbin_bin, script ,
                           lambda executable:
                           f"python \"{executable}\" %*" if WINDOWS else f"exec python \"{executable}\" \"$@\""
                           )
    setup_coreutils(dotbin_home, dotbin_bin)
    setup_archlinux_utils(dotbin_home, dotbin_bin)
    extra_dir = os.path.join(dotbin_home, "extra")
    bin_dir = os.path.join(extra_dir, "bin")
    portable_dir = os.path.join(extra_dir, "portable")
    symlink_dir = os.path.join(extra_dir, "symlink")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(portable_dir, exist_ok=True)
    os.makedirs(symlink_dir, exist_ok=True)

if __name__ == "__main__":
    main()
