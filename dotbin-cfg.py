"""Shim script to invoke script/configure-xxx.py"""

import sys
import os
import subprocess

WINDOWS = os.name == "nt"

def find_script(script):
    return os.path.join(os.path.dirname(__file__), "script", f"configure-{script}.py")

def main():
    script = find_script(sys.argv[1])
    if not script or not os.path.exists(script):
        print(f"dotbin-cfg: script not found: {script}")
        sys.exit(1)
    args = sys.argv[2:]
    result = subprocess.run([sys.executable, script] + args)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
