local frappe = require("catppuccin.palettes").get_palette("frappe")
local mocha = require("catppuccin.palettes").get_palette("mocha")

require("catppuccin").setup({
    flavour = "auto", -- latte, frappe, macchiato, mocha
    background = { -- :h background
        light = "latte",
        dark = "mocha",
    },
    transparent_background = false, -- disables setting the background color.
    show_end_of_buffer = false, -- shows the '~' characters after the end of buffers
    term_colors = true, -- sets terminal colors (e.g. `g:terminal_color_0`)
    dim_inactive = {
        enabled = false, -- dims the background color of inactive window
        shade = "dark",
        percentage = 0.15, -- percentage of the shade to apply to the inactive window
    },
    no_italic = false, -- Force no italic
    no_bold = false, -- Force no bold
    no_underline = false, -- Force no underline
    styles = { -- Handles the styles of general hi groups (see `:h highlight-args`):
        comments = { "italic" },
        conditionals = {},
        loops = {},
        functions = {},
        keywords = {},
        strings = {},
        variables = {},
        numbers = {},
        booleans = {},
        properties = {},
        types = {},
        operators = {},
        miscs = {},
    },
    color_overrides = {},
    custom_highlights = function()
        return {
            -- make line numbers easier to read
            LineNr = { fg = mocha.overlay2 },

            -- functions
            Function = { fg = mocha.yellow },
            ["@function.builtin"] = { link = "Function" },

            -- macros
            Macro = { fg = mocha.peach },
            ["@function.macro"] = { link = "Macro" },
            ["@lsp.typemod.macro"] = { link = "Macro" },
            ["@lsp.typemod.macro.defaultLibrary"] = { link = "Macro" },
            ["@lsp.typemod.macro.library"] = { link = "Macro" },

            -- types
            Type = { fg = mocha.blue },
            ["@module"] = { link = "Type" }, -- make module/namespace not blend in with variables
            ["@type.builtin"] = { link = "Type" },
            ["@type.builtin.cpp"] = { link = "Type" },
            ["@lsp.type.interface"] = {link = "Type"},

            -- punctuation
            Operator = { fg = mocha.sapphire },
            ["@punctuation.special"] = { link = "Delimiter" },
            ["@tag.delimiter"] = { link = "Delimiter" },

            -- variables
            ["@variable"] = { fg = mocha.lavender },
            ["@parameter"] = { link = "@variable" },
            ["@variable.parameter"] = { link = "@variable" },

            -- constants
            ["@lsp.typemod.variable.readonly"] = { link = "Constant" },

            -- override the terminal color to be frappe
            -- so it stands out from the editor
            Floaterm = { bg = frappe.base },
            FloatermNC = { bg = frappe.crust },
            FloatermBorder = { bg = frappe.base },
        }
    end,
    default_integrations = true,
    integrations = {
        cmp = true,
        gitsigns = true,
        nvimtree = true,
        treesitter = true,
        notify = false,
        mason = true,
        mini = {
            enabled = true,
            indentscope_color = "",
        },
        native_lsp = {
            enabled = true,
            virtual_text = {
                errors = { "italic" },
                hints = { "italic" },
                warnings = { "italic" },
                information = { "italic" },
                ok = { "italic" },
            },
            underlines = {
                errors = { "undercurl" },
                hints = { "undercurl" },
                warnings = { "undercurl" },
                information = { "underline" },
                ok = { "underline" },
            },
            inlay_hints = {
                background = true,
            },
        },
        -- For more plugins integrations please scroll down (https://github.com/catppuccin/nvim#integrations)
    },
    -- set pre-compiled path to be inside config
    compile_path = vim.fn.stdpath("config") .. "/cache/catppuccin",
})
vim.cmd.colorscheme('catppuccin')