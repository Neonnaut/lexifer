import os
import textwrap

os.chdir(os.path.dirname(os.path.realpath(__file__)))

from phone_define_parser import PhonologyDefinition
from wordgen import textify
from settings import ARGUMENTS




def main():
    pd = PhonologyDefinition(file_name = ARGUMENTS.get('filename'))
    text = generate_words(pd = pd)
    print_results(text = text)
    


def generate_words(pd:PhonologyDefinition) -> str:
    """Example function with PEP 484 type annotations.

    Args:
        param1 (int): The first parameter.
        param2: The second parameter.

    Returns:
        The return value. True for success, False otherwise.
    """
    if not ARGUMENTS.get('number'):
        # Prints out a paragraph of text.
        return textify(pd.sound_system, 25)
    else:
        # Prints out a list of words.
        try:
            no_of_words = int(ARGUMENTS.get('number'))
        except:
            return textify(pd.sound_system, 25)
        else:
            words = pd.generate(no_of_words, ARGUMENTS.get('unsorted'))
            if ARGUMENTS.get('one_per_line'):
                return '\n'.join([
                    word
                    for word in words
                    if word
                ])
            else:
                return textwrap.wrap('\n'.join([
                    word
                    for word in words
                    if word
                ]))
            
                words = textwrap.wrap(" ".join(words), 70)
                print("\n".join(words), file=utf8stdout)

def print_results(text:str) -> None:
    # Hack to make print stop whining about encodings.
    utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
    print(text, file=utf8stdout)

if __name__ == '__main__':
    main()