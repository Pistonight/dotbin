local lsp = require('lsp-zero').preset({})

lsp.on_attach(function(_client, bufnr)
    lsp.default_keymaps({
        buffer = bufnr,
        omit = { 'gd', 'gr', 'gi', 'gs', '<F2>', '<F3>', '<F4>' }
    })
    vim.keymap.set('n', '<leader>r', vim.lsp.buf.rename, { buffer = bufnr })
    vim.keymap.set('n', '<leader>f', vim.lsp.buf.format, { buffer = bufnr })
    vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, { buffer = bufnr })
    vim.keymap.set('n', ']d', vim.diagnostic.goto_next, { buffer = bufnr })
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, { buffer = bufnr })
    vim.keymap.set('n', 'gt', vim.lsp.buf.type_definition, { buffer = bufnr })
    -- code action menu
    vim.keymap.set({ 'n', 'v' }, '<leader>a', vim.lsp.buf.code_action, { buffer = bufnr })

    -- signature help in input mode
    vim.keymap.set('i', '<C-h>', vim.lsp.buf.signature_help, { buffer = bufnr })
end)

-- Configure individual language servers
local lspconfig = require('lspconfig')
-- Lua LS
lspconfig.lua_ls.setup(lsp.nvim_lua_ls())

local string_to_list = function(str, delimiter)
    local list = {}
    for word in string.gmatch(str, '([^' .. delimiter .. ']+)') do
        table.insert(list, word)
    end
    return list
end

-- Rust Analyzer Environment Variables
--   LSP_RUST_ANALYZER_FEATURES: comma separated list of features to enable
--   LSP_RUST_ANALYZER_NO_DEFAULT_FEATURES: set to anything to disable default features
--   LSP_RUST_ANALYZER_EXTRA_ARGS: extra arguments to pass to cargo
local lsp_rust_analyzer_features = (function()
    local env_value = vim.env.LSP_RUST_ANALYZER_FEATURES
    if env_value == nil then
        return {}
    end
    return string_to_list(env_value, ',')
end)()
local lsp_rust_analyzer_extra_args = (function()
    local env_value = vim.env.LSP_RUST_ANALYZER_EXTRA_ARGS
    if env_value == nil then
        return {}
    end
    return string_to_list(env_value, ' ')
end)()
local lsp_rust_analyzer_no_default_features = vim.env.LSP_RUST_ANALYZER_NO_DEFAULT_FEATURES ~= nil
lspconfig.rust_analyzer.setup({
    settings = {
        ["rust-analyzer"] = {
            cargo = {
                extraArgs = lsp_rust_analyzer_extra_args,
                features = lsp_rust_analyzer_features,
                noDefaultFeatures = lsp_rust_analyzer_no_default_features,
            }
        }
    }
})

lsp.setup()

-- auto complete setup (needs to be after lsp.setup())
local cmp = require('cmp')
cmp.setup({
    -- completion menu kep mapping
    mapping = {
        -- accept completion
        ['<CR>'] = cmp.mapping.confirm({ select = false }),
        -- trigger completion
        ['<C-n>'] = cmp.mapping.complete(),
        -- abort completion
        ['<C-e>'] = cmp.mapping.abort(),
        -- nagivate
        ['<A-k>'] = cmp.mapping.select_prev_item(),
        ['<A-j>'] = cmp.mapping.select_next_item(),
    },

    -- Installed sources:
    sources = {
        { name = 'buffer',                 keyword_length = 3 }, -- source current buffer
        { name = 'path' },                     -- file paths
        { name = 'nvim_lsp',               keyword_length = 3 }, -- from language server
        { name = 'nvim_lsp_signature_help' },  -- display function signatures with current parameter emphasized
        { name = 'nvim_lua',               keyword_length = 2 }, -- complete neovim's Lua runtime API such vim.lsp.*
    },
    window = {
        completion = cmp.config.window.bordered(),
        documentation = cmp.config.window.bordered(),
    },
    formatting = {
        fields = { 'abbr', 'kind' },
    },
})
-- Set completeopt to have a better completion experience
--
-- :help completeopt
-- menuone: popup even when there's only one match
-- noinsert: Do not insert text until a selection is made
-- noselect: Do not select, force to select one from the menu
-- shortmess: avoid showing extra messages when using completion
-- updatetime: set updatetime for CursorHold
vim.opt.completeopt = { 'menuone', 'noselect', 'noinsert' }
vim.opt.shortmess = vim.opt.shortmess + { c = true }
vim.api.nvim_set_option_value('updatetime', 300, {})

-- https://github.com/neovim/neovim/issues/30985 workaround for LSP error from rust-analyzer
for _, method in ipairs({ 'textDocument/diagnostic', 'workspace/diagnostic' }) do
    local default_diagnostic_handler = vim.lsp.handlers[method]
    vim.lsp.handlers[method] = function(err, result, context, config)
        if err ~= nil then
            if err.code == -32802 then
                return
            end
            if err.code == -32603 then
                return
            end
        end

        return default_diagnostic_handler(err, result, context, config)
    end
end
