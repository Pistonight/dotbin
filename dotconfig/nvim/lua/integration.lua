-- integration options

-- defaults, will be overridden when updating config
local defaults = {
    -- Git integration in nvim-tree (slow on some systems)
    git = true,

    -- Automatically install languages for treesitter (TS is slow to compile on some systems)
    ts_auto_install = true,
}

-- overrides here won't be removed on merge
-- @keep-start
local overrides = {
}
-- @keep-end

return vim.tbl_extend("force", defaults, overrides)
