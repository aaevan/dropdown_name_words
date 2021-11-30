import epitran

def gen_word_dict(input_csv='phonetic_dict.csv'):
    """
    generates a dictionary of words and their phonetic representations
    from a pre-computed file.
    (see phonetic_dict.csv generated_by phonetic_wordset.py)
    """
    word_dict = {}
    with open(input_csv) as f:
        for line in f:
            (key, value) = line.split()
            word_dict[key] = value
    return word_dict

def gen_combo_arr(
    first_input='first_horse.txt',
    second_input='second_horse.txt',
):
    """
    generates an array of every combination of first and last name option
    """
    # generate array of first names:
    firsts_file = open(first_input, "r") 
    firsts = []
    for line in firsts_file:
        firsts.append(line.strip())
    firsts_file.close()
    # generate array of second names:
    seconds_file = open(second_input, "r") 
    seconds = []
    for line in seconds_file:
        seconds.append(line.strip())
    print(f"seconds:\n{seconds}")
    seconds_file.close()
    # stick every permutation of firsts and seconds into one array:
    combo_arr = []
    for first in firsts:
        for second in seconds:
            #print(f'first:{first.strip()}, last:{second.strip()}')
            combined = f'{first.lower().strip()}{second.lower().strip()}'
            combo_arr.append(combined)
    print(f'combo_arr:\n{combo_arr}')
    return combo_arr

def gen_phonetic_dict(input_arr):
    """
    generate a dictionary where the keys are combined words 
    and the values are the phonetic representations of each word
    """
    epi = epitran.Epitran('eng-Latn')
    output_dict = {}
    count = 0
    for word in input_arr:
        phonetic_word = epi.transliterate(word)
        output_dict[word] = phonetic_word
        if count % 1000 == 0:
            print(f'gen_phonetic_dict: {count} words of {len(input_arr)}')
        count += 1
    return output_dict

def main():
    # pairs of every dictionary word and its phonetic representation:
    word_dict = gen_word_dict()
    inverse_word_dict = {value:key for (key, value) in word_dict.items()}
    # generate every pair of first and last name-dropdown options:
    combo_arr = gen_combo_arr()
    # generates  a dictionary (like word_dict) for just the valid pairs of 
    # first names and last names
    phonetic_dict = gen_phonetic_dict(combo_arr)
    output_pairs = []
    for key in phonetic_dict:
        phonetic_value = phonetic_dict[key]
        in_phon_dict = phonetic_value in inverse_word_dict
        not_word = key not in word_dict
        if in_phon_dict and not_word:
            output_tuple = (key, inverse_word_dict[phonetic_value][:-1])
            if output_tuple[0].lower() != output_tuple[1].lower():
                print(f'homophone of "{output_tuple[0]}" and "{output_tuple[1]}"')
                output_pairs.append(output_tuple)
    print(output_pairs)
    output_file = open("output_file", "w")
    output_file.writelines([f'{line[0]}, {line[1]}\n' for line in output_pairs])
    output_file.close()

if __name__ == "__main__":
    main()

