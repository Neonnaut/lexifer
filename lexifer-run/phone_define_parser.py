import codecs
import re
import sys

import wordgen

class UnknownOption(Exception): pass

class ParseError(Exception): pass


class PhonologyDefinition(object):
    def __init__(self, file_name):
        """Expects a sound_systemtem instance for the first argument."""
        self.sound_system = wordgen.SoundSystem()
        self.file_name = file_name
        self.features = []
        self.macros = {} # The '$S' things
        # For sanity checking at the end
        self.letters = []
        self.ph_classes = []   # phoneme classes
        self.parse()
        self.sanity_check()

        self.no_of_words = None
        self.one_per_line = False
        self.sorted = False

    def parse(self):
        with codecs.open(self.file_name, encoding='utf-8') as f:
            # The loop over the file is handled this way to let me
            # pass in the file handle to a subparser.
            line = f.readline()
            while line != '':
                line = re.sub(r'#.*', '', line)   # comments
                line = line.strip()
                if line == '': 
                    line = f.readline()
                    continue
                if re.match(r'with:', line):
                    self.parse_option(line[5:].strip())
                elif re.match(r'random-rate:', line):
                    self.parse_random_rate(line[12:].strip())
                elif re.match(r'filter:', line):
                    self.parse_filter(line[7:].strip())
                elif re.match(r'reject:', line):
                    self.parse_reject(line[7:].strip())
                elif re.match(r'words:', line):
                    self.parse_words(line[6:].strip())
                elif re.match(r'letters:', line):
                    self.parse_letters(line[8:].strip())
                elif re.match(r'number of words:', line):
                    self.no_of_words = line[16:].strip()
                elif line[0] == '%':
                    self.parse_clusterfield(line, f)
                elif '=' in line:
                    self.parse_class(line)
                else:
                    raise ParseError(line)
                line = f.readline()
        # A non-fatal bit of sanity checking and warning.
        if (self.sound_system.use_assim or self.sound_system.use_coronal_metathesis) and self.sound_system.sorter is None:
            sys.stderr.write("Without 'letters:' cannot apply assimilations or coronal metathesis.\n\n")

# add option to remove: ji, wu, bw, dl, etc. forbid onset
# clusters from the same place 
    def parse_option(self, line):
        for option in line.split():
            if option == 'std-ipa-features':
                #print "Loaded IPA..."
                self.sound_system.use_ipa()
            elif option == 'std-digraph-features':
                self.sound_system.use_digraphs()
            elif option == 'std-assimilations':
                #print "Loaded assimilations..."
                self.sound_system.with_std_assimilations()
            elif option == 'coronal-metathesis':
                self.sound_system.with_coronal_metathesis()
            else:
                raise UnknownOption(option)    

    def add_filter(self, pre, post):
        pre = pre.strip()
        #pre = pre.replace("\\", "\\\\")
        post = post.strip()
        #post = post.replace("\\", "\\\\")
        self.sound_system.add_filter(pre, post)
        
    def parse_filter(self, line):
        for filt in line.split(";"):
            # First, check for a redundant semicolon at the end of the
            # line, resulting in a blank entry.
            filt = filt.strip()
            if filt == '': continue

            # Now we can parse the filter.
            (pre, post) = filt.split(">")
            self.add_filter(pre, post)

    def parse_reject(self, line):
        for filt in line.split():
            self.sound_system.add_filter(filt, 'REJECT')

    def parse_letters(self, line):
        self.letters = line.split()
        self.sound_system.add_sort_order(line)

    def parse_words(self, line):
        line = self.expand_macros(line)
        for (n, word) in enumerate(line.split()):
            # Crude Zipf distribution for word selection.
            self.sound_system.add_rule(word, 10.0 / ((n + 1) ** .9))

    def expand_macros(self, word):
        for (macro, value) in list(self.macros.items()):
            word = re.sub(macro, value, word)
        return word

    def parse_class(self, line):
        (sclass, values) = line.split("=")
        sclass = sclass.strip()
        values = values.strip()
        if sclass[0] == '$':
            self.macros["\\" + sclass] = values
        else:
            self.ph_classes += values.split()
            self.sound_system.add_ph_unit(sclass, values)

    def parse_clusterfield(self, line, fh):
        c2list = line.split()[1:]  # ignore leading %
        # Width of all rows must be 'n'.
        n = len(c2list)
        line = fh.readline()
        while line not in ('','\n','\r\n'):
            # filter comments
            line = re.sub(r'#.*', '', line)   # comments
            line = line.strip()
            if line == '':
                line = fh.readline()
                continue
            row = line.split()
            c1 = row[0]
            row = row[1:]
            if len(row) == n:
                for (i, result) in enumerate(row):
                    if result == '+':
                        continue
                    if result == '-':
                        self.sound_system.add_filter(c1 + c2list[i], 'REJECT')
                    else:
                        self.add_filter(c1 + c2list[i], result)
            elif len(row) > n:
                raise ParseError(f"Cluster field row too long: {line}")
            else:
                raise ParseError(f"Cluster field row too short: {line}")
            line = fh.readline()

    def parse_random_rate(self, line):
        self.sound_system.randpercent = int(line)

    def sanity_check(self):
        # Can't do sanity checking if the letters: directive isn't used.
        if len(self.letters) == 0: return
        letters = set(self.letters)
        phonemes = set(self.ph_classes)
        if not phonemes <= letters:
            diff = list(phonemes - letters)
            msg = "** A phoneme class contains '{}' missing from 'letters'.\n".format(" ".join(diff))
            sys.stderr.write(msg)
            sys.stderr.write("** Strange word shapes are likely to result.\n")

    def generate(self, n=1, unsorted=False):
        return self.sound_system.generate(n, unsorted)
