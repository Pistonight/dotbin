require('lualine').setup({
    options = {
        theme = 'vscode',
        disabled_filetypes = {
            'packer',
            'NvimTree',
            'undotree',
        },
    },
    sections = {
        lualine_b = {
            'branch',
            'diff',
            {
                'diagnostics',
                colored = true,
                symbols = {
                    error = 'E',
                    warn = 'W',
                    hint = 'H',
                    info = 'I',
                }
            }
        }
    }
})
