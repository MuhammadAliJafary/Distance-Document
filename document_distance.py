#====================================

# document_distance.py

#====================================


import string
import math

#-----------------------------------------------------
### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()
#-----------------------------------------------------

### Problem 0: Prep Data ###
def text_to_list(input_text):
    """
    Args:
        input_text: string representation of text from file.
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """
    text = input_text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    words = text.split()
    return words

#-----------------------------------------------------

### Problem 1: Get Frequency ###
def get_frequencies(input_iterable):
    """
    Args:
        input_iterable: a string or a list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
           is a letter or word in input_iterable and the corresponding int
           is the frequency of the letter or word in input_iterable
    Note: 
        You can assume that the only kinds of white space in the text documents we provide will be new lines or space(s) between words (i.e. there are no tabs)
    """
    freq_dict = {}

    if type(input_iterable) == str:
        for ch in input_iterable:
            if ch == " " or ch == "\n" or ch == "\r" or ch == "\t":
                continue
            if ch in freq_dict:
                freq_dict[ch] = freq_dict[ch] + 1
            else:
                freq_dict[ch] = 1

    elif type(input_iterable) == list:
        for word in input_iterable:
            if word in freq_dict:
                freq_dict[word] = freq_dict[word] + 1
            else:
                freq_dict[word] = 1
    else:
        raise TypeError("input_iterable must be a string or a list of strings")

    return freq_dict

#-----------------------------------------------------

### Problem 2: Letter Frequencies ###
def get_letter_frequencies(word):
    """
    Args:
        word: word as a string
    Returns:
        dictionary that maps string:int where each string
           is a letter in word and the corresponding int
           is the frequency of the letter in word
    """
    
    freq_dict = {}
    for letter in word:
        if letter in freq_dict:
            freq_dict[letter] = freq_dict[letter] + 1
        else:
            freq_dict[letter] = 1
    return freq_dict

#-----------------------------------------------------

### Problem 3: Similarity ###
def calculate_similarity_score(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary of letters of word1 or words of text1
        freq_dict2: frequency dictionary of letters of word2 or words of text2
    Returns:
        float, a number between 0 and 1, inclusive
           representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums words
           from these three scenarios:
        * If an element occurs in dict1 and dict2 then
            get the difference in frequencies
        * If an element occurs only in dict1 then take the
            frequency from dict1
        * If an element occurs only in dict2 then take the
            frequency from dict2
         The total frequencies = ALL is calculated by summing
            all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """
    
    total = 0
    for value in freq_dict1.values():
        total = total + value
    for value in freq_dict2.values():
        total = total + value

    if total == 0:
        return 0.0

    difference = 0
    for key in freq_dict1:
        if key in freq_dict2:
            difference = difference + abs(freq_dict1[key] - freq_dict2[key])
        else:
            difference = difference + freq_dict1[key]

    for key in freq_dict2:
        if key not in freq_dict1:
            difference = difference + freq_dict2[key]

    similarity = 1 - (difference / float(total))
    similarity = round(similarity, 2)
    return similarity

#-----------------------------------------------------

### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(freq_dict1, freq_dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
       you will NOT need to worry about case sensitivity.

    Args:
        freq_dict1: frequency dictionary for one text
        freq_dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
            If a word occurs in both dictionaries, consider the sum the
            freqencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
            dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
       return an alphabetically ordered list of all these words.
    """
    
    combined = {}

    for word in freq_dict1:
        if word in combined:
            combined[word] = combined[word] + freq_dict1[word]
        else:
            combined[word] = freq_dict1[word]

    for word in freq_dict2:
        if word in combined:
            combined[word] = combined[word] + freq_dict2[word]
        else:
            combined[word] = freq_dict2[word]

    if len(combined) == 0:
        return []

    max_freq = 0
    for word in combined:
        if combined[word] > max_freq:
            max_freq = combined[word]

    most_frequent = []
    for word in combined:
        if combined[word] == max_freq:
            most_frequent.append(word)

    most_frequent.sort()
    return most_frequent

#-----------------------------------------------------

### Problem 5: TF ###
def get_tf(file_path):
    """
    Args:
        file_path: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculatd as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    """
    f = open(file_path, 'r', encoding='utf-8')
    text = f.read()
    f.close()

    for char in string.punctuation:
        text = text.replace(char, "")
    text = text.lower()

    words = text.split()
    total_words = len(words)

    freq_dict = {}
    for word in words:
        if word in freq_dict:
            freq_dict[word] = freq_dict[word] + 1
        else:
            freq_dict[word] = 1

    tf_dict = {}
    for word in freq_dict:
        tf_dict[word] = freq_dict[word] / float(total_words)

    return tf_dict

#-----------------------------------------------------

### Problem 6: IDF ###
def get_idf(file_paths):
    """
    Args:
        file_paths: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
        documents with word *i* in it), where log_10 is log base 10 and can be called
        with math.log10()

    """
    
    total_docs = len(file_paths)
    count_dict = {}

    for path in file_paths:
        f = open(path, 'r', encoding='utf-8')
        text = f.read()
        f.close()

        for char in string.punctuation:
            text = text.replace(char, "")
        text = text.lower()

        words = text.split()
        unique_words = []
        for w in words:
            if w not in unique_words:
                unique_words.append(w)

        for w in unique_words:
            if w in count_dict:
                count_dict[w] = count_dict[w] + 1
            else:
                count_dict[w] = 1

    idf_dict = {}
    for w in count_dict:
        idf_dict[w] = math.log10(total_docs / float(count_dict[w]))

    return idf_dict

#-----------------------------------------------------

### Problem 7: TF-IDF ###
def get_tfidf(tf_file_path, idf_file_paths):
    """
        Args:
            tf_file_path: name of file in the form of a string (used to calculate TF)
            idf_file_paths: list of names of files, where each file name is a string
               (used to calculate IDF)
        Returns:
           a sorted list of tuples (in increasing TF-IDF score), where each tuple is
              of the form (word, TF-IDF). In case of words with the same TF-IDF, the
              words should be sorted in increasing alphabetical order.

        * TF-IDF(i) = TF(i) * IDF(i)
        """
    tf_dict = get_tf(tf_file_path)
    idf_dict = get_idf(idf_file_paths)

    tfidf_list = []
    for word in tf_dict:
        if word in idf_dict:
            value = tf_dict[word] * idf_dict[word]
        else:
            value = 0
        tfidf_list.append((word, value))

    # Sort alphabetically first, then by TF-IDF value
    tfidf_list.sort()
    tfidf_list.sort(key=lambda x: x[1])
    return tfidf_list

#-----------------------------------------------------

if __name__ == "__main__":
    
    #Tests Problem 0: Prep Data
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = text_to_list(hello_world), text_to_list(hello_friend)
    print(world)      # should print ['hello', 'world', 'hello']
    print(friend)     # should print ['hello', 'friends']

    #Tests Problem 1: Get Frequencies
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = text_to_list(hello_world), text_to_list(hello_friend)
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    print(world_word_freq)    # should print {'hello': 2, 'world': 1}
    print(friend_word_freq)   # should print {'hello': 1, 'friends': 1}

    #Tests Problem 2: Get Letter Frequencies
    freq1 = get_letter_frequencies('hello')
    freq2 = get_letter_frequencies('that')
    print(freq1)      #  should print {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    print(freq2)      #  should print {'t': 2, 'h': 1, 'a': 1}

    #Tests Problem 3: Similarity
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = text_to_list(hello_world), text_to_list(hello_friend)
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    word1_freq = get_letter_frequencies('toes')
    word2_freq = get_letter_frequencies('that')
    word3_freq = get_frequencies('nah')
    word_similarity1 = calculate_similarity_score(word1_freq, word1_freq)
    word_similarity2 = calculate_similarity_score(word1_freq, word2_freq)
    word_similarity3 = calculate_similarity_score(word1_freq, word3_freq)
    word_similarity4 = calculate_similarity_score(world_word_freq, friend_word_freq)
    print(word_similarity1)       # should print 1.0
    print(word_similarity2)       # should print 0.25
    print(word_similarity3)       # should print 0.0
    print(word_similarity4)       # should print 0.4

    #Tests Problem 4: Most Frequent Word(s)
    freq_dict1, freq_dict2 = {"hello": 5, "world": 1}, {"hello": 1, "world": 5}
    most_frequent = get_most_frequent_words(freq_dict1, freq_dict2)
    print(most_frequent)      # should print ["hello", "world"]

    #Tests Problem 5: Find TF-IDF
    tf_text_file = 'tests/student_tests/hello_world.txt'
    idf_text_files = ['tests/student_tests/hello_world.txt', 'tests/student_tests/hello_friends.txt']
    tf = get_tf(tf_text_file)
    idf = get_idf(idf_text_files)
    tf_idf = get_tfidf(tf_text_file, idf_text_files)
    print(tf)     # should print {'hello': 0.6666666666666666, 'world': 0.3333333333333333}
    print(idf)    # should print {'hello': 0.0, 'world': 0.3010299956639812, 'friends': 0.3010299956639812}
    print(tf_idf) # should print [('hello', 0.0), ('world', 0.10034333188799373)]
