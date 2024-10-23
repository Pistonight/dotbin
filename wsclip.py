"""
A simple python websocket server that copies received messages into system clipboard.

This uses [`pyperclip`](https://pypi.org/project/pyperclip/) under the hood, which should work out of box for Windows and MacOS. For Linux, you may need to install `xclip` or `xsel` depending on your distro.

## Why
I use this on my headless dev VM so I can yank from neovim to host

```lua
-- copy to system clipboard (commented out because it doesn't work over ssh)
-- workaround is sending the text over websocket to the host
-- noremap({ 'n', 'v' }, '<leader>y', '"+y')
-- save yanked text to host
-- for host windows machine, this uses powershell set-clipboard
-- for vm ssh session, this uses websocat and a websocket server running on the host machine
vim.cmd([[
if has("win32")
    augroup YankToScript
      autocmd!
      autocmd TextYankPost * if v:register == 'a' | call writefile([getreg('a')], $HOME .. '/.vim/yank') | silent! execute '!(Get-Content $env:USERPROFILE/.vim/yank) -replace "`0","`n" | set-clipboard' | redraw! | endif
    augroup END
else
    augroup YankToScript
      autocmd!
      autocmd TextYankPost * if v:register == 'a' | call writefile([getreg('a')], '/tmp/yank') | silent! execute '!bash -c "source ~/.bashrc && cat /tmp/yank | websocat -1 -t -u ws://$HOST_MACHINE_IP:8881"' | redraw! | endif
    augroup END
endif
]])
```
This requires `export HOST_MACHINE_IP=<IP>` in your `~/.bashrc` and `cargo install websocat` in the system

"""

import asyncio
import websockets
import sys
import pyperclip
DEFAULT_PORT = 8881

def run_server(port):
    async def handle_message(websocket):
        async for message in websocket:
            # Replace the null character from vim yank with newline
            message = message.strip().replace("\x00", "\n")
            length = len(message)
            print(f"Received message {length=}")
            pyperclip.copy(message)
    start_server = websockets.serve(handle_message, "0.0.0.0", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"Server started on port {port}")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
