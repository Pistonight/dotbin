# This is invoked by nvim to start jdtls, see java.lua

import os
import sys
import subprocess

if __name__ != "__main__":
    raise Exception("This script is not meant to be imported")

java_path = sys.argv[1]
jdtls_base_directory = os.path.abspath(sys.argv[2])
project_name = sys.argv[3]
plugins_dir = os.path.join(jdtls_base_directory, "plugins")
launcher = None
for jar in os.listdir(plugins_dir):
    if jar.startswith("org.eclipse.equinox.launcher_"):
        launcher = os.path.join(plugins_dir, jar)
        break
if launcher is None:
    raise Exception("Cannot find equinox launcher")

if sys.platform == "darwin":
    config_path = os.path.join(jdtls_base_directory, "config_mac")
elif sys.platform == "win32":
    config_path = os.path.join(jdtls_base_directory, "config_win")
else:
    config_path = os.path.join(jdtls_base_directory, "config_linux")

exec_args = [
    '-Declipse.application=org.eclipse.jdt.ls.core.id1',
    '-Dosgi.bundles.defaultStartLevel=4',
    '-Declipse.product=org.eclipse.jdt.ls.core.product',
    '-Dlog.protocol=true',
    '-Dlog.level=ALL',
    '-Xmx4g',
    '--add-modules=ALL-SYSTEM',
    '--add-opens', 'java.base/java.util=ALL-UNNAMED',
    '--add-opens', 'java.base/java.lang=ALL-UNNAMED',
    '-jar', launcher,
    '-configuration', config_path,
    '-data', os.path.join(jdtls_base_directory, "workspace", project_name),

]

print("Starting jdtls with args: " + str(exec_args))
if os.name == 'posix':
    os.execvp(java_path, exec_args)
else:
    subprocess.run([java_path] + exec_args)
