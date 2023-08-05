def load_words():
    '''
    Opens wordlist.txt and extracts all words
    '''
    with open("worldlist.txt", "r") as f:
        wordlist = f.read().splitlines()
    return wordlist



def create_filter(word: str, result: str) -> dict:
    '''
    Creates a filter from the tested `word` and `result`
    `result`:
        period:    (black)  not included
        lowercase: (yellow) included, wrong position
        uppercase: (green)  included, correct position
    
    Returns:
        list of possible letters at each position,
        set of letters marked yellow
        
    '''
    # force lower just in case
    word = word.lower()
    
    greens  = [''] * 5
    yellows = [''] * 5
    blacks = set()
    
    for i, (letter, flag) in enumerate(zip(word, result)):
        # green
        if flag.isupper():
            greens[i] = letter
        
        # yellow
        elif flag.islower():
            yellows[i] = letter
        
        # blacks (only black letters not in yellow are completely excluded)
        else:
            if letter in yellows:
                yellows[i] = letter
            else:
                blacks.add(letter)
                
    # remove blacks
    filters = [''.join(l for l in "abcdefghijklmnopqrstuvwxyz" if l not in blacks)] * 5
    
    # remove yellows and add greens
    for i, (green, yellow) in enumerate(zip(greens, yellows)):
        if green != '':
            filters[i] = green
        elif yellow != '':
            filters[i] = filters[i].replace(yellow, '')
    
    # convert yellows to set
    yellows = set(yellows)
    yellows.remove('')
    
    return {
        "filter": filters,
        "yellows": yellows,
    }
    


def filter_words(wordlist: list[str], filters: dict):
    '''
    Filters `wordlist` based on the info provided by `filters`
    '''
    filtered = []
    
    for word in wordlist:
        if (
            not any(letter not in filt for (letter, filt) in zip(word, filters["filter"]))  # matches filter
            and all(yellow in word for yellow in filters["yellows"])    # contains all yellows
        ):
            filtered.append(word)
    
    return filtered



def pick_word(wordlist: list[str]) -> str:
    '''
    Assigning a score to each word in `wordlist` based on occurance
    of high frequency letters, and returns the highest scoring word
    '''
    freq = dict()
    
    # count letter frequency (ignore repeats in a single word)
    for letter in "abcdefghijklmnopqrstuvwxyz":
        freq[letter] = sum(letter in word for word in wordlist)
    
    bestscore = -1
    bestword = ""
    
    # find best word
    for word in wordlist:
        score = sum(freq[letter] for letter in word)
        score *= len(set(letter for letter in word))    # encourage diversity
        if score > bestscore:
            bestword = word
            bestscore = score
        
    return bestword
        



if __name__ == '__main__':
    wordlist = load_words()
    
    print("\nHow to use:")
    print("  The program will send a word to guess. Once you enter the word, type the result in the console.")
    print("  Green letters should be typed in caps")
    print("  Yellow letters should be typed in lowercase")
    print("  Black letters should be replaced with a period '.'\n")
    
    # initial guess
    guess = pick_word(wordlist)
    print(f"Guess:  {guess}, {len(wordlist)} possible words")
    
    # 5 more tries
    for i in range(5):
        result = input("Result: ")
        if result.isupper() and '.' not in result:
            print("You won!")
            exit()
        
        filters = create_filter(guess, result)
        wordlist = filter_words(wordlist, filters)
        guess = pick_word(wordlist)
        print(f"\nGuess:  {guess}, {len(wordlist)} possible words")
    
    result = input("Result: ")
    if result.isupper() and '.' not in result:
        print("You won!")
        exit()
    
    print("You lose")