local M = {}

-- Telescope LSP mappings that integrate with your existing LSP setup
function M.setup_telescope_lsp_mappings()
  local telescope = require('telescope.builtin')
  local utils = require('base.utils')
  
  -- Check if telescope is available
  if not pcall(require, 'telescope') then
    return
  end

  -- LSP Telescope mappings
  local mappings = {
    -- References
    ['<leader>lR'] = {
      function() 
        telescope.lsp_references({
          include_declaration = false,
          show_line = false,
        })
      end,
      desc = "LSP references (telescope)"
    },
    
    -- Definitions
    ['<leader>ld'] = {
      function() telescope.lsp_definitions() end,
      desc = "LSP definitions (telescope)"
    },
    
    -- Type definitions
    ['<leader>lD'] = {
      function() telescope.lsp_type_definitions() end,
      desc = "LSP type definitions (telescope)"
    },
    
    -- Implementations
    ['<leader>li'] = {
      function() telescope.lsp_implementations() end,
      desc = "LSP implementations (telescope)"
    },
    
    -- Document symbols
    ['<leader>ls'] = {
      function() telescope.lsp_document_symbols() end,
      desc = "LSP document symbols (telescope)"
    },
    
    -- Workspace symbols
    ['<leader>lS'] = {
      function() telescope.lsp_dynamic_workspace_symbols() end,
      desc = "LSP workspace symbols (telescope)"
    },
    
    -- Diagnostics
    ['<leader>lD'] = {
      function() telescope.diagnostics({ bufnr = 0 }) end,
      desc = "Buffer diagnostics (telescope)"
    },
    
    -- Workspace diagnostics
    ['<leader>lW'] = {
      function() telescope.diagnostics() end,
      desc = "Workspace diagnostics (telescope)"
    },
    
    -- Incoming calls
    ['<leader>lc'] = {
      function() telescope.lsp_incoming_calls() end,
      desc = "LSP incoming calls (telescope)"
    },
    
    -- Outgoing calls
    ['<leader>lC'] = {
      function() telescope.lsp_outgoing_calls() end,
      desc = "LSP outgoing calls (telescope)"
    },
  }

  -- Apply the mappings
  for key, mapping in pairs(mappings) do
    utils.set_mappings({
      n = {
        [key] = mapping
      }
    })
  end
end

return M