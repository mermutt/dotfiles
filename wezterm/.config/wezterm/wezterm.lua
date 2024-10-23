-- Pull in the wezterm API
local wezterm = require 'wezterm'

-- This will hold the configuration.
local config = wezterm.config_builder()
config.enable_tab_bar = false

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
-- config.color_scheme = 'Sagelight'
-- config.color_scheme = 's3r0 modified (terminal.sexy)'
-- config.color_scheme = 'Sea Shells (Gogh)'
config.color_scheme = 'SeaShells'

-- and finally, return the configuration to wezterm
return config
