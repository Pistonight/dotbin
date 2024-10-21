-- only required if packer is `opt`
vim.cmd [[packadd packer.nvim ]]

return require("packer").startup(function(use)
    -- plugin manager
    use "wbthomason/packer.nvim"
    -- copilot
    use 'github/copilot.vim'
    -- vscode-ize
    use 'Mofiqul/vscode.nvim'         -- color scheme
    use 'nvim-tree/nvim-tree.lua'     -- file tree
    use 'nvim-tree/nvim-web-devicons' -- icons
    use 'nvim-lualine/lualine.nvim'   -- status line
    -- tree sitter parser
    use 'nvim-treesitter/nvim-treesitter'
    use 'nvim-treesitter/nvim-treesitter-context'
    use 'IndianBoy42/tree-sitter-just'
    -- telescope fuzzy finder
    use 'nvim-telescope/telescope.nvim'
    use 'nvim-telescope/telescope-ui-select.nvim'
    use 'nvim-lua/plenary.nvim' -- useful stuff (required by telescope)
    -- useful plugins
    use 'mbbill/undotree'
    use 'terrortylor/nvim-comment'
    use 'voldikss/vim-floaterm'
    use 'ThePrimeagen/harpoon'
    use 'lukas-reineke/indent-blankline.nvim'
    -- lsp zero
    use {
        'VonHeikemen/lsp-zero.nvim',
        branch = 'v2.x',
        requires = {
            -- lsp support
            { 'neovim/nvim-lspconfig' },
            -- mason is a lsp auto-installer/manager, optional but REALLY good
            {
                'williamboman/mason.nvim',
                run = function()
                    pcall(vim.cmd, 'MasonUpdate')
                end,
            },
            { 'williamboman/mason-lspconfig.nvim' },
            -- required autocompletion plugins
            { 'hrsh7th/nvim-cmp' },
            { 'hrsh7th/cmp-nvim-lsp' },
            { 'L3MON4D3/LuaSnip' },
        }
    }
    -- jdtls needs this for full suport
    use 'mfussenegger/nvim-jdtls'
    -- other completion plugins
    use 'hrsh7th/cmp-path'
    use 'hrsh7th/cmp-buffer'
    use 'hrsh7th/cmp-nvim-lsp-signature-help'
    use 'hrsh7th/cmp-nvim-lua'
    -- inlay hints
    use 'lvimuser/lsp-inlayhints.nvim'
    -- git
    use 'tpope/vim-fugitive'
end)
