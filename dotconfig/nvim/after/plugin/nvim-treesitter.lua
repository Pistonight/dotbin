local integration = require("integration")

require('nvim-treesitter.configs').setup({
    ensure_installed = { },
    auto_install = integration.ts_auto_install,
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
