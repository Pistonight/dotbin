-- disable nvim builtin file explorer
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
-- load plugins
require('plugins')
-- load key mappings and options
require('keys')
require('opts')

-- windows specials
vim.cmd([[
if has("win32")
    set shell=pwsh
    set shellcmdflag=-command
    set shellquote="
    set shellxquote=
endif
]])
