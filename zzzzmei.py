import tkinter as tk
import random

# Настройки
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 10
SNAKE_SPEED = 100  # миллисекунды

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Змейка")
        
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.reset_game()

        self.canvas.bind("<Button-1>", self.restart)

    def reset_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = 'Right'
        self.food_position = self.place_food()

        self.score = 0
        self.game_over = False

        self.master.bind("<Key>", self.change_direction)
        self.update()
    
    def place_food(self):
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        return x, y

    def change_direction(self, event):
        if event.keysym == 'Left' and self.snake_direction != 'Right':
            self.snake_direction = 'Left'
        elif event.keysym == 'Right' and self.snake_direction != 'Left':
            self.snake_direction = 'Right'
        elif event.keysym == 'Up' and self.snake_direction != 'Down':
            self.snake_direction = 'Up'
        elif event.keysym == 'Down' and self.snake_direction != 'Up':
            self.snake_direction = 'Down'

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.canvas.delete(tk.ALL)
            self.draw_snake()
            self.draw_food()
            self.display_score()
            self.master.after(SNAKE_SPEED, self.update)
        else:
            self.display_game_over()

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.snake_direction == 'Left':
            head_x -= SNAKE_SIZE
        elif self.snake_direction == 'Right':
            head_x += SNAKE_SIZE
        elif self.snake_direction == 'Up':
            head_y -= SNAKE_SIZE
        elif self.snake_direction == 'Down':
            head_y += SNAKE_SIZE
        
        # Перемещение за границы
        head_x = head_x % WIDTH
        head_y = head_y % HEIGHT

        new_head = (head_x, head_y)

        if self.check_collision(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        
        if new_head == self.food_position:
            self.score += 1
            self.food_position = self.place_food()
        else:
            self.snake.pop()

    def check_collision(self, head):
        x, y = head
        return head in self.snake[1:]
    
    def draw_snake(self):
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE, fill="green")

    def draw_food(self):
        food_x, food_y = self.food_position
        self.canvas.create_rectangle(food_x, food_y, food_x + SNAKE_SIZE, food_y + SNAKE_SIZE, fill="red")
        
    def display_score(self):
        self.canvas.create_text(50, 10, text=f"Счет: {self.score}", fill="white", font=("Arial", 16))
        
    def display_game_over(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="Ты проиграл!", fill="red", font=("Arial", 24))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, text="Нажмите сюда, чтобы начать заново", fill="white", font=("Arial", 16))

    def restart(self, event):
        if self.game_over:
            self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

