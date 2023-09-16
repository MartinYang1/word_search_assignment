import random


C_WIDTH = 800
C_HEIGHT = 1000

def get_words(difficulty):
    with open("words.txt") as f:
        words = [line.strip() for line in f.readlines()]
    
    if difficulty == 1:
        return [random.choice(words) for i in range(5)]
    elif difficulty == 2:
        return [random.choice(words) for i in range(10)]
    else:
        return [random.choice(words) for i in range(15)]


def draw_grid(rows, columns):
    grid_w = C_WIDTH / (columns + 1)
    
    for i in range(rows + 1):
        line(0, i * grid_w, C_WIDTH, i * grid_w)
    
    for j in range(columns + 1):
        line(j * grid_w, 0, j * grid_w, grid_w * rows)
        

def location_valid(grid, word, word_start_pos, word_end_pos, direction):
    word_end_pos
    if word_end_pox[0] < len(grid) or word_end_pos[1] < len(grid):
        return True
    
    x, y = word_start_pos
    for letter in word:
        if not (grid[y][x] == " " or grid[y][x] == letter):
            return False
        x += direction[0]
        y += direction[1]
            
    

def place_initial_words(grid, words):
    words_temp = words[:]
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, 1)]
    
    for word in words_temp[0]:
        x, y = random.randrange(0, len(grid)), random.randrange(0, len(grid))
        direction = random.choice(directions)
        if location_valid(grid, word, 
        for letter in word:
            print(y, x)
            grid[y][x] = letter
            x += direction[0]
            y += direction[1]

    
def generate_word_search(rows, columns, grid_w, words):
    draw_grid(rows, columns)
    
    grid = [[' ' for _ in range(columns)] for _ in range(rows)]
    place_initial_words(grid, get_words(2))
    
    
    
def setup():
    generate_word_search(10, 10, 2, get_words(1))
    size(C_WIDTH, C_HEIGHT)

def draw():
    pass
