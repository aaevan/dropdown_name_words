#setup wordlist to poll from:
import nltk
nltk.download('words')
from nltk.corpus import words
wordset = set(words.words())

#import epitran to turn the wordset into a phonetic representation for each word
# before first run, follow flite installation instructions at
# https://github.com/dmort27/epitran

#the following worked for me:
"""
$ git clone git@github.com:festvox/flite.git
$ cd flite/

then

$ ./configure && make
$ sudo make install
$ cd testsuite
$ make lex_lookup
$ sudo cp lex_lookup /usr/local/bin
"""
import epitran
epi = epitran.Epitran('eng-Latn')

pho_wordset = []
write_block = []
block_count = 0

output_file = open('phonetic_dict.csv', 'w')

for count, word in enumerate(wordset):
    write_block.append(f'{word}, {epi.transliterate(word)}\n')
    if count % 100 == 0:
        print(f'{count} words transliterated of {len(wordset)}')
    # batch file writes:
    if count % 1000 == 0 and count != 0:
        print(f'writing block {block_count} to file...')
        output_file.writelines(write_block)
        #clear write block
        write_block = []
        block_count += 1
#write final incomplete block to file:
if write_block != []:
    print(f'writing final block ({block_count}) to file.')
    output_file.writelines(write_block)
    block_count += 1

output_file.close()
