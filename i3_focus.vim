" CountOpenVertical and CountOpenHorizontal: stolen from Ben Klein
" http://www.vim.org/account/profile.php?user_id=67078
" Count the open vertical split windows in the current horizontal split
fun! CountVSplits()
  " If there's only one open window, return 1
  if(winnr('$') == 1)
    return 1
  endif
  let l:start_window = winnr()
  " Start by moving to the top horizontal window
  " in this vertical split window
  let l:status = 0
  execute "1wincmd h"
  while winnr() != l:status
    let l:status = winnr()
    execute "1wincmd h"
  endwhile
  " There's one window so far
  let l:count = 1 | let l:status = winnr()
  " Move to the next top-level vertical window
  execute "1wincmd l"
  " Add to the count each time we can move to
  " another top-level vertical window
  while winnr() != l:status
    let l:status = winnr()
    execute "1wincmd l"
    let l:count += 1
  endwhile
  " Return to the original window
  execute l:start_window . "wincmd w"
  " Return the total
  return l:count
endfun

" Count the open horizontal split windows in the
" current vertical split window
fun! CountHSplits()
  " If there aren't split windows, return 1
  if(winnr('$') == 1)
    return 1
  endif
  let l:start_window = winnr()
  let l:count = 0 | let l:status = 0
  " Start by moving to the top horizontal window
  " in this vertical split window
  execute "1wincmd k"
  while winnr() != l:status
    let l:status = winnr()
    execute "1wincmd k"
  endwhile
  " Once we're there, start over, and begin the
  " count
  let l:status = 0
  " For each time we can move to another window,
  " add one to the count
  while winnr() != l:status
    let l:status = winnr()
    execute "1wincmd j"
    let l:count += 1
  endwhile
  execute l:start_window . "wincmd w"
  " Return the total
  return l:count
endfun
