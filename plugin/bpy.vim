if !has('python')
        echo "Error: Required vim compiled with +python"
            finish
        endif

let s:scriptfile=expand("<sfile>")
function! Post()
    execute "pyfile ".fnameescape(fnamemodify(s:scriptfile, ":h")."/bpy.py") 
endfunc
command! -nargs=0 Post call Post()
