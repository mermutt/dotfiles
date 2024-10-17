set nocompatible

filetype indent plugin on

syntax on

set hidden

set viminfo+=!

set wildmenu

set showcmd

set hlsearch

set ignorecase
set smartcase

" Allow backspacing over autoindent, line breaks and start of insert action
set backspace=indent,eol,start

set autoindent

" Stop certain movements from always going to the first character of a line.
set nostartofline

" Display the cursor position on the last line of the screen or in the status
" line of a window
set ruler

" Always display the status line, even if only one window is displayed
set laststatus=2

" Instead of failing a command because of unsaved changes, instead raise a
" dialogue asking if you wish to save changed files.
set confirm

" Use visual bell instead of beeping when doing something wrong
set visualbell

" And reset the terminal code for the visual bell. If visualbell is set, and
" this line is also included, vim will neiher flash nor beep. If visualbell is
" unset, this does nothing.
set t_vb=

" Enable use of the mouse for all modes
set mouse=c

" Set the command window height to 2 lines, to avoid many cases of having to
" "press <Enter> to continue"
set cmdheight=2

" Display line numbers on the left
set number

" Quickly time out on keycodes, but never time out on mappings
set notimeout ttimeout ttimeoutlen=200

" Use <F11> to toggle between 'paste' and 'nopaste'
set pastetoggle=<F11>

set shiftwidth=4
set softtabstop=4
set expandtab

let mapleader = " "

nmap <Leader>b :!cscope -bR<CR>:!ctags -R<CR>:cscope reset<CR>
nmap <Leader>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>f :cs find f <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>i :cs find i <C-R>=expand("<cword>")<CR><CR>
nmap <Leader>d :cs find d <C-R>=expand("<cword>")<CR><CR>

map Y y$

nnoremap <C-L> :nohl<CR><C-L>

nnoremap <Leader>r :%s/^\S\+\s.s\s\[/\[/g<CR>

colorscheme jellybeans

set nowrap
