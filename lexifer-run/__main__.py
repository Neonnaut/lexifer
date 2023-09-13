import os
import textwrap



os.chdir(os.path.dirname(os.path.realpath(__file__)))

from phone_define_parser import PhonologyDefinition
from wordgen import textify
from settings import ARGUMENTS

from pyuca.collator import Collator
c = Collator("pyuca/allkeys.txt")
sorted_words = sorted(["z","ä","a","á","ê"], key=c.sort_key)

print(sorted_words)


def main():
    pd = PhonologyDefinition(file_name = ARGUMENTS.get('filename'))
    text = generate_words(pd = pd)
    print_results(text = text)
    


def generate_words(pd:PhonologyDefinition) -> str:
    """.

    Args:
        param1 (int): The first parameter.
        param2: The second parameter.

    Returns:
        Returns a string of words.
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
                return textify(pd.sound_system, 25)

def print_results(text:str) -> None:
    # Hack to make print stop whining about encodings.
    utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
    print(text, file=utf8stdout)

if __name__ == '__main__':
    main()