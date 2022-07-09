from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer



def auto_complete(input_list):
    input_list = WordCompleter(input_list, ignore_case=True)
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=input_list)
    while True:
        try:
            text = session.prompt('> ',vi_mode=True)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            #print('You entered:', text)
            return(text)


if __name__ == '__main__':
    input_list = ['abort', 'action', 'add', 'after', 'all', 'alter', 'analyze', 'and']
    text = auto_complete(input_list)
