-- styling
vim.g.floaterm_title = 'Terminal [$1/$2]'
-- toggle floaterm
vim.keymap.set('n', [[<C-\>]], vim.cmd.FloatermToggle)
vim.keymap.set('t', [[<C-\>]], vim.cmd.FloatermToggle)
-- new floaterm terminal
vim.keymap.set('n', [[<leader><C-\>]], vim.cmd.FloatermNew)
vim.keymap.set('t', [[<leader><C-\>]], [[<C-\><C-n><cmd>FloatermNew<CR>]])
-- back to normal mode with Ctrl-w
vim.keymap.set('t', '<C-w>', [[<C-\><C-n>]])
-- cycle through terminals
vim.keymap.set('n', '<C-n>', vim.cmd.FloatermNext)
vim.keymap.set('t', '<C-n>', vim.cmd.FloatermNext)