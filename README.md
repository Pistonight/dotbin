# dotbin
My python util scripts

## Installation
First clone the repo to a place like `~/dotbin`.

Then install dependencies
```bash
pip install -r ~/dotbin/requirements.txt
```

Then setup shell aliases using the steps below. This will setup aliases for scripts in the `~/dotbin` directory.
For example `n` maps to `n.py`. Currently only bash and powershell are supported.

### Bash
```bash
python ~/dotbin/_setup.py ~/.bashrc
```

### PowerShell (Windows only)
```powershell
python ~/dotbin/_setup.py $Profile
```

### Index
- [`n`](n.py) - Number format utility
- [`wsclip`](wsclip.py) - Clipboard server running over websocket