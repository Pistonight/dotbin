local mark = require('harpoon.mark')
vim.keymap.set('n', '<leader>A', mark.add_file, { noremap = true })

local ui = require('harpoon.ui')
vim.keymap.set('n', '<leader>s', ui.toggle_quick_menu, { noremap = true })

-- quick switch
vim.keymap.set('n', '<leader>1', function() ui.nav_file(1) end, { noremap = true })
vim.keymap.set('n', '<leader>2', function() ui.nav_file(2) end, { noremap = true })
vim.keymap.set('n', '<leader>3', function() ui.nav_file(3) end, { noremap = true })

