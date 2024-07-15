-- Dev
-- Things you actively use for coding.

--    Sections:
--       ## SNIPPETS
--       -> luasnip                        [snippet engine]
--       -> friendly-snippets              [snippet templates]

--       ## GIT
--       -> gitsigns.nvim                  [git hunks]
--       -> fugitive.vim                   [git commands]

--       ## ANALYZER
--       -> aerial.nvim                    [symbols tree]
--       -> litee-calltree.nvim            [calltree]

--       ## CODE DOCUMENTATION
--       -> dooku.nvim                     [html doc generator]
--       -> markdown-preview.nvim          [markdown previewer]
--       -> markmap.nvim                   [markdown mindmap]

--       ## ARTIFICIAL INTELLIGENCE
--       -> neural                         [chatgpt code generator]
--       -> copilot                        [github code suggestions]

--       ## DEBUGGER
--       -> nvim-dap                       [debugger]

--       ## TESTING
--       -> neotest.nvim                   [unit testing]
--       -> nvim-coverage                  [code coverage]

--       ## LANGUAGE IMPROVEMENTS
--       -> guttentags_plus                [auto generate C/C++ tags]

local is_windows = vim.fn.has('win32') == 1 -- true if on windows

return {
  --  SNIPPETS ----------------------------------------------------------------
  --  Vim Snippets engine  [snippet engine] + [snippet templates]
  --  https://github.com/L3MON4D3/LuaSnip
  --  https://github.com/rafamadriz/friendly-snippets
  {
    "L3MON4D3/LuaSnip",
    build = not is_windows and "make install_jsregexp" or nil,
    dependencies = {
      "rafamadriz/friendly-snippets",
      "zeioth/NormalSnippets",
      "benfowler/telescope-luasnip.nvim",
    },
    event = "User BaseFile",
    opts = {
      history = true,
      delete_check_events = "TextChanged",
      region_check_events = "CursorMoved",
    },
    config = function(_, opts)
      if opts then require("luasnip").config.setup(opts) end
      vim.tbl_map(
        function(type) require("luasnip.loaders.from_" .. type).lazy_load() end,
        { "vscode", "snipmate", "lua" }
      )
      -- friendly-snippets - enable standardized comments snippets
      require("luasnip").filetype_extend("typescript", { "tsdoc" })
      require("luasnip").filetype_extend("javascript", { "jsdoc" })
      require("luasnip").filetype_extend("lua", { "luadoc" })
      require("luasnip").filetype_extend("python", { "pydoc" })
      require("luasnip").filetype_extend("rust", { "rustdoc" })
      require("luasnip").filetype_extend("cs", { "csharpdoc" })
      require("luasnip").filetype_extend("java", { "javadoc" })
      require("luasnip").filetype_extend("c", { "cdoc" })
      require("luasnip").filetype_extend("cpp", { "cppdoc" })
      require("luasnip").filetype_extend("php", { "phpdoc" })
      require("luasnip").filetype_extend("kotlin", { "kdoc" })
      require("luasnip").filetype_extend("ruby", { "rdoc" })
      require("luasnip").filetype_extend("sh", { "shelldoc" })
    end,
  },

  --  GIT ---------------------------------------------------------------------
  --  Git signs [git hunks]
  --  https://github.com/lewis6991/gitsigns.nvim
  {
    "lewis6991/gitsigns.nvim",
    enabled = vim.fn.executable "git" == 1,
    event = "User BaseGitFile",
    opts = function()
      local get_icon = require("base.utils").get_icon
      return {
        max_file_length = vim.g.big_file.lines,
        signs = {
          add = { text = get_icon("GitSign") },
          change = { text = get_icon("GitSign") },
          delete = { text = get_icon("GitSign") },
          topdelete = { text = get_icon("GitSign") },
          changedelete = { text = get_icon("GitSign") },
          untracked = { text = get_icon("GitSign") },
        },
      }
    end
  },

  --  Git fugitive mergetool + [git commands]
  --  https://github.com/lewis6991/gitsigns.nvim
  --  PR needed: Setup keymappings to move quickly when using this feature.
  --
  --  We only want this plugin to use it as mergetool like "git mergetool".
  --  To enable this feature, add this  to your global .gitconfig:
  --
  --  [mergetool "fugitive"]
  --  	cmd = nvim -c \"Gvdiffsplit!\" \"$MERGED\"
  --  [merge]
  --  	tool = fugitive
  --  [mergetool]
  --  	keepBackup = false
  {
    "tpope/vim-fugitive",
    enabled = vim.fn.executable "git" == 1,
    dependencies = { "tpope/vim-rhubarb" },
    cmd = {
      "Gvdiffsplit",
      "Gdiffsplit",
      "Gedit",
      "Gsplit",
      "Gread",
      "Gwrite",
      "Ggrep",
      "GMove",
      "GRename",
      "GDelete",
      "GRemove",
      "GBrowse",
      "Git",
      "Gstatus",
    },
    config = function()
      -- NOTE: On vimplugins we use config instead of opts.
      vim.g.fugitive_no_maps = 1
    end,
  },

  --  ANALYZER ----------------------------------------------------------------
  --  [symbols tree]
  --  https://github.com/stevearc/aerial.nvim
  {
    "stevearc/aerial.nvim",
    event = "User BaseFile",
    opts = {
      filter_kind = { -- Symbols that will appear on the tree
        -- "Class",
        "Constructor",
        "Enum",
        "Function",
        "Interface",
        -- "Module",
        "Method",
        -- "Struct",
      },
      open_automatic = false, -- Open if the buffer is compatible
      autojump = true,
      link_folds_to_tree = false,
      link_tree_to_folds = false,
      attach_mode = "global",
      backends = { "lsp", "treesitter", "markdown", "man" },
      disable_max_lines = vim.g.big_file.lines,
      disable_max_size = vim.g.big_file.size,
      layout = {
        min_width = 28,
        default_direction = "right",
        placement = "edge",
      },
      show_guides = true,
      guides = {
        mid_item = "├ ",
        last_item = "└ ",
        nested_top = "│ ",
        whitespace = "  ",
      },
      keymaps = {
        ["[y"] = "actions.prev",
        ["]y"] = "actions.next",
        ["[Y"] = "actions.prev_up",
        ["]Y"] = "actions.next_up",
        ["{"] = false,
        ["}"] = false,
        ["[["] = false,
        ["]]"] = false,
      },
    },
    config = function(_, opts)
      require("aerial").setup(opts)
      -- HACK: The first time you open aerial on a session, close all folds.
      vim.api.nvim_create_autocmd({"FileType", "BufEnter"}, {
        desc = "Aerial: When aerial is opened, close all its folds.",
        callback = function()
          local is_aerial = vim.bo.filetype == "aerial"
          local is_ufo_available = require("base.utils").is_available("nvim-ufo")
          if is_ufo_available and is_aerial and vim.b.new_aerial_session == nil then
            vim.b.new_aerial_session = false
            require("aerial").tree_set_collapse_level(0, 0)
          end
        end,
      })
    end
  },

  -- Litee calltree [calltree]
  -- https://github.com/ldelossa/litee.nvim
  -- https://github.com/ldelossa/litee-calltree.nvim
  -- press ? inside the panel to show help.
  {
    'ldelossa/litee.nvim',
    event = "User BaseFile",
    opts = {
      notify = { enabled = false },
      panel = {
          orientation = "bottom",
          panel_size = 10,
      },
    },
    config = function(_, opts)
      require('litee.lib').setup(opts)
    end
  },
  {
    'ldelossa/litee-calltree.nvim',
    dependencies = 'ldelossa/litee.nvim',
    event = "User BaseFile",
    opts = {
      on_open = "panel", -- or popout
      map_resize_keys = false,
      keymaps = {
        expand = "<CR>",
        collapse = "c",
        collapse_all = "C",
        jump = "<C-CR>"
      },
    },
    config = function(_, opts)
      require('litee.calltree').setup(opts)

      -- Highlight only while on calltree
      vim.api.nvim_create_autocmd({ "WinEnter" }, {
        desc = "Clear highlights when leaving calltree + UX improvements.",
        callback = function()
          vim.defer_fn(function()
            if vim.bo.filetype == "calltree" then
              vim.wo.colorcolumn = "0"
              vim.wo.foldcolumn = "0"
              vim.cmd("silent! PinBuffer") -- stickybuf.nvim
              vim.cmd("silent! hi LTSymbolJump ctermfg=015 ctermbg=110 cterm=italic,bold,underline guifg=#464646 guibg=#87afd7 gui=italic,bold")
              vim.cmd("silent! hi LTSymbolJumpRefs ctermfg=015 ctermbg=110 cterm=italic,bold,underline guifg=#464646 guibg=#87afd7 gui=italic,bold")
            else
              vim.cmd("silent! highlight clear LTSymbolJump")
              vim.cmd("silent! highlight clear LTSymbolJumpRefs")
            end
          end, 100)
        end
      })
    end
  },

  --  CODE DOCUMENTATION ------------------------------------------------------
  --  dooku.nvim [html doc generator]
  --  https://github.com/zeioth/dooku.nvim
  {
    "zeioth/dooku.nvim",
    cmd = {
      "DookuGenerate",
      "DookuOpen",
      "DookuAutoSetup"
    },
    opts = {},
  },

  --  [markdown previewer]
  --  https://github.com/iamcco/markdown-preview.nvim
  --  Note: If you change the build command, wipe ~/.local/data/nvim/lazy
  {
    "iamcco/markdown-preview.nvim",
    build = function() vim.fn["mkdp#util#install"]() end,
    ft = { "markdown" },
    cmd = {
      "MarkdownPreview",
      "MarkdownPreviewStop",
      "MarkdownPreviewToggle",
    },
  },

  --  [markdown markmap]
  --  https://github.com/zeioth/markmap.nvim
  --  Important: Make sure you have yarn in your PATH before running markmap.
  {
    "zeioth/markmap.nvim",
    build = "yarn global add markmap-cli",
    cmd = { "MarkmapOpen", "MarkmapSave", "MarkmapWatch", "MarkmapWatchStop" },
    config = function(_, opts) require("markmap").setup(opts) end,
  },

  --  ARTIFICIAL INTELLIGENCE  -------------------------------------------------
  --  neural [chatgpt code generator]
  --  https://github.com/dense-analysis/neural
  --
  --  NOTE: In order for this plugin to work, you will have to set
  --        the next env var in your OS:
  --        OPENAI_API_KEY="my_key_here"
  {
    "dense-analysis/neural",
    cmd = { "Neural" },
    config = function()
      require("neural").setup {
        source = {
          openai = {
            api_key = vim.env.OPENAI_API_KEY,
          },
        },
        ui = {
          prompt_icon = ">",
        },
      }
    end,
  },

  --  copilot [github code suggestions]
  --  https://github.com/github/copilot.vim
  --  As alternative to chatgpt, you can use copilot uncommenting this.
  --  Then you must run :Copilot setup
  -- {
  --   "github/copilot.vim",
  --   event = "User BaseFile"
  -- },
  -- copilot-cmp
  -- https://github.com/zbirenbaum/copilot-cmp
  -- {
  --   "zbirenbaum/copilot-cmp",
  --   opts = { suggesion = { enabled = false }, panel = { enabled = false } },
  --   config = function (_, opts) require("copilot_cmp").setup(opts) end
  -- },

  --  DEBUGGER ----------------------------------------------------------------
  --  Debugger alternative to vim-inspector [debugger]
  --  https://github.com/mfussenegger/nvim-dap
  --  Here we configure the adapter+config of every debugger.
  --  Debuggers don't have system dependencies, you just install them with mason.
  --  We currently ship most of them with nvim.
  {
    "mfussenegger/nvim-dap",
    enabled = vim.fn.has "win32" == 0,
    event = "User BaseFile",
    config = function()
      local dap = require("dap")

      -- C#
      dap.adapters.coreclr = {
        type = 'executable',
        command = vim.fn.stdpath('data') .. '/mason/bin/netcoredbg',
        args = { '--interpreter=vscode' }
      }
      dap.configurations.cs = {
        {
          type = "coreclr",
          name = "launch - netcoredbg",
          request = "launch",
          program = function() -- Ask the user what executable wants to debug
            return vim.fn.input('Path to dll: ', vim.fn.getcwd() .. '/bin/Program.exe', 'file')
          end,
        },
      }

      -- F#
      dap.configurations.fsharp = dap.configurations.cs

      -- Visual basic dotnet
      dap.configurations.vb = dap.configurations.cs

      -- Java
      -- Note: The java debugger jdtls is automatically spawned and configured
      -- by the plugin 'nvim-java' in './3-dev-core.lua'.

      -- Python
      dap.adapters.python = {
        type = 'executable',
        command = vim.fn.stdpath('data') .. '/mason/packages/debugpy/venv/bin/python',
        args = { '-m', 'debugpy.adapter' },
      }
      dap.configurations.python = {
        {
          type = "python",
          request = "launch",
          name = "Launch file",
          program = "${file}", -- This configuration will launch the current file if used.
        },
      }

      -- Lua
      dap.adapters.nlua = function(callback, config)
        callback({ type = 'server', host = config.host or "127.0.0.1", port = config.port or 8086 })
      end
      dap.configurations.lua = {
        {
          type = 'nlua',
          request = 'attach',
          name = "Attach to running Neovim instance",
          program = function() pcall(require "osv".launch({ port = 8086 })) end,
        }
      }

      -- C
      dap.adapters.codelldb = {
        type = 'server',
        port = "${port}",
        executable = {
          command = vim.fn.stdpath('data') .. '/mason/bin/codelldb',
          args = { "--port", "${port}" },
          detached = function() if is_windows then return false else return true end end,
        }
      }
      dap.configurations.c = {
        {
          name = 'Launch',
          type = 'codelldb',
          request = 'launch',
          program = function() -- Ask the user what executable wants to debug
            return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/bin/program', 'file')
          end,
          cwd = '${workspaceFolder}',
          stopOnEntry = false,
          args = {},
        },
      }

      -- C++
      dap.configurations.cpp = dap.configurations.c

      -- Rust
      dap.configurations.rust = {
        {
          name = 'Launch',
          type = 'codelldb',
          request = 'launch',
          program = function() -- Ask the user what executable wants to debug
            return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/bin/program', 'file')
          end,
          cwd = '${workspaceFolder}',
          stopOnEntry = false,
          args = {},
          initCommands = function() -- add rust types support (optional)
            -- Find out where to look for the pretty printer Python module
            local rustc_sysroot = vim.fn.trim(vim.fn.system('rustc --print sysroot'))

            local script_import = 'command script import "' .. rustc_sysroot .. '/lib/rustlib/etc/lldb_lookup.py"'
            local commands_file = rustc_sysroot .. '/lib/rustlib/etc/lldb_commands'

            local commands = {}
            local file = io.open(commands_file, 'r')
            if file then
              for line in file:lines() do
                table.insert(commands, line)
              end
              file:close()
            end
            table.insert(commands, 1, script_import)

            return commands
          end,
        }
      }

      -- Go
      -- Requires:
      -- * You have initialized your module with 'go mod init module_name'.
      -- * You :cd your project before running DAP.
      dap.adapters.delve = {
        type = 'server',
        port = '${port}',
        executable = {
          command = vim.fn.stdpath('data') .. '/mason/packages/delve/dlv',
          args = { 'dap', '-l', '127.0.0.1:${port}' },
        }
      }
      dap.configurations.go = {
        {
          type = "delve",
          name = "Compile module and debug this file",
          request = "launch",
          program = "./${relativeFileDirname}",
        },
        {
          type = "delve",
          name = "Compile module and debug this file (test)",
          request = "launch",
          mode = "test",
          program = "./${relativeFileDirname}"
        },
      }

      -- Dart / Flutter
      dap.adapters.dart = {
        type = 'executable',
        command = vim.fn.stdpath('data') .. '/mason/bin/dart-debug-adapter',
        args = { 'dart' }
      }
      dap.adapters.flutter = {
        type = 'executable',
        command = vim.fn.stdpath('data') .. '/mason/bin/dart-debug-adapter',
        args = { 'flutter' }
      }
      dap.configurations.dart = {
        {
          type = "dart",
          request = "launch",
          name = "Launch dart",
          dartSdkPath = "/opt/flutter/bin/cache/dart-sdk/", -- ensure this is correct
          flutterSdkPath = "/opt/flutter",                  -- ensure this is correct
          program = "${workspaceFolder}/lib/main.dart",     -- ensure this is correct
          cwd = "${workspaceFolder}",
        },
        {
          type = "flutter",
          request = "launch",
          name = "Launch flutter",
          dartSdkPath = "/opt/flutter/bin/cache/dart-sdk/", -- ensure this is correct
          flutterSdkPath = "/opt/flutter",                  -- ensure this is correct
          program = "${workspaceFolder}/lib/main.dart",     -- ensure this is correct
          cwd = "${workspaceFolder}",
        }
      }

      -- Kotlin
      -- Kotlin projects have very weak project structure conventions.
      -- You must manually specify what the project root and main class are.
      dap.adapters.kotlin = {
        type = 'executable',
        command = vim.fn.stdpath('data') .. '/mason/bin/kotlin-debug-adapter',
      }
      dap.configurations.kotlin = {
        {
          type = 'kotlin',
          request = 'launch',
          name = 'Launch kotlin program',
          projectRoot = "${workspaceFolder}/app",     -- ensure this is correct
          mainClass = "AppKt",                        -- ensure this is correct
        },
      }

      -- Javascript / Typescript (firefox)
      dap.adapters.firefox = {
        type = 'executable',
        command = vim.fn.stdpath('data') .. '/mason/bin/firefox-debug-adapter',
      }
      dap.configurations.typescript = {
        {
          name = 'Debug with Firefox',
          type = 'firefox',
          request = 'launch',
          reAttach = true,
          url = 'http://localhost:4200', -- Write the actual URL of your project.
          webRoot = '${workspaceFolder}',
          firefoxExecutable = '/usr/bin/firefox'
        }
      }
      dap.configurations.javascript = dap.configurations.typescript
      dap.configurations.javascriptreact = dap.configurations.typescript
      dap.configurations.typescriptreact = dap.configurations.typescript

      -- Javascript / Typescript (chromium)
      -- If you prefer to use this adapter, comment the firefox one.
      -- But to use this adapter, you must manually run one of these two, first:
      -- * chromium --remote-debugging-port=9222 --user-data-dir=remote-profile
      -- * google-chrome-stable --remote-debugging-port=9222 --user-data-dir=remote-profile
      -- After starting the debugger, you must manually reload page to get all features.
      -- dap.adapters.chrome = {
      --  type = 'executable',
      --  command = vim.fn.stdpath('data')..'/mason/bin/chrome-debug-adapter',
      -- }
      -- dap.configurations.typescript = {
      --  {
      --   name = 'Debug with Chromium',
      --   type = "chrome",
      --   request = "attach",
      --   program = "${file}",
      --   cwd = vim.fn.getcwd(),
      --   sourceMaps = true,
      --   protocol = "inspector",
      --   port = 9222,
      --   webRoot = "${workspaceFolder}"
      --  }
      -- }
      -- dap.configurations.javascript = dap.configurations.typescript
      -- dap.configurations.javascriptreact = dap.configurations.typescript
      -- dap.configurations.typescriptreact = dap.configurations.typescript

      -- PHP
      dap.adapters.php = {
        type = 'executable',
        command = vim.fn.stdpath("data") .. '/mason/bin/php-debug-adapter',
      }
      dap.configurations.php = {
        {
          type = 'php',
          request = 'launch',
          name = 'Listen for Xdebug',
          port = 9000
        }
      }

      -- Shell
      dap.adapters.bashdb = {
        type = 'executable',
        command = vim.fn.stdpath("data") .. '/mason/packages/bash-debug-adapter/bash-debug-adapter',
        name = 'bashdb',
      }
      dap.configurations.sh = {
        {
          type = 'bashdb',
          request = 'launch',
          name = "Launch file",
          showDebugOutput = true,
          pathBashdb = vim.fn.stdpath("data") .. '/mason/packages/bash-debug-adapter/extension/bashdb_dir/bashdb',
          pathBashdbLib = vim.fn.stdpath("data") .. '/mason/packages/bash-debug-adapter/extension/bashdb_dir',
          trace = true,
          file = "${file}",
          program = "${file}",
          cwd = '${workspaceFolder}',
          pathCat = "cat",
          pathBash = "/bin/bash",
          pathMkfifo = "mkfifo",
          pathPkill = "pkill",
          args = {},
          env = {},
          terminalKind = "integrated",
        }
      }

      -- Elixir
      dap.adapters.mix_task = {
        type = 'executable',
        command = vim.fn.stdpath("data") .. '/mason/bin/elixir-ls-debugger',
        args = {}
      }
      dap.configurations.elixir = {
        {
          type = "mix_task",
          name = "mix test",
          task = 'test',
          taskArgs = { "--trace" },
          request = "launch",
          startApps = true, -- for Phoenix projects
          projectDir = "${workspaceFolder}",
          requireFiles = {
            "test/**/test_helper.exs",
            "test/**/*_test.exs"
          }
        },
      }
    end, -- of dap config
    dependencies = {
      "rcarriga/nvim-dap-ui",
      "rcarriga/cmp-dap",
      "jay-babu/mason-nvim-dap.nvim",
      "jbyuki/one-small-step-for-vimkind",
      "nvim-java/nvim-java",
    },
  },

  -- nvim-dap-ui [dap ui]
  -- https://github.com/mfussenegger/nvim-dap-ui
  -- user interface for the debugger dap
  {
    "rcarriga/nvim-dap-ui",
    dependencies = { "nvim-neotest/nvim-nio" },
    opts = { floating = { border = "rounded" } },
    config = function(_, opts)
      local dap, dapui = require("dap"), require("dapui")
      dap.listeners.after.event_initialized["dapui_config"] = function(
      )
        dapui.open()
      end
      dap.listeners.before.event_terminated["dapui_config"] = function(
      )
        dapui.close()
      end
      dap.listeners.before.event_exited["dapui_config"] = function()
        dapui.close()
      end
      dapui.setup(opts)
    end,
  },

  -- cmp-dap [dap autocomplete]
  -- https://github.com/mfussenegger/cmp-dap
  -- Enables autocomplete for the debugger dap.
  {
    "rcarriga/cmp-dap",
    dependencies = { "nvim-cmp" },
    config = function()
      require("cmp").setup.filetype(
        { "dap-repl", "dapui_watches", "dapui_hover" },
        {
          sources = {
            { name = "dap" },
          },
        }
      )
    end,
  },

  {
     "dhananjaylatkar/cscope_maps.nvim",
     dependencies = {
        "folke/which-key.nvim", -- optional [for whichkey hints]
        "nvim-telescope/telescope.nvim", -- optional [for picker="telescope"]
        "ibhagwan/fzf-lua", -- optional [for picker="fzf-lua"]
        "nvim-tree/nvim-web-devicons", -- optional [for devicons in telescope or fzf]
     },
     opts = {
        -- USE EMPTY FOR DEFAULT OPTIONS
        -- DEFAULTS ARE LISTED BELOW
     },
  },

} -- end of return
