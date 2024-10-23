-- Dev
-- My additional plugins

--    Sections:
--       ## ARTIFICIAL INTELLIGENCE
--       -> codecompanion                  [LLM integration]
--       -> avante                         [LLM integration]

--       ## LANGUAGE IMPROVEMENTS
--       -> cscope_maps                    [/C++ tags search]

return {
 -- [codecompanion.nvim] - Integrates LLMs with neovim
  -- see: `:h codecompanion.txt`
  -- link: https://github.com/olimorris/codecompanion.nvim
  {
      'olimorris/codecompanion.nvim',
      event = 'VeryLazy',
      branch = 'main',
      dependencies = { 'nvim-lua/plenary.nvim', 'nvim-treesitter/nvim-treesitter', 'nvim-telescope/telescope.nvim', 'stevearc/dressing.nvim' },
      -- stylua: ignore
      keys = {
          { '<leader>zi', '<cmd>CodeCompanion<cr>', mode = { 'n', 'v' }, desc = 'Inline Prompt [zi]' },
          { '<leader>zz', '<cmd>CodeCompanionChat<cr>', mode = { 'n', 'v' }, desc = 'Open Chat [zz]' },
          { '<leader>zt', '<cmd>CodeCompanionToggle<cr>', mode = { 'n', 'v' }, desc = 'Toggle Chat [zt]' },
          { '<leader>za', '<cmd>CodeCompanionActions<cr>', mode = { 'n', 'v' }, desc = 'Actions [za]' },
          { '<leader>zp', '<cmd>CodeCompanionAdd<cr>', mode = { 'v' }, desc = 'Paste Selected to the Chat [zp]' },
      },
      config = function()
          require('codecompanion').setup {
              adapters = {
                  ollama = function()
                      return require('codecompanion.adapters').extend('ollama', {
                          env = {
                              url = "http://127.0.0.1:11434",
                          },
                          schema = {
                              model = {
                                  default = 'qwen2.5-coder:latest',
                                  -- default = "llama3.1:8b-instruct-q8_0",
                              },
                              num_ctx = {
                                  default = 32768,
                              },
                          },
                      })
                  end,
              },
              strategies = {
                  chat = { adapter = 'ollama', },
                  inline = { adapter = 'ollama', },
                  agent = { adapter = 'ollama', },
              },
              -- GENERAL OPTIONS ----------------------------------------------------------
              opts = {
                  log_level = 'TRACE', -- TRACE|DEBUG|ERROR|INFO
                  -- If this is false then any default prompt that is marked as containing code
                  -- will not be sent to the LLM. Please note that whilst I have made every
                  -- effort to ensure no code leakage, using this is at your own risk
                  send_code = true,
                  use_default_actions = true, -- Show the default actions in the action palette?
                  use_default_prompts = true, -- Show the default prompts in the action palette?
              },
          }
      end,
  },
  {
    "yetone/avante.nvim",
    event = "VeryLazy",
    lazy = false,
    version = false, -- set this if you want to always pull the latest change
    opts = {
      provider = "ollama",
      vendors = {
        ---@type AvanteProvider
        ollama = {
          ["local"] = true,
          endpoint = "127.0.0.1:11434/v1",
          --model = "llama3.1:8b-instruct-q8_0",
          model = "qwen2.5-coder:latest",
          parse_curl_args = function(opts, code_opts)
            return {
              url = opts.endpoint .. "/chat/completions",
              headers = {
                ["Accept"] = "application/json",
                ["Content-Type"] = "application/json",
              },
              body = {
                model = opts.model,
                messages = require("avante.providers").copilot.parse_message(code_opts), -- you can make your own message, but this is very advanced
                max_tokens = 131072,
                stream = true,
              },
            }
          end,
          parse_response_data = function(data_stream, event_state, opts)
            require("avante.providers").openai.parse_response(data_stream, event_state, opts)
          end,
        },
      },
    },
    -- if you want to build from source then do `make BUILD_FROM_SOURCE=true`
    build = "make",
    -- build = "powershell -ExecutionPolicy Bypass -File Build.ps1 -BuildFromSource false" -- for windows
    dependencies = {
      "stevearc/dressing.nvim",
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      --- The below dependencies are optional,
      "nvim-tree/nvim-web-devicons", -- or echasnovski/mini.icons
      "zbirenbaum/copilot.lua", -- for providers='copilot'
      {
        -- support for image pasting
	"HakonHarnes/img-clip.nvim",
	event = "VeryLazy",
	opts = {
	  -- recommended settings
	  default = {
	    embed_image_as_base64 = false,
	    prompt_for_file_name = false,
	    drag_and_drop = {
	      insert_mode = true,
	    },
	    -- required for Windows users
	      use_absolute_path = true,
	  },
	},
	{
	  -- Make sure to set this up properly if you have lazy=true
	  'MeanderingProgrammer/render-markdown.nvim',
	  opts = {
		  file_types = { "markdown", "Avante" },
	  },
	  ft = { "markdown", "Avante" },
	},
      },
    },
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
      skip_input_prompt = true, -- doesn't ask for input

      -- cscope related defaults
      cscope = {
        -- location of cscope db file
        db_file = "./cscope.out", -- DB or table of DBs
        -- NOTE:
        --   when table of DBs is provided -
        --   first DB is "primary" and others are "secondary"
        --   primary DB is used for build and project_rooter
        db_build_cmd_args = { "-bR" },
        -- cscope executable
        exec = "cscope", -- "cscope" or "gtags-cscope"
        -- choose your fav picker
        picker = "telescope", -- "quickfix", "telescope", "fzf-lua" or "mini-pick"
      },
    },
  },
} -- end of return
