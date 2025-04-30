import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import sys


#credit : Dhruv Hazarika
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 5
SPACE_SIZE = 50
INITIAL_BODY_PARTS = 3
SNAKE_COLOR = "red"
FOOD_COLOR = "green"
BG_COLOR = "#0B192C"

class Snake:
    def __init__(self) :
        self.reset_snake()



    def reset_snake(self) :
        self.snake_body_size = INITIAL_BODY_PARTS
        self.coordinates_of_snake = [[0, 0]] * self.snake_body_size
        self.squares = []  # this stores the shape of the squares of the snake
        self.direction = "down"
        for x, y in self.coordinates_of_snake:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        self.create_food()

    def create_food(self):
        self.x = random.randint(0,(GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [self.x, self.y]
        donut_image = Image.open("assets/doughnut.png")
        donut_image = donut_image.resize((SPACE_SIZE, SPACE_SIZE), Image.Resampling.LANCZOS)
        self.food = ImageTk.PhotoImage(donut_image)
        canvas.create_image(self.x, self.y, image=self.food, anchor ="nw", tag ="food")
        # canvas.create_oval(self.x, self.y,self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill= FOOD_COLOR, tags="food")

def next_turn(snake, food):
    x,y = snake.coordinates_of_snake[0]
    direction = snake.direction

    if direction == "up":
        y -= SPACE_SIZE
    if direction == "down":
        y += SPACE_SIZE
    if direction == "left":
        x -= SPACE_SIZE
    if direction == "right":
        x += SPACE_SIZE

    snake.coordinates_of_snake.insert(0, [x,y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
    snake.squares.insert(0, square)

    if food.x == x and food.y == y:
        canvas.delete("food")
        food.create_food()

    else:
        del snake.coordinates_of_snake[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(x,y,snake) == True:
        game_over ()
        return

    window.after(1000//SPEED, next_turn, snake, food)


def game_over():
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 40, text = "Game Over", fill = "white", font = ("consolas", 50))
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 10, text="Press 'R' to Restart", fill="white", font=("consolas", 20))
    window.update()
    window.bind('r', restart_game)


def restart_game(event):
    canvas.delete("all")
    snake.reset_snake()
    food.create_food()
    next_turn(snake, food)
    window.unbind('<r>')


def change_direction(direction, snake):
    opposite_directions = { "left" : "right", "right" : "left", "up" : "down", "down" : "up"}
    if direction != opposite_directions.get (snake.direction):
        snake.direction = direction


def check_collision (x,y,snake):
    # TODO: Check collision with walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for x_val, y_val in snake.coordinates_of_snake[1:]:
        if x == x_val and y == y_val:
            return True
    return False





window = tk.Tk()
window.title("Snake Gobbler Game")
window.resizable(False, False)

# Game canvas setup
canvas = tk.Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
snake = Snake()
food = Food()

window.bind('<Left>', lambda event: change_direction('left', snake))
window.bind('<Right>', lambda event: change_direction('right', snake))
window.bind('<Up>', lambda event: change_direction('up', snake))
window.bind('<Down>', lambda event: change_direction('down', snake))

next_turn(snake, food)
#Center the window on the screen
window.update()

window_height = window.winfo_height()
window_width = window.winfo_width()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width /2) - window_width / 2)
y = int((screen_height /2) - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{x}+{y}')

#main event loop
window.mainloop()


