from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer



def auto_complete(input_list, prompt_text):
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=input_list)
    print(prompt_text)
    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print('You entered:', text)
            break

if __name__ == '__main__':
    input_list = WordCompleter(['abort', 'action', 'add', 'after', 'all', 'alter', 'analyze', 'and'], ignore_case=True)
    AutoComp(input_list)