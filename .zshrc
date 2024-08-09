export ZSH="$HOME/.oh-my-zsh"

if [[ ! -d "$ZSH" ]]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended --keep-zshrc
fi

if [[ ! -d "$ZSH/custom/plugins/zsh-syntax-highlighting" ]]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH/custom/plugins/zsh-syntax-highlighting"
fi

ZSH_THEME="eastwood"

if [[ $TERM_PROGRAM == "WarpTerminal" ]]; then
    plugins=(git brew)
else
    plugins=(git brew zsh-syntax-highlighting vi-mode)
fi

# Configure path
path+=("$HOME/.local/bin")

if [[ -f "$HOME/.zsh_path" ]]; then
    source "$HOME/.zsh_path"
fi

export PATH

# Configure keys
bindkey "^[^[[C" forward-word
bindkey "^[^[[D" backward-word

# End
source $ZSH/oh-my-zsh.sh

export EDITOR='vim'

# @if OS_NAME == "macos"
# @include "include/zshrc/conda.zsh"
# @endif

# @if OS_NAME == "macos"
if [ -d "$HOME/Library/pnpm" ]; then
    export PNPM_HOME="$HOME/Library/pnpm"
    case ":$PATH:" in
    *":$PNPM_HOME:"*) ;;
    *) export PATH="$PNPM_HOME:$PATH" ;;
    esac
fi
# @endif
