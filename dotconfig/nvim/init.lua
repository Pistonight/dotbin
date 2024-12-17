--[[
MIT License

Copyright (c) 2025 Michael

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
]]
-- Nvim configuration structure:
-- lua/ -> base configuration files
--   - lazy-cfgw/      -> lazy loaded configuration files and wrapper scripts
--   - integration.lua -> turn integration on/off
--   - keys.lua        -> base vim.keymap settings (exclusing lsp specific)
--   - opts.lua        -> base vim.opt settings
--   - plugins.lua     -> package manager (packer.nvim) configuration
-- after/plugin/ -> plugin configuration files
--
-- cache/ and plugin/ are cache directories

-- disable nvim builtin file explorer
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
require('plugins')
require('keys')
require('opts')
