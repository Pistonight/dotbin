-- This file executes when a jdtls plugin loads

-- JDTLS Environment Variables
--
-- TODO: make this better
--
--   ECLIPSE_JDTLS_HOME: path to jdtls installation
--   ECLIPSE_JDK_HOME: path to JDK used to launch eclipse jdtls
--
--   It uses JDK<version>_HOME to locate the JDK to use. For example, JDK8_HOME
local eclipse_jdtls_home = vim.env.ECLIPSE_JDTLS_HOME
if eclipse_jdtls_home == nil then
    print("ECLIPSE_JDTLS_HOME not set. Not starting Java language server")
    return
end
local nvim_config_path = vim.fn.stdpath('config')
local project_name = vim.fn.fnamemodify(vim.fn.getcwd(), ':p:h:t')

local python_path = vim.fn.exepath('python')

local config = {
    cmd = {
        python_path,
        nvim_config_path .. '/lua/lsp-wrapper/jdtls_wrapper.py',
        vim.env.ECLIPSE_JDK_HOME .. '/bin/java',
        eclipse_jdtls_home,
        project_name
    },
    root_dir = require('jdtls.setup').find_root({'.git', 'mvnw', 'gradlew'}),
    settings = {
        java = {
            import = {
                gradle = { enabled = false },
                maven = { enabled = false },
                exclusions = {}
            },
            format = {
                settings = {
                    url = 'https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml',
                    profile = "GoogleStyle",
                }
            },
            signatureHelp = { enabled = true },
            contentProvider = { preferred = 'fernflower' },
            -- Specify any options for organizing imports
            sources = {
                organizeImports = {
                    starThreshold = 9999;
                    staticStarThreshold = 9999;
                },
            },
            codeGeneration = {
                useBlock = true,
            },
            configuration = {
                runtimes = {
                    {
                        name = "JavaSE-1.8",
                        path = vim.env.JDK8_HOME,
                    },
                    {
                        name = "JavaSE-17",
                        path = vim.env.JDK17_HOME,
                    },
                    {
                        name = "JavaSE-21",
                        path = vim.env.JDK21_HOME,
                    },
                }
            }
        }
    }
}
require('jdtls').start_or_attach(config)
-- jdtls specific key maps
vim.keymap.set('n', '<leader>O', function()
    require('jdtls').organize_imports()
end)
