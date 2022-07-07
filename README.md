# anyNote
a light weight cli tool note system that can be read notes in the terminal on the fly

# to Install
```
git clone https://github.com/michavardy/anyNote
nano ~/.bashrc
alias anynote=<path_to_anynote>/anyNote/cli.sh $PWD
```
# to Use
1. go to projects file and type anynote init
2. go to .anynote/notes.md and type in notes
3. type in anynote -r <keyword> to access notes in command line


# note format
example
# Keyword
```
code line 1    # comment
code line 2    # comment
code line 3    # comment
```
## sub-Keyword
```
code line 1    # comment
code line 2    # comment
code line 3    # comment
```
# example use
$ anynote -r keyword
>> ```
>> code line 1    # comment
>> code line 2    # comment
>> code line 3    # comment
>> ```






