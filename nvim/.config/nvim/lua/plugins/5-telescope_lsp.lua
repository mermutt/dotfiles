return {
  -- Telescope LSP integration
  {
    "nvim-telescope/telescope.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      local telescope = require("telescope")
      local telescope_lsp = require("base.utils.telescope_lsp")
      
      -- Setup telescope LSP mappings
      telescope_lsp.setup_telescope_lsp_mappings()
      
      -- Configure telescope for better LSP experience
      telescope.setup({
        defaults = {
          mappings = {
            i = {
              ["<C-j>"] = require("telescope.actions").move_selection_next,
              ["<C-k>"] = require("telescope.actions").move_selection_previous,
              ["<C-q>"] = require("telescope.actions").send_selected_to_qflist,
            },
          },
          file_ignore_patterns = { "node_modules", ".git" },
        },
        extensions = {
          lsp_handlers = {
            disable = {},
            location = {
              telescope = {},
              no_results_message = "No references found",
            },
            symbol = {
              telescope = {},
              no_results_message = "No symbols found",
            },
          },
        },
      })
    end,
  },
}