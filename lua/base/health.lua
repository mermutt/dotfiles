-- Command to check if you have the required dependencies to use NormalNvim.
--
-- DESCRIPTION:
-- To use it run the command :healthcheck base

local M = {}

local health = {
  start = vim.health.start or vim.health.report_start,
  ok = vim.health.ok or vim.health.report_ok,
  warn = vim.health.warn or vim.health.report_warn,
  error = vim.health.error or vim.health.report_error,
  info = vim.health.info or vim.health.report_info,
}

function M.check()
  health.start "NormalNvim"

  health.info(
    "NormalNvim Version: " .. require("distroupdate.utils.updater").version(true)
  )
  health.info(
    "Neovim Version: v"
    .. vim.fn.matchstr(vim.fn.execute "version", "NVIM v\\zs[^\n]*")
  )

  if vim.version().prerelease then
    health.warn "Neovim nightly is not officially supported and may have breaking changes"
  elseif vim.fn.has "nvim-0.9" == 1 then
    health.ok "Using stable Neovim >= 0.9.0"
  else
    health.error "Neovim >= 0.9.0 is required"
  end

  -- Checks to perform.
  local programs = {
    {
      cmd = { "git" },
      type = "error",
      msg = "Used for core functionality such as updater and plugin management",
    },
    {
      cmd = { "node" },
      type = "error",
      msg = "Used for core functionality such as updater and plugin management",
    },
    {
      cmd = { "yarn" },
      type = "error",
      msg = "Used for core functionality such as updater and plugin management.",
    },
    {
      cmd = { "markmap" },
      type = "warn",
      msg = "Used by markmap.nvim. Make sure yarn is in your PATH. To learn how check markmap.nvim github page.",
    },
    {
      cmd = { "fd" },
      type = "error",
      msg = "Used for nvim-spectre to find using fd.",
    },
    {
      cmd = { "lazygit" },
      type = "warn",
      msg = "Used for mappings to pull up git TUI (Optional)",
    },
    {
      cmd = { "gitui" },
      type = "warn",
      msg = "Used for mappings to pull up git TUI (Optional)",
    },
    {
      cmd = { "delta" },
      type = "warn",
      msg = "Used by undotree to show a diff (Optional)",
    },
    {
      cmd = { "grcov" },
      type = "warn",
      msg = "Used to show code coverage (Optional)",
    },
    {
      cmd = { "pytest" },
      type = "warn",
      msg = "Used to run python tests (Optional)",
    },
    {
      cmd = { "doxygen" },
      type = "warn",
      msg = "Used by dooku.nvim to generate c/c++/python/java html docs (optional)",
    },
  }

  -- Actually perform the checks we defined above.
  for _, program in ipairs(programs) do
    if type(program.cmd) == "string" then program.cmd = { program.cmd } end
    local name = table.concat(program.cmd, "/")
    local found = false
    for _, cmd in ipairs(program.cmd) do
      if vim.fn.executable(cmd) == 1 then
        name = cmd
        found = true
        break
      end
    end

    if found then
      health.ok(("`%s` is installed: %s"):format(name, program.msg))
    else
      health[program.type](
        ("`%s` is not installed: %s"):format(name, program.msg)
      )
    end
  end
  health.info("")
  health.info("Write `:bw` to close `:checkhealth` gracefully.")
end

return M
