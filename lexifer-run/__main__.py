import textwrap

from .phone_define_parser import PhonologyDefinition
from .wordgen import SoundSystem, textify
from .settings import ARGUMENTS

# And off we go!  Parse the definition file.
pd = PhonologyDefinition(SoundSystem(), ARGUMENTS.get('filename'))

# Hack to make print stop whining about encodings.
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

# Generate some words...
if not ARGUMENTS.get('number'):
    # Prints out a paragraph of text.
    print(textify(pd.soundsys, 25), file=utf8stdout)
else:
    # Prints out a list of words.
    try:
        no_of_words = int(ARGUMENTS.get('number'))
    except:
        print(textify(pd.soundsys, 25), file=utf8stdout)
    else:
        words = pd.generate(no_of_words, ARGUMENTS.get('unsorted'))
        if ARGUMENTS.get('one_per_line'):
            for w in words:
                print(w, file=utf8stdout)
        else:
            words = textwrap.wrap(" ".join(words), 70)
            print("\n".join(words), file=utf8stdout)