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
          require("codecompanion").setup({
              adapters = {
                  openai_compatible = function()
                      return require("codecompanion.adapters").extend("openai_compatible", {
                          url = "http://ted-cat-avery:4000/v1/chat/completions",
                          env = {
                              url = "http://ted-cat-avery:4000",
                              api_key = "OPENAI_API_KEY",
                          },
                          schema = {
                              model = { default = "premium", },
                              num_ctx = { default = 16384, },
                              num_predict = { default = -1, },
                          },
                      })
                  end,
                  ollama = function()
                      return require("codecompanion.adapters").extend("ollama", {
                          env = {
                              url = "http://Mac:11434",
                          },
                          schema = {
                              model = {
                                  -- default = "r1-1776:70b-distill-llama-q8_0",
                                  -- default = "deepseek-r1:32b-qwen-distill-fp16",
                                  -- default = "deepseek-coder-v2:16b-lite-instruct-fp16",
                                  default = "qwen3:32b-fp16",
                              },
                              num_ctx = {
                                  default = 32768,
                              },
                          },
                      })
                  end,
                  my_openai = function()
                      return require("codecompanion.adapters").extend("openai_compatible", {
                          env = {
                              url = "http://ted-cat-avery:4000", -- optional: default value is ollama url http://127.0.0.1:11434
                              api_key = "OpenAI_API_KEY", -- optional: if your endpoint is authenticated
                              chat_url = "/v1/chat/completions", -- optional: default value, override if different
                              models_endpoint = "/v1/models", -- optional: attaches to the end of the URL to form the endpoint to retrieve models
                          },
                          schema = {
                              model = {
                                  default = "premium",  -- define llm model to be used
                              },
                              temperature = {
                                  order = 2,
                                  mapping = "parameters",
                                  type = "number",
                                  optional = true,
                                  default = 0.8,
                                  desc = "What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.",
                                  validate = function(n)
                                      return n >= 0 and n <= 2, "Must be between 0 and 2"
                                  end,
                              },
                              max_completion_tokens = {
                                  order = 3,
                                  mapping = "parameters",
                                  type = "integer",
                                  optional = true,
                                  default = nil,
                                  desc = "An upper bound for the number of tokens that can be generated for a completion.",
                                  validate = function(n)
                                      return n > 0, "Must be greater than 0"
                                  end,
                              },
                              stop = {
                                  order = 4,
                                  mapping = "parameters",
                                  type = "string",
                                  optional = true,
                                  default = nil,
                                  desc = "Sets the stop sequences to use. When this pattern is encountered the LLM will stop generating text and return. Multiple stop patterns may be set by specifying multiple separate stop parameters in a modelfile.",
                                  validate = function(s)
                                      return s:len() > 0, "Cannot be an empty string"
                                  end,
                              },
                              logit_bias = {
                                  order = 5,
                                  mapping = "parameters",
                                  type = "map",
                                  optional = true,
                                  default = nil,
                                  desc = "Modify the likelihood of specified tokens appearing in the completion. Maps tokens (specified by their token ID) to an associated bias value from -100 to 100. Use https://platform.openai.com/tokenizer to find token IDs.",
                                  subtype_key = {
                                      type = "integer",
                                  },
                                  subtype = {
                                      type = "integer",
                                      validate = function(n)
                                          return n >= -100 and n <= 100, "Must be between -100 and 100"
                                      end,
                                  },
                              },
                          },
                      })
                  end,
              },
              strategies = {
                  chat = { adapter = "ollama", },
                  -- chat = { adapter = "openai_compatible", },
                  inline = { adapter = "ollama", },
                  -- inline = { adapter = "openai_compatible", },
                  agent = { adapter = "ollama", },
                  -- agent = { adapter = "openai_compatible", },
              },
              opts = {
                  log_level = 'DEBUG', -- TRACE|DEBUG|ERROR|INFO
                  -- If this is false then any default prompt that is marked as containing code
                  -- will not be sent to the LLM. Please note that whilst I have made every
                  -- effort to ensure no code leakage, using this is at your own risk
                  send_code = true,
                  use_default_actions = true, -- Show the default actions in the action palette?
                  use_default_prompts = true, -- Show the default prompts in the action palette?
              },
          })
      end,
  },

  {
    "yetone/avante.nvim",
    enabled = false,
    event = "VeryLazy",
    lazy = false,
    version = false, -- set this if you want to always pull the latest change
    opts = {
      provider = "ollama",
      vendors = {
        ---@type AvanteProvider
        ollama = {
          ["local"] = true,
--        endpoint = "http://ted-cat-avery:4000/v1",
          endpoint = "http://Mac:11434/v1",
          model = "deepseek-coder-v2:16b-lite-instruct-fp16",
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
        db_build_cmd = {args = {"-bR"}},
        -- cscope executable
        exec = "cscope", -- "cscope" or "gtags-cscope"
        -- choose your fav picker
        picker = "telescope", -- "quickfix", "telescope", "fzf-lua" or "mini-pick"
      },
    },
  },
} -- end of return
