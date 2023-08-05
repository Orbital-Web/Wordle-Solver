# Wordle-Solver
An efficient Wordle Solver in Python.

## How to use

1. Run `Solver.py`
2. The program will send a word to guess. Once you enter the word, type the result in the console.
3. Green letters should be typed in caps

   Yellow letters should be typed in lowercase

   Black letters should be replaced with a period


## Example

```
Guess:  aeros, 14855 possible words
Result: Ae.o.

Guess:  alone, 24 possible words
Result: A.OnE

Guess:  anode, 1 possible words
Result: ANODE
You won!
```

## How it works

The solver first starts by creating a filter, which is a list of possible letters at each position.

It parses the word left to right, keeping track of letters marked green and yellow. If a black letter is encountered, it first checks whether that letter is also in yellows (using the fact that in the case of repeated letters, yellows always comes before blacks). If it is, the black letter is treated as another yellow. Otherwise, it adds the letter to the exclude list.

Then, the black letters are excluded from every position, and the yellow letters are removed while the green letters are added back. The greens are added later in the case a letter is marked as both green and black.

Next, the solver filters the words using the given filter, and also checks all letters marked yellow are included.

Lastly, the solver counts how many times each letter (A to Z) appears in the filtered words. It then goes through each word in the filtered list, gives a score based on the sum of frequencies of each letter in the word, times the number of unique letters, and picks the highest scoring word.