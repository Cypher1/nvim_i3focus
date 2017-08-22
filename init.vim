function! RegisterNvimI3Connection()
    if strlen($WINDOWID) != 0
        silent exec '!~/.config/i3/i3_nvim_focus_client.py register '. $WINDOWID . ' ' . shellescape($NVIM_LISTEN_ADDRESS)
        let g:i3_nvim_connection = 1
    else
        let g:i3_nvim_connection = 0
    endif
endfunction

function! UnregisterNvimI3Connection()
    if g:i3_nvim_connection
        silent exec '!~/.config/i3/i3_nvim_focus_client.py unregister '. $WINDOWID
    endif
endfunction

augroup i3
call RegisterNvimI3Connection()
autocmd VimLeave * call UnregisterNvimI3Connection()
augroup END
