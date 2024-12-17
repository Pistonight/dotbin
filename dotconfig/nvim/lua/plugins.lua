-- only required if packer is `opt`
vim.cmd [[packadd packer.nvim ]]

return require("packer").startup(function(use)
    use "wbthomason/packer.nvim"
    -- U: Upstream appears to be unmaintained. No need to check for updates
    -- L: Lock to this version because of an issue, put the issue link like L#123

    -- ## UI AND EDITOR FUNCTION
    use { 'nvim-tree/nvim-tree.lua',                 tag = "v1.9.0" }
    use { 'nvim-tree/nvim-web-devicons',             commit = "0eb18da56e2ba6ba24de7130a12bcc4e31ad11cb" }
    use { 'nvim-lualine/lualine.nvim',               commit = "2a5bae925481f999263d6f5ed8361baef8df4f83" }
    use { 'lukas-reineke/indent-blankline.nvim',     tag = "v3.8.6" }
    use { 'nvim-telescope/telescope.nvim',           commit = "2eca9ba22002184ac05eddbe47a7fe2d5a384dfc" }
    use { 'nvim-telescope/telescope-ui-select.nvim', commit = "6e51d7da30bd139a6950adf2a47fda6df9fa06d2" }
    use { 'nvim-lua/plenary.nvim',                   commit = "2d9b06177a975543726ce5c73fca176cedbffe9d" }
    use { 'mbbill/undotree',                         commit = "78b5241191852ffa9bb5da5ff2ee033160798c3b" }
    use { 'voldikss/vim-floaterm',                   commit = "4e28c8dd0271e10a5f55142fb6fe9b1599ee6160" }
    use { 'terrortylor/nvim-comment',                commit = "e9ac16ab056695cad6461173693069ec070d2b23" } -- U

    -- ## THEME AND COLORS
    use { "catppuccin/nvim", tag = "v1.9.0", as = "catppuccin" }
    use { 'nvim-treesitter/nvim-treesitter', run = ':TSUpdate' }
    use 'nvim-treesitter/nvim-treesitter-context'

    -- ## LANGUAGE SERVICE
    use { 'neovim/nvim-lspconfig' }
    use { 'williamboman/mason.nvim', run = ":MasonUpdate" }
    use { 'williamboman/mason-lspconfig.nvim' }
    use { 'github/copilot.vim',                      tag = "v1.14.0" }
    use { 'VonHeikemen/lsp-zero.nvim',               branch = 'v2.x' } -- U
    -- completion
    use { 'hrsh7th/nvim-cmp',
        requires = {
            { 'hrsh7th/cmp-nvim-lsp' },
            { 'hrsh7th/cmp-path' },
            { 'hrsh7th/cmp-buffer' },
            { 'hrsh7th/cmp-nvim-lsp-signature-help' },
            { 'hrsh7th/cmp-nvim-lua' }
        }
    }
    use { 'lvimuser/lsp-inlayhints.nvim',            commit = "d981f65c9ae0b6062176f0accb9c151daeda6f16", } -- U
    -- language: java (jdtls)
    use { 'mfussenegger/nvim-jdtls',                 commit = "ece818f909c6414cbad4e1fb240d87e003e10fda",
        ft = { 'java' },
        config = function () require('lsp-wrapper.jdtls') end
    }

    -- ## LOW USE: consider removing if not used
    use 'tpope/vim-fugitive'
end)
