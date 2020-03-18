export ZSH="/Users/zmayhew/.oh-my-zsh"

# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="agnoster"

(cat ~/.cache/wal/sequences &)

plugins=(git brew zsh-syntax-highlighting nvm node npm)

source $ZSH/oh-my-zsh.sh

# User configuration

path+=("$HOME/bin")
path+=("$HOME/Library/Python/3.5/bin")
path+=("$HOME/.cargo/bin")

export PATH

# export MANPATH="/usr/local/man:$MANPATH"

export LANG=en_US.UTF-8
export EDITOR='vim'

AGNOSTER_PROMPT_SEGMENTS[2]=
alias code="/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"

fortune -e literature | cowsay
