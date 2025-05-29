import tkinter as tk
from tkinter import messagebox
import random
import time

class SnakeGame:
    def __init__(self):
        # Game settings
        self.window_width = 600
        self.window_height = 600
        self.grid_size = 20
        self.game_speed = 150  # milliseconds between moves
        
        # Colors
        self.bg_color = "#000000"
        self.snake_color = "#00FF00"
        self.snake_head_color = "#00AA00"
        self.food_color = "#FF0000"
        self.text_color = "#FFFFFF"
        
        # Game state
        self.snake_positions = [(10, 10)]
        self.snake_direction = "Right"
        self.food_position = self.generate_food()
        self.score = 0
        self.game_running = True
        self.game_paused = False
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("🐍 Snake Game - Pure Python")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg_color)
        
        # Create the game canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Create score label
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score} | Length: {len(self.snake_positions)}",
            font=("Arial", 14),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.score_label.pack()
        
        # Create control instructions
        self.controls_label = tk.Label(
            self.root,
            text="Controls: Arrow Keys or WASD | Space: Pause | R: Restart",
            font=("Arial", 10),
            fg="#FFFF00",
            bg=self.bg_color
        )
        self.controls_label.pack()
        
        # Bind keyboard events
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        
        # Start the game loop
        self.update_game()
        
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            x = random.randint(0, (self.window_width // self.grid_size) - 1)
            y = random.randint(0, (self.window_height // self.grid_size) - 1)
            if (x, y) not in self.snake_positions:
                return (x, y)
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym.lower()
        
        if key == "space":
            self.game_paused = not self.game_paused
            return
        
        if key == "r":
            self.restart_game()
            return
        
        if self.game_paused or not self.game_running:
            return
        
        # Movement controls
        new_direction = None
        if key in ["up", "w"]:
            new_direction = "Up"
        elif key in ["down", "s"]:
            new_direction = "Down"
        elif key in ["left", "a"]:
            new_direction = "Left"
        elif key in ["right", "d"]:
            new_direction = "Right"
        
        # Prevent moving in opposite direction
        if new_direction:
            opposite_directions = {
                "Up": "Down",
                "Down": "Up",
                "Left": "Right",
                "Right": "Left"
            }
            if new_direction != opposite_directions.get(self.snake_direction):
                self.snake_direction = new_direction
    
    def move_snake(self):
        """Move the snake in the current direction"""
        head_x, head_y = self.snake_positions[0]
        
        # Calculate new head position
        if self.snake_direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.snake_direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.snake_direction == "Right":
            new_head = (head_x + 1, head_y)
        
        # Check wall collision
        max_x = (self.window_width // self.grid_size) - 1
        max_y = (self.window_height // self.grid_size) - 1
        
        if (new_head[0] < 0 or new_head[0] > max_x or 
            new_head[1] < 0 or new_head[1] > max_y):
            return False
        
        # Check self collision
        if new_head in self.snake_positions:
            return False
        
        # Add new head
        self.snake_positions.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food_position:
            self.score += 10
            self.food_position = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake_positions.pop()
        
        return True
    
    def draw_game(self):
        """Draw all game elements on the canvas"""
        self.canvas.delete("all")
        
        if not self.game_running:
            # Draw game over screen
            self.canvas.create_text(
                self.window_width // 2,
                self.window_height // 2 - 50,
                text="GAME OVER",
                fill="#FF0000",
                font=("Arial", 32, "bold")
            )
            self.canvas.create_text(
                self.window_width // 2,
                self.window_height // 2,
                text=f"Final Score: {self.score}",
                fill=self.text_color,
                font=("Arial", 16)
            )
            self.canvas.create_text(
                self.window_width // 2,
                self.window_height // 2 + 30,
                text="Press R to Restart",
                fill="#FFFF00",
                font=("Arial", 14)
            )
            return
        
        if self.game_paused:
            # Draw pause screen
            self.canvas.create_text(
                self.window_width // 2,
                self.window_height // 2,
                text="PAUSED",
                fill="#FFFF00",
                font=("Arial", 32, "bold")
            )
            self.canvas.create_text(
                self.window_width // 2,
                self.window_height // 2 + 40,
                text="Press Space to Continue",
                fill=self.text_color,
                font=("Arial", 14)
            )
            return
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake_positions):
            x1 = x * self.grid_size
            y1 = y * self.grid_size
            x2 = x1 + self.grid_size
            y2 = y1 + self.grid_size
            
            # Draw head differently from body
            if i == 0:
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.snake_head_color,
                    outline=self.snake_color,
                    width=2
                )
                # Draw eyes
                eye_size = 3
                eye1_x = x1 + 5
                eye2_x = x2 - 8
                eye_y = y1 + 5
                self.canvas.create_oval(
                    eye1_x, eye_y, eye1_x + eye_size, eye_y + eye_size,
                    fill="white"
                )
                self.canvas.create_oval(
                    eye2_x, eye_y, eye2_x + eye_size, eye_y + eye_size,
                    fill="white"
                )
            else:
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.snake_color,
                    outline=self.snake_head_color,
                    width=1
                )
        
        # Draw food
        food_x, food_y = self.food_position
        x1 = food_x * self.grid_size
        y1 = food_y * self.grid_size
        x2 = x1 + self.grid_size
        y2 = y1 + self.grid_size
        
        self.canvas.create_oval(
            x1 + 2, y1 + 2, x2 - 2, y2 - 2,
            fill=self.food_color,
            outline="#AA0000",
            width=2
        )
        
        # Draw grid (optional)
        self.draw_grid()
    
    def draw_grid(self):
        """Draw a subtle grid"""
        for i in range(0, self.window_width, self.grid_size):
            self.canvas.create_line(
                i, 0, i, self.window_height,
                fill="#333333",
                width=1
            )
        for i in range(0, self.window_height, self.grid_size):
            self.canvas.create_line(
                0, i, self.window_width, i,
                fill="#333333",
                width=1
            )
    
    def update_score_display(self):
        """Update the score and length display"""
        self.score_label.config(
            text=f"Score: {self.score} | Length: {len(self.snake_positions)}"
        )
    
    def restart_game(self):
        """Restart the game"""
        self.snake_positions = [(10, 10)]
        self.snake_direction = "Right"
        self.food_position = self.generate_food()
        self.score = 0
        self.game_running = True
        self.game_paused = False
        self.update_score_display()
    
    def update_game(self):
        """Main game loop"""
        if self.game_running and not self.game_paused:
            if not self.move_snake():
                self.game_running = False
                self.show_game_over()
            
            self.update_score_display()
        
        self.draw_game()
        
        # Schedule next update
        self.root.after(self.game_speed, self.update_game)
    
    def show_game_over(self):
        """Show game over message"""
        messagebox.showinfo(
            "Game Over",
            f"Game Over!\n\nFinal Score: {self.score}\nSnake Length: {len(self.snake_positions)}\n\nPress R to restart or close to quit."
        )
    
    def run(self):
        """Start the game"""
        print("🐍 Snake Game Started!")
        print("Controls:")
        print("  - Arrow Keys or WASD: Move")
        print("  - Space: Pause/Unpause")
        print("  - R: Restart")
        print("  - Close window: Quit")
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Start the main loop
        self.root.mainloop()
        
        print(f"Game ended! Final score: {self.score}")

# Additional game modes and features
class SnakeGameAdvanced(SnakeGame):
    """Extended version with additional features"""
    
    def __init__(self):
        super().__init__()
        self.high_score = 0
        self.speed_increase = True
        self.obstacles = []
        self.power_ups = []
        
        # Add high score display
        self.high_score_label = tk.Label(
            self.root,
            text=f"High Score: {self.high_score}",
            font=("Arial", 12),
            fg="#FFD700",
            bg=self.bg_color
        )
        self.high_score_label.pack()
    
    def move_snake(self):
        """Enhanced move with speed increase"""
        result = super().move_snake()
        
        if result and self.speed_increase:
            # Increase speed every 50 points
            if self.score > 0 and self.score % 50 == 0:
                self.game_speed = max(50, self.game_speed - 5)
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
        
        return result

# Demo function to show both versions
def demo_snake_games():
    """Demonstrate both game versions"""
    print("Choose Snake Game Version:")
    print("1. Classic Snake Game")
    print("2. Advanced Snake Game (with speed increase)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        game = SnakeGameAdvanced()
    else:
        game = SnakeGame()
    
    game.run()

# Run the game
if __name__ == "__main__":
    try:
        # Run classic version by default
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        print("This game uses tkinter which should be included with Python.")
