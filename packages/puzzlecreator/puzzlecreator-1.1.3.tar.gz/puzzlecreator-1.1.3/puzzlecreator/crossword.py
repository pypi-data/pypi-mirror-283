import random
import time

def create_empty_crossword(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def place(word, crossword, x, y, direction):
    new_crossword = [row[:] for row in crossword]
    
    if direction == 'HORIZONTAL':
        for i, letter in enumerate(word):
            if x + i < len(new_crossword[0]) and (new_crossword[y][x+i] == ' ' or new_crossword[y][x+i] == letter):
                new_crossword[y][x+i] = letter
            else:
                return None  # Invalid placement
    elif direction == 'VERTICAL':
        for i, letter in enumerate(word):
            if y + i < len(new_crossword) and (new_crossword[y+i][x] == ' ' or new_crossword[y+i][x] == letter):
                new_crossword[y+i][x] = letter
            else:
                return None  # Invalid placement
    
    return new_crossword

def rows(crossword):
    return len(crossword)

def cols(crossword):
    return len(crossword[0]) if crossword else 0

def find_intersections(word, crossword):
    intersections = []
    for y in range(rows(crossword)):
        for x in range(cols(crossword)):
            if crossword[y][x] in word:
                intersections.append((x, y, crossword[y][x]))
    return intersections

def find_placements(word, crossword):
    placements = []
    for y in range(rows(crossword)):
        for x in range(cols(crossword)):
            if x + len(word) <= cols(crossword):
                valid = True
                for i in range(len(word)):
                    if crossword[y][x+i] != ' ' and crossword[y][x+i] != word[i]:
                        valid = False
                        break
                if valid:
                    placements.append((x, y, 'HORIZONTAL'))
            if y + len(word) <= rows(crossword):
                valid = True
                for i in range(len(word)):
                    if crossword[y+i][x] != ' ' and crossword[y+i][x] != word[i]:
                        valid = False
                        break
                if valid:
                    placements.append((x, y, 'VERTICAL'))
    return placements

def generate_score(board):
    score = 0
    for y in range(rows(board)):
        for x in range(cols(board)):
            if board[y][x] != ' ':
                neighbors = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < cols(board) and 0 <= ny < rows(board) and board[ny][nx] != ' ':
                        neighbors += 1
                if neighbors > 0:
                    score += neighbors
    return score

def score_crossword(crossword):
    placed_words = sum(1 for row in crossword for cell in row if cell != ' ')
    width = max((x for y, row in enumerate(crossword) for x, cell in enumerate(row) if cell != ' '), default=0) + 1
    height = max((y for y, row in enumerate(crossword) for x, cell in enumerate(row) if cell != ' '), default=0) + 1
    intersection_score = generate_score(crossword)
    size_score = 1.0 / (width * height) if width * height > 0 else 0
    ratio_score = 1.0 / abs(width - height) if width != height else 1.0
    return placed_words + intersection_score + size_score + ratio_score

def trim_crossword(crossword):
    # Remove empty rows
    crossword = [row for row in crossword if any(cell != ' ' for cell in row)]
    # Transpose, remove empty rows, then transpose back to remove empty columns
    crossword = list(map(list, zip(*crossword)))
    crossword = [row for row in crossword if any(cell != ' ' for cell in row)]
    crossword = list(map(list, zip(*crossword)))
    return crossword

def repeated_word_placement(words, max_time=5):
    words = sorted(words, key=len, reverse=True)
    best_crossword = None
    best_score = -1
    start_time = time.time()

    while time.time() - start_time < max_time:
        random.shuffle(words)
        word = words[0]
        crossword = place(word, create_empty_crossword(15), 0, 0, 'HORIZONTAL')
        count = 1

        for word in words[1:]:
            best_placement_score = -1
            best_board = None

            intersections = find_intersections(word, crossword)
            for (ix, iy, letter) in intersections:
                for i, w_letter in enumerate(word):
                    if w_letter == letter:
                        placements = [(ix-i, iy, 'HORIZONTAL'), (ix, iy-i, 'VERTICAL')]
                        for (x, y, direction) in placements:
                            new_board = place(word, crossword, x, y, direction)
                            if new_board:
                                new_score = generate_score(new_board)
                                if new_score > best_placement_score:
                                    best_placement_score = new_score
                                    best_board = new_board

            if best_board:
                crossword = best_board
                count += 1

        current_score = score_crossword(crossword)
        if current_score > best_score:
            best_score = current_score
            best_crossword = crossword

    return trim_crossword(best_crossword)

def print_crossword(crossword):
    for row in crossword:
        print(' '.join(cell if cell != ' ' else '#' for cell in row))

def remove_letters_from_crossword(crossword):
    for y in range(rows(crossword)):
        for x in range(cols(crossword)):
            if crossword[y][x].isalpha():
                crossword[y][x] = '_'
    return crossword

def get_word_positions(crossword, words):
    positions = {}
    
    for word in words:
        found = False
        # Check horizontally
        for y in range(rows(crossword)):
            for x in range(cols(crossword) - len(word) + 1):
                if all(crossword[y][x + i] == word[i] for i in range(len(word))):
                    positions[word] = (x + 1, y + 1)  # Increment positions to start from 1
                    found = True
                    break
            if found:
                break
        
        if found:
            continue
        
        # Check vertically
        for x in range(cols(crossword)):
            for y in range(rows(crossword) - len(word) + 1):
                if all(crossword[y + i][x] == word[i] for i in range(len(word))):
                    positions[word] = (x + 1, y + 1)  # Increment positions to start from 1
                    found = True
                    break
            if found:
                break
    
    return positions