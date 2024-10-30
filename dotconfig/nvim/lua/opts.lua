-- OPTIONS
-- line numbers
vim.opt.number = true    -- Enable line numbers
vim.opt.rnu = true       -- Relative line numbers by default
-- hidden characters (controlled by keymapping)
vim.opt.listchars = "tab:▸ ,trail:·,nbsp:␣,extends:»,precedes:«,eol:↲"
-- indent
vim.opt.expandtab = true -- Tab become spaces
vim.opt.shiftwidth = 4   -- Indent 4
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.smartindent = true

vim.opt.wrap = false

vim.opt.termguicolors = true -- colors
-- undo dir
vim.opt.swapfile = false
vim.opt.backup = false
vim.opt.undofile = true
local home = os.getenv('HOME')
if home == nil then
    home = os.getenv('USERPROFILE')
end
if home ~= nil then
    vim.opt.undodir = home .. '/.vim/undodir'
end

-- folds
vim.opt.foldenable = false   -- no fold at startup
vim.opt.foldmethod = 'expr'  -- treesitter folding
vim.opt.foldexpr = 'nvim_treesitter#foldexpr()'
-- search
vim.opt.hlsearch = true
vim.opt.incsearch = true -- should be the default
-- scrolling
vim.opt.scrolloff = 8
vim.opt.sidescrolloff = 8

-- filetypes
-- note that setting it in this way doesn't work in telescope preview
-- txtpp
vim.cmd [[
  au BufRead,BufNewFile *.md.txtpp                set filetype=markdown
  au BufRead,BufNewFile *.html.txtpp              set filetype=html
  au BufRead,BufNewFile *.rs.txtpp                set filetype=rust
  au BufRead,BufNewFile *.ts.txtpp                set filetype=typescript
  au BufRead,BufNewFile *.tsx.txtpp               set filetype=typescriptreact
  au BufRead,BufNewFile *.js.txtpp                set filetype=javascript
  au BufRead,BufNewFile *.jsx.txtpp               set filetype=javascriptreact
  au BufRead,BufNewFile *.py.txtpp                set filetype=python
  au BufRead,BufNewFile *.css.txtpp               set filetype=css
  au BufRead,BufNewFile *.json.txtpp              set filetype=json
  au BufRead,BufNewFile *.yaml.txtpp              set filetype=yaml
  au BufRead,BufNewFile *.yml.txtpp               set filetype=yaml
  au BufRead,BufNewFile *.toml.txtpp              set filetype=toml
  au BufRead,BufNewFile *.bash.txtpp              set filetype=bash
]]