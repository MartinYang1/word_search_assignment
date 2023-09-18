import random
from copy import deepcopy


C_WIDTH = 800
C_HEIGHT = 1000

def get_words(difficulty):
    with open("words.txt") as f:
        words = [line.strip() for line in f.readlines()]
    
    num_words = 5 if difficulty == 1 else 10 if difficulty == 2 else 15
    random_words = []
    for i in range(num_words):
        word = random.choice(words)
        random_words.append(word)
        words.remove(word)
        
    return random_words


def get_grid_width(grid):
    """Gets the width of each cell that's drawn to the canvas"""
    return C_WIDTH / (len(grid))


def draw_grid(grid):
    grid_w = get_grid_width(grid)
    
    fill(0)
    for i in range(len(grid) + 1):
        line(0, i * grid_w, C_WIDTH, i * grid_w)
    
    for j in range(len(grid)):
        line(j * grid_w, 0, j * grid_w, grid_w * len(grid))


def draw_letter(letter, cell_width, row, column):
    textFont(font, 20)
    fill(0)
    x = column * cell_width + cell_width / 2
    y = row * cell_width + cell_width / 2
    textAlign(CENTER)
    text(letter, x, y)
    noFill()


def location_valid(grid, word, word_start_pos, direction):
    word_end_pos = (word_start_pos[0] + direction[0] * (len(word) - 1), word_start_pos[1] + direction[1] * (len(word) - 1))

    if word_end_pos[0] >= len(grid) or word_end_pos[0] < 0 or word_end_pos[1] >= len(grid) or word_end_pos[1] < 0:
        return False
    
    x, y = word_start_pos
    for letter in word:
        if not (grid[y][x] == " " or grid[y][x] == letter):
            return False
        x += direction[0]
        y += direction[1]

    return True
            

def place_initial_words(grid, words):
    words_temp = words[:]
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    tried_cells = {}  # have each word mapped to the cells that have been tried
    tried_directions = {}  # have each word mapped to the directions that have been tried
    grids = []  # stack containing each grid iteration to be used for backtracking
    visited = {}  # contains a grid mapped to a boolean value
    
    grids.append((deepcopy(grid), 0))
    while grids:
        # print("start loop")
        available_cells = [(x, y) for x in range(len(grid)) for y in range(len(grid))]     
        direction = None
        x, y = None, None
        grid, num_words_placed = grids.pop()
        if num_words_placed == len(words):
            return grid
        
        word = words[num_words_placed]
        # Looping through the child nodes (possible combinations) of the current grid
        while available_cells:
            # there's still cells that haven't been tested yet
            x, y = random.choice(available_cells)
            available_cells.remove((x, y))
            available_directions = directions[:]
            
            while available_directions:
                direction = random.choice(available_directions)
                available_directions.remove(direction)
                if location_valid(grid, word, (x, y), direction):
                    grid_temp = deepcopy(grid)
                    x_temp, y_temp = x, y
                    
                    for letter in word:
                        grid_temp[y_temp][x_temp] = letter
                        x_temp += direction[0]
                        y_temp += direction[1]
                    
                    if not visited.get(tuple(map(tuple, grid_temp))):
                        grids.append((grid_temp, num_words_placed + 1))
                        visited[tuple(map(tuple, grid_temp))] = True
            
    
def generate_word_search(rows, columns, grid_w, words):    
    grid = [[' ' for _ in range(columns)] for _ in range(rows)]
    draw_grid(grid)
    return place_initial_words(grid, words)
    

def coords_to_cell(grid):
    """
    Converts cartesian coordinates on the canvas to the row and column
    in a 2D matrix
    """
    cell_w = get_grid_width(grid)
    return mouseX // cell_w, mouseY // cell_w


def check_word_selected(grid, words, start_x, start_y, end_x, end_y):
    selected = ""
    direction_x = 1 if start_x <= end_x else -1
    direction_y = 1 if start_y <= end_y else -1
    
    if start_x == end_x:
        for i in range(start_y, end_y + 1 if direction_y == 1 else end_y - 1, direction_y):
            selected += grid[i][start_x]
    elif start_y == end_y:
        for j in range(start_x, end_x + 1 if direction_x == 1 else end_x - 1, direction_x):
            selected += grid[start_y][j]
    else:
        # diagonal
        y = start_y
        for j in range(start_x, end_x + 1 if direction_x == 1 else end_x - 1, direction_x):
            selected += grid[y][j]
            y += direction_y
    print(selected)
    if selected in words:
        words.remove(selected)
        print("sel")
        crossout_word(grid, start_x, start_y, end_x, end_y)
        return True


def crossout_word(grid, start_x, start_y, end_x, end_y):
    stroke(255, 255, 153)
    strokeWeight(6)
    cell_width = get_grid_width(grid)
    line(start_x * cell_width + cell_width / 2, 
         start_y * cell_width + cell_width / 2,
         end_x * cell_width + cell_width / 2, 
         end_y * cell_width + cell_width / 2)
    noStroke()

def display_words_remaining():
    textFont(font, 15)
    textAlign(CENTER)
    
    fill("#D3D3D3")
    rect(0, get_grid_width(grid) * len(grid), C_WIDTH, C_HEIGHT)        
    fill(0)
    
    text("Words Remaining: ", C_WIDTH // 2, C_HEIGHT - 140)
    
    word_x = C_WIDTH // 2
    word_y = C_HEIGHT - 120
    for i, word in enumerate(words):
        if i > 0 and i % 5 == 0:
            word_x += 80
            word_y = C_HEIGHT - 120
        text(word, word_x, word_y)
        word_y += 20
    noFill()

def setup():
    global font, words, grid
    global bottom_rect
    
    font = createFont("Arial", 20, True)
    words = get_words(3)
    grid = generate_word_search(12, 12, 2, words)
    for i in range(len(grid)):
        print(grid[i])
        for j, letter in enumerate(grid[i]):
            draw_letter(letter, get_grid_width(grid), i, j)
    
    fill("#D3D3D3")
    rect(0, get_grid_width(grid) * len(grid), C_WIDTH, C_HEIGHT)        
    noFill()
    
    size(C_WIDTH, C_HEIGHT)

def draw():
    display_words_remaining()


def start_screen():
    global curr_screen, difficulty
    
    curr_screen = 0
    difficulty = None
    textFont(font, 30)
    text("Word Search", C_WIDTH // 2, 200)
    
    textFont(font, 20)
    text("Press 1 for easy, 2 for medium, and 3 for hard", C_WIDTH // 2, 400)
    
    text("Instructions: To select a word, click the first letter\nand drag across the word until the last letter", 100, 600)
    

def keyPressed():
    global difficulty
    if curr_screen == 0 and (key == '1' or key == '2' or key == '3'):
        curr_screen = 1
        difficulty = int(key)
        

def mousePressed():
    global mouse_x, mouse_y
    mouse_x, mouse_y = coords_to_cell(grid)
    

def mouseReleased():
    check_word_selected(grid, words, mouse_x, mouse_y, *coords_to_cell(grid))
    
