require('nvim_comment').setup({
    create_mappings = false
})

vim.keymap.set('n', '<leader>c', vim.cmd.CommentToggle)
vim.keymap.set('v', '<leader>c', "V<cmd>'<,'>CommentToggle<cr>gv")
