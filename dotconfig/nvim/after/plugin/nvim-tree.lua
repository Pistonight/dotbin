local api = require "nvim-tree.api"
vim.keymap.set('n', '<leader>t', api.tree.open) -- open tree and focus
vim.cmd([[
    augroup NvimTreeAutoFocus
        autocmd BufEnter * lua require'nvim-tree.api'.tree.find_file()
    augroup END


]])
local function on_attach_nvim_tree(bufnr)
    -- only attack keys i need
    local function opts(desc)
        return {
            desc = 'nvim-tree: ' .. desc,
            buffer = bufnr,
            noremap = true,
            silent = true,
            nowait = true
        }
    end
    vim.keymap.set('n', '<C-k>', api.node.show_info_popup, opts('Info'))
    vim.keymap.set('n', 'O', api.node.navigate.parent_close, opts('Close parent'))
    vim.keymap.set('n', 'P', api.node.navigate.parent, opts('Go to parent'))
    vim.keymap.set('n', 'm', api.fs.rename_sub, opts('Move'))
    vim.keymap.set('n', 'o', api.node.open.edit, opts('Open'))
    vim.keymap.set('n', 'v', api.node.open.vertical, opts('Open: vertical'))
    vim.keymap.set('n', 's', api.node.open.horizontal, opts('Open: split'))
    vim.keymap.set('n', 'a', api.fs.create, opts('Create'))
    vim.keymap.set('n', 'c', api.fs.copy.node, opts('Copy'))
    vim.keymap.set('n', 'p', api.fs.paste, opts('Paste'))
    vim.keymap.set('n', 'd', api.fs.remove, opts('Delete'))
    vim.keymap.set('n', 'D', api.fs.trash, opts('Trash'))
    vim.keymap.set('n', 'x', api.fs.cut, opts('Cut'))
    vim.keymap.set('n', 'r', api.fs.rename_sub, opts('Rename'))
    vim.keymap.set('n', '-', api.marks.toggle, opts('Select'))
    vim.keymap.set('n', 'bd', api.marks.bulk.delete, opts('Delete: selected'))
    vim.keymap.set('n', 'bm', api.marks.bulk.move, opts('Move: selected'))
    vim.keymap.set('n', '[', api.node.navigate.diagnostics.prev, opts('Prev diagnostic'))
    vim.keymap.set('n', ']', api.node.navigate.diagnostics.next, opts('Next diagnostic'))
    vim.keymap.set('n', 'B', api.tree.toggle_no_buffer_filter, opts('Toggle opened'))
    vim.keymap.set('n', 'H', api.tree.toggle_hidden_filter, opts('Toggle dotfiles'))
    vim.keymap.set('n', 'I', api.tree.toggle_gitignore_filter, opts('Toggle gitignore'))
    vim.keymap.set('n', 'q', api.tree.close, opts('Close'))
    vim.keymap.set('n', 'R', api.tree.reload, opts('Refresh'))
    vim.keymap.set('n', 'gy', api.fs.copy.absolute_path, opts('Copy absolute path'))
    vim.keymap.set('n', 'y', api.fs.copy.filename, opts('Copy name'))
    vim.keymap.set('n', 'Y', api.fs.copy.relative_path, opts('Copy relative path'))
    vim.keymap.set('n', 'g?', api.tree.toggle_help, opts('Help'))

    -- add custom
    vim.keymap.set('n', '<leader>t', '<C-W>l', opts 'Unfocus tree')
end
require("nvim-tree").setup({
    on_attach = on_attach_nvim_tree,
    renderer = {
        icons = {
            glyphs = {
                bookmark = "-",
                git = {
                    unstaged = "M",
                    staged = "✓",
                    unmerged = "",
                    renamed = "R",
                    untracked = "U",
                    deleted = "D",
                    ignored = "i",
                },
            }
        }
    },
    diagnostics = {
        enable = true,
        show_on_dirs = true,
        icons = {
            hint = "H",
            info = "I",
            warning = "W",
            error = "E",
        }
    }
})
