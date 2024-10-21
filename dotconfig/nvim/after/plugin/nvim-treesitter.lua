require('nvim-treesitter.configs').setup({
    ensure_installed = { 'lua' },
    auto_install = true,
    highlight = {
        enable = true,
        additional_vim_regex_highlighting = false,
    },
    indent = { enable = true },
    rainbow = {
        enable = true,
        extended_mode = true,
        max_file_lines = nil,
    }
})
-- additional parsers
require('tree-sitter-just').setup({})
