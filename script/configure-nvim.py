import os
import sys
import subprocess
import shutil

if sys.platform == "win32":
    NVIM_HOME = "~\\\\AppData\\\\Local\\\\nvim"
else:
    NVIM_HOME = "~/.config/nvim"
NVIM_HOME = os.path.expanduser(NVIM_HOME)

DOTBIN_CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dotconfig")

def copy_to_dotbin(dotbin_nvim):
    subprocess.run(["cp", os.path.join(NVIM_HOME, "init.lua"), dotbin_nvim], check=True, shell=True)
    subprocess.run(["cp", "-r", os.path.join(NVIM_HOME, "after"), dotbin_nvim], check=True, shell=True)
    subprocess.run(["cp", "-r", os.path.join(NVIM_HOME, "lua"), dotbin_nvim], check=True, shell=True)

def copy_to_user(dotbin_nvim):
    subprocess.run(["cp", os.path.join(dotbin_nvim, "init.lua"), NVIM_HOME], check=True, shell=True)
    shutil.rmtree(os.path.join(NVIM_HOME, "after"))
    shutil.rmtree(os.path.join(NVIM_HOME, "lua"))
    subprocess.run(["cp", "-r", os.path.join(dotbin_nvim, "after"), NVIM_HOME], check=True, shell=True)
    subprocess.run(["cp", "-r", os.path.join(dotbin_nvim, "lua"), NVIM_HOME], check=True, shell=True)

if __name__ == "__main__":
    dotbin_nvim = os.path.join(DOTBIN_CONFIG, "nvim")
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        print("updating dotconfig/nvim using user config")
        copy_to_dotbin(dotbin_nvim)
    else:
        print("updating user config with dotconfig/nvim")
        copy_to_user(dotbin_nvim)