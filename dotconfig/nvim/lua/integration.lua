-- integration options

-- defaults, will be overridden when updating config
local defaults = {
    -- Git integration in nvim-tree (slow on some systems)
    git = true
}

-- overrides here won't be removed on merge
-- @keep-start
local overrides = {
}
-- @keep-end

return vim.tbl_extend("force", defaults, overrides)
