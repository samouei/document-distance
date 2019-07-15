
import string

### DO NOT MODIFY THIS FUNCTION
def load_text(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    #print("Loading file...")
    inFile = open(filename, 'r', encoding='ascii', errors='ignore')
    line = inFile.read()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()
##----------------------------------------------------------------------------

### Problem 0: Prep Data ###
def prep_data(input_text):
    """
    Args:
        input_text: string representation of text from file,
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text
    """
    
    # Split a string into a list where each word is a list item
    converted_input_text = input_text.split()
    return converted_input_text 

#    pass

### Problem 1: Find Bigrams ###
def find_bigrams(words):
    """
    Args:
        words: list of words in the text,
               all words are made of lowercase characters
    Returns:
        list of bigrams from input text list
    """
    
    # Create an empty list for storing bigrams
    bigram_list = []
    
    # Loop through the list of words
    for i in range(len(words) - 1):
        
        # Define each word and its next immediate neighbor as a bigram
        bigram = " ".join(words[i : i + 2])
        
        # Add each bigram to a list
        bigram_list.append(bigram)
                
    return bigram_list

#    pass

### Problem 2: Word Frequency ###
def get_frequencies(words):
    """
    Args:
        words: list of words, all words are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string 
        is a word in words and the corresponding int 
        is the frequency of the word in words
    """
    # Create an empty dictionary for storing word frequency values
    frequency_dictionary = {}   
    
    # Loop through the list of words
    for i in (words):
        
        # If word is not in dictionary add it as a key with value 1
        if not i in frequency_dictionary:
            frequency_dictionary[i] = 1
        
        # If word is in dictionary increment value by 1
        else:
            frequency_dictionary[i] += 1
    return frequency_dictionary
    
    
    pass


### Problem 3: Similarity ###
def calculate_similarity(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.
    
    Args:
        dict1: frequency dictionary of words or bigrams for one text
        dict2: frequency dictionary of words or bigrams for another text
    Returns:
        float, a number between 0 and 1, inclusive 
        representing how similar the texts are to each other
        
        The difference in text frequencies = DIFF sums words 
        from these three scenarios: 
        * If a word or bigram occurs in dict1 and dict2 then 
          get the difference in frequencies
        * If a word or bigram occurs only in dict1 then take the 
          frequency from dict1
        * If a word or bigram occurs only in dict2 then take the 
          frequency from dict2
         The total frequencies = ALL is calculated by summing 
         all frequencies in both dict1 and dict2. 
        Return 1-DIFF/ALL rounded to 2 decimal places
    """

   
    DIFF = 0
    ALL = 0
    
    # Loop through dict1
    for i in dict1:
        
        # If a key is in both dicts, get the difference in frequencies
        if i in dict2:
            DIFF += abs(dict1[i] - dict2[i])
            ALL += (dict1[i] + dict2[i])
        else: 
            DIFF += dict1[i]
            ALL += dict1[i]
    
    # Loop through dict2
    for i in dict2:
        if not i in dict1:
            DIFF += dict2[i]
            ALL += dict2[i]
    
    # Calculate similarity rounded to 2 decimal places       
    similarity = round(1 - (DIFF / ALL), 2)
        
    return similarity

    pass

### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.
    
    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
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
    # Create an empty dictionary to merge dict1 and dict2
    combined_dict = {}
    
    # Loop through dict1
    for i in dict1:
        
        # If a key is in both dicts, add their values 
        if i in dict2:
            total_frequency = dict1[i] + dict2[i]
            combined_dict[i] = total_frequency
        else:
            combined_dict[i] = dict1[i]
    
    # Loop through dict2
    for i in dict2:
        if not i in dict1:
            combined_dict[i] = dict2[i]
    
    # Get max value in combined_dict
    max_value = max(combined_dict.values())
    
    # Create an empty list for adding the most frequent word(s)
    value_list = []
    
    # Loop through combined_dict to find keys with max_value
    for i in combined_dict:
        if combined_dict[i] == max_value:
            value_list.append(i)
            
    # Sort value_list alphabetically       
    value_list.sort()
    return value_list

    pass

### Problem 5: Finding closest matching document ###
def find_closest_match(filenames, query, bigrams = False):
    """
    Args:
        filenames: list, names of files to be considered
        query: string, specifying search terms
        bigrams: boolean, optional parameter. Default set to False.
                 If it is True, bigrams of text in files 
                 and bigrams of search query should be used in analysis.
    Returns:
        list of the filenames that most closely match the query string
        based on the similarity function we defined earlier,
        in the case of ties return the filenames sorted by alphabetical order
    """
    # Create an empty list for final result(s)
    closest_match_list = []
    
    # Create an empty dictionaries for storing file names (as key) + content, frequency, similarity (as values)
    file_content_dict = {}
    file_frequency_dict = {}
    file_similarity_dict = {}
    
    # Get frequency for query
    if bigrams:
        query_frequency = get_frequencies((find_bigrams(prep_data(query))))
    else:
        query_frequency = get_frequencies(prep_data(query))
        
    # If no files give, return empty list
    if len(filenames) == 0:
        return closest_match_list
    
    # Loop through filenames to load and prep the data
    for i in filenames:
        file_content_dict[i] = prep_data(load_text(i)) 
        
        # If bigrams condition is true, convert document content to bigrams
        if bigrams:
            file_content_dict[i] = find_bigrams(file_content_dict[i]) 
            
        # Calculate frequencies for documents                          
        file_frequency_dict[i] = get_frequencies(file_content_dict[i])
    
    # Calculate similarity for files
    for i in file_frequency_dict: 
        file_similarity_dict[i] = calculate_similarity(file_frequency_dict[i], query_frequency)    
    
    # Get max similarity value
    max_similarity_value = max(file_similarity_dict.values())
    
    # If max similarity not zero, add file names that match that value to closest_match_list
    if max_similarity_value != 0:   
        for i in file_similarity_dict:
            if file_similarity_dict[i] == max_similarity_value:
                closest_match_list.append(i)
                
        # Sort closest_match_list alphabetically
        closest_match_list.sort()
            
    return closest_match_list
        
    pass


if __name__ == "__main__":
    pass
#    Uncomment the following lines to test your implementation
#    # Tests Problem 0: Prep Data
#    hello_world, hello_friend = load_text('hello_world.txt'), load_text('hello_friends.txt') 
#    world, friend = prep_data(hello_world), prep_data(hello_friend)
#    print(world) ## should print ['hello', 'world', 'hello']
#
#    # Tests Problem 1: Find Bigrams
#    world_bigrams, friend_bigrams = find_bigrams(world), find_bigrams(friend)
#    print(world_bigrams) ## should print ['hello world', 'world hello']
#
#    ## Tests Problem 2: Get frequency
#    world_word_freq, world_bigram_freq = get_frequencies(world), get_frequencies(world_bigrams)
#    friend_word_freq, friend_bigram_freq = get_frequencies(friend), get_frequencies(friend_bigrams)
#    print(world_word_freq) ## should print {'hello': 2, 'world': 1}
#    print(world_bigram_freq) ## should print {'hello world': 1, 'world hello': 1}
#
#    ## Tests Problem 3: Similarity
#    word_similarity = calculate_similarity(world_word_freq, friend_word_freq)
#    bigram_similarity = calculate_similarity(world_bigram_freq, friend_bigram_freq)
#    print(word_similarity) ## should print 0.33
#    print(bigram_similarity) ## should pring 0.0
#
#    ## Tests Problem 4: Most Frequent Word(s)
#    freq1, freq2 = {"hello":5, "world":1}, {"hello":1, "world":5}
#    most_frequent = get_most_frequent_words(freq1, freq2)
#    print(most_frequent) ## should print ["hello", "world"]
#
#    ## Tests Problem 5: Find closeset matching document
#    match1 = find_closest_match(["hello_friends.txt", "hello_world.txt"], "hello")
#    match2 = find_closest_match(["hello_friends.txt", "hello_world.txt"], "hello apples", bigrams=True)
#    print(match2) ## should print []
