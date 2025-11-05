#  ╔═╗╔═╗╦ ╦╦═╗╔═╗  ╔═╗╔═╗╔╗╔╔═╗╦╔═╗	- z0mbi3
#  ╔═╝╚═╗╠═╣╠╦╝║    ║  ║ ║║║║╠╣ ║║ ╦	- https://github.com/gh0stzk/dotfiles
#  ╚═╝╚═╝╩ ╩╩╚═╚═╝  ╚═╝╚═╝╝╚╝╚  ╩╚═╝	- My zsh conf

#  ┬  ┬┌─┐┬─┐┌─┐
#  └┐┌┘├─┤├┬┘└─┐
#   └┘ ┴ ┴┴└─└─┘
export EDITOR='vim'
export TERMINAL='wezterm'
export BROWSER='firefox'
export HISTORY_IGNORE="(ls|cd|pwd|exit|sudo reboot|history|cd -|cd ..)"

export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git --exclude external'

#export LANG=ru_RU.UTF-8
#export LC_ALL=ru_RU.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

#  ┬  ┌─┐┌─┐┌┬┐  ┌─┐┌┐┌┌─┐┬┌┐┌┌─┐
#  │  │ │├─┤ ││  ├┤ ││││ ┬││││├┤
#  ┴─┘└─┘┴ ┴─┴┘  └─┘┘└┘└─┘┴┘└┘└─┘
autoload -Uz compinit

for dump in ~/.config/zsh/zcompdump(N.mh+24); do
  compinit -d ~/.config/zsh/zcompdump
done

compinit -C -d ~/.config/zsh/zcompdump

autoload -Uz add-zsh-hook
autoload -Uz vcs_info
precmd () { vcs_info }

zstyle ':completion:*' verbose true
zstyle ':completion:*:*:*:*:*' menu select
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS} 'ma=48;5;197;1'
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*:warnings' format "%B%F{red}No matches for:%f %F{magenta}%d%b"
zstyle ':completion:*:descriptions' format '%F{yellow}[-- %d --]%f'
zstyle ':vcs_info:*' formats ' %B%s-[%F{magenta}%f %F{yellow}%b%f]-'
zstyle ':fzf-tab:*' fzf-command ftb-tmux-popup

#  ┬ ┬┌─┐┬┌┬┐┬┌┐┌┌─┐  ┌┬┐┌─┐┌┬┐┌─┐
#  │││├─┤│ │ │││││ ┬   │││ │ │ └─┐
#  └┴┘┴ ┴┴ ┴ ┴┘└┘└─┘  ─┴┘└─┘ ┴ └─┘
expand-or-complete-with-dots() {
  echo -n "\e[31m…\e[0m"
  zle expand-or-complete
  zle redisplay
}
zle -N expand-or-complete-with-dots
bindkey "^I" expand-or-complete-with-dots

#  ┬ ┬┬┌─┐┌┬┐┌─┐┬─┐┬ ┬
#  ├─┤│└─┐ │ │ │├┬┘└┬┘
#  ┴ ┴┴└─┘ ┴ └─┘┴└─ ┴
HISTFILE=~/.config/zsh/zhistory
HISTSIZE=5000
SAVEHIST=5000

#  ┌─┐┌─┐┬ ┬  ┌─┐┌─┐┌─┐┬    ┌─┐┌─┐┌┬┐┬┌─┐┌┐┌┌─┐
#  ┌─┘└─┐├─┤  │  │ ││ ││    │ │├─┘ │ ││ ││││└─┐
#  └─┘└─┘┴ ┴  └─┘└─┘└─┘┴─┘  └─┘┴   ┴ ┴└─┘┘└┘└─┘
setopt AUTOCD              # change directory just by typing its name
setopt PROMPT_SUBST        # enable command substitution in prompt
setopt MENU_COMPLETE       # Automatically highlight first element of completion menu
setopt LIST_PACKED	   # The completion menu takes less space.
setopt AUTO_LIST           # Automatically list choices on ambiguous completion.
setopt HIST_IGNORE_DUPS	   # Do not write events to history that are duplicates of previous events
setopt HIST_FIND_NO_DUPS   # When searching history don't display results already cycled through twice
setopt COMPLETE_IN_WORD    # Complete from both ends of a word.

#  ┌┬┐┬ ┬┌─┐  ┌─┐┬─┐┌─┐┌┬┐┌─┐┌┬┐
#   │ ├─┤├┤   ├─┘├┬┘│ ││││├─┘ │
#   ┴ ┴ ┴└─┘  ┴  ┴└─└─┘┴ ┴┴   ┴
function dir_icon {
    if [[ "$PWD" == $HOME(|/*) ]]; then
    echo "%B%F{cyan}%f%b"
  else
    echo "%B%F{cyan}%f%b"
  fi
}
bindkey -v

PS1='%B%F{blue}%f%b %B%F{blue}%n@${${(%):-%m}##*-}%f%b $(dir_icon) %B%F{cyan}%2~ %f%b${vcs_info_msg_0_} %(?.%B%F{green}.%F{red})%f%b '

# #  ┌─┐┬  ┬ ┬┌─┐┬┌┐┌┌─┐
# #  ├─┘│  │ ││ ┬││││└─┐
# #  ┴  ┴─┘└─┘└─┘┴┘└┘└─┘
#    The following plugins has been moved into ~/.zshrc.local
# source ~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
# source ~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
# source ~/.zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
# source ~/.zsh/plugins/zsh-auto-notify/auto-notify.plugin.zsh
# source ~/.zsh/plugins/fzf-tab/fzf-tab.plugin.zsh

# Location specific settings.
if [ -f ~/.zshrc.local ]; then
    . ~/.zshrc.local
fi

bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# OPENAI_API_KEY
if [ -f ~/.sk ]; then
    source ~/.sk
fi

#  ┌─┐┬  ┬┌─┐┌─┐
#  ├─┤│  │├─┤└─┐
#  ┴ ┴┴─┘┴┴ ┴└─┘
#
alias tmux='TERM=screen-256color tmux'
alias tma='tmux attach'

alias  l='ls --color=always'
alias ll='ls -lh --color=always'
alias la='ls -alh --color=always'

alias rgi='rg -i'

#alias ls='lsd -a --group-directories-first'

#  ┌─┐┬ ┬┌┬┐┌─┐  ┌─┐┌┬┐┌─┐┬─┐┌┬┐
#  ├─┤│ │ │ │ │  └─┐ │ ├─┤├┬┘ │
#  ┴ ┴└─┘ ┴ └─┘  └─┘ ┴ ┴ ┴┴└─ ┴

# Set up fzf key bindings and fuzzy completion
source <(fzf --zsh)

# git hotkeys - especially <C-g><C-b> to bring up fzf with all git branches
if [ -f ~/.gitrc ]; then
    . ~/.gitrc
fi

# opencode
export PATH=/home/yury/.opencode/bin:$PATH
