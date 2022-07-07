# anynote
a cli repository for notes, envirnmental variables, and passwords easily accessible to any terminal 
## --read, -r
prints note to standard out
```
    $ anynote --read <keyword>
```
## --write, -w
saves note to repo
```
    $ anynote --write <keyword> "messge text"
```
## --replace, -rep
replaces note in repo
```
    $ anynote --replace <keyword> <new_text_file>
```
## --edit-vim, -ev
- pulls keyword note into vim
- vim save pushes new edit
```
    $ anynote --edit-vim <keyword>
```
## --edit-nano, -en
- pulls keyword note into nano
- nano saves pushes new edit
```
    $ anynote --edit-nano <keyword>
```
# init
initializes a new anynote repo
## --local, -l
```
    $ anynote init --local 
```
# remote add
add a remote repository to back up 
```
    $ anynote remote add <repo>
```