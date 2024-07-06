# Puzzle Creator

A Python package for creating crossword puzzles.

Creator is Frank Vitetta

CEO and Founder of [Orchid Box Agency](https://www.orchidbox.com/)

## Installation

You can install the package using pip:
`pip install puzzlecreator`

## Usage

from puzzlecreator import crossword

word_list = ["GAME", "BR", "PEALED", "KILLS", "SHOP", "FIG", "PAW", "PUFFED", "BULLET", "MOLLIFY", "KIDS"]

max_time= 5 #number of seconds to find the most efficient combination

result = crossword.repeated_word_placement(word_list, max_time=5)

crossword.print_crossword(result)

```
G A M E # #
S H O P A W
B U L L E T
K I L L S K
# F I G P I
P U F F E D
# # Y # A S
# # # # L #
# # # # E #
# # # # D #
```

## Get Word Positions

from puzzlecreator import crossword

 #Define a list of words to include in the crossword

word_list = ["GAME", "BR", "PEALED", "KILLS", "SHOP", "FIG", "PAW", "PUFFED", "BULLET", "MOLLIFY", "KIDS"]

 #Generate the crossword puzzle

result = crossword.repeated_word_placement(word_list, max_time=5)

 #Get positions of the words in the crossword

positions = crossword.get_word_positions(result, word_list)
print("Positions:", positions)

```
Positions: {'GAME': (1, 1), 'BR': (2, 2), 'PEALED': (5, 3), 'KILLS': (1, 4), 'SHOP': (2, 5), 'FIG': (6, 2), 'PAW': (2, 3), 'PUFFED': (1, 6), 'BULLET': (3, 1),
```

## Remove Letters from Crossword
from puzzlecreator import crossword

 #Define a list of words to include in the crossword

word_list = ["GAME", "BR", "PEALED", "KILLS", "SHOP", "FIG", "PAW", "PUFFED", "BULLET", "MOLLIFY", "KIDS"]

 #Generate the crossword puzzle

result = crossword.repeated_word_placement(word_list, max_time=5)

 #Remove letters from the crossword

empty_crossword = crossword.remove_letters_from_crossword([row[:] for row in result])

print("Crossword without letters:")

crossword.print_crossword(empty_crossword)

```
Crossword without letters:
_ _ _ _ # #
_ _ _ _ _ _
_ _ _ _ _ _
_ _ _ _ _ _
# _ _ _ _ _
_ _ _ _ _ _
# # _ # _ _
# # # # _ #
# # # # _ #
# # # # _ #
```

## Algo Explanation

1.	Intersection Points: Finds potential intersection points where new words can intersect with existing ones.
2.	Placement Scoring: Evaluates each potential placement based on how well it intersects with existing words and the overall compactness of the crossword grid.
3.	Best Placement Selection: Iterates over possible placements for each word, selects the best one based on the score, and updates the grid accordingly.
4.	Multiple Attempts: Generates multiple crossword puzzles within a given time frame (5 seconds is default) and selects the best one based on the scoring criteria.
5.	Trimming the Grid: Before printing, removes any empty rows or columns to ensure a more compact grid.
6.	Result Printing: The final crossword grid is printed with words intersecting properly, and empty spaces are filled with dots (’#’).


```sh
pip install puzzlecreator
