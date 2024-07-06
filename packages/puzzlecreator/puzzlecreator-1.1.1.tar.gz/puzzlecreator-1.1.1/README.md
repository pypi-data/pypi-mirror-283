# Puzzle Creator

A Python package for creating crossword puzzles.

Creator is Frank Vitetta

CEO and Founder of Orchid Box Agency

## Installation

You can install the package using pip: pip install puzzlecreator

## Usage

from puzzlecreator import crossword

word_list = ["GAME", "BR", "PEALED", "KILLS", "SHOP", "FIG", "PAW", "PUFFED", "BULLET", "MOLLIFY", "KIDS"]
max_time= 5 #number of seconds to find the most efficient combination

result = crossword.repeated_word_placement(word_list, max_time=5)

crossword.print_crossword(result)


## Explanation

	1.	Intersection Points: Finds potential intersection points where new words can intersect with existing ones.
	2.	Placement Scoring: Evaluates each potential placement based on how well it intersects with existing words and the overall compactness of the crossword grid.
	3.	Best Placement Selection: Iterates over possible placements for each word, selects the best one based on the score, and updates the grid accordingly.
	4.	Multiple Attempts: Generates multiple crossword puzzles within a given time frame (5 seconds is default) and selects the best one based on the scoring criteria.
	5.	Trimming the Grid: Before printing, removes any empty rows or columns to ensure a more compact grid.
	6.	Result Printing: The final crossword grid is printed with words intersecting properly, and empty spaces are filled with dots (’.’).


```sh
pip install puzzlecreator
