import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import os
import sys

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.pack()  # Assicura che il Canvas sia visibile prima di aggiungere gli oggetti
        self.start_game_text()

    def load_assets(self):
        try:
            brundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
            path_to_snake = os.path.join(brundle_dir, "assets", "snake.png")
            self.snake_body_image = Image.open(path_to_snake)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            path_to_food = os.path.join(brundle_dir, "assets", "food.png")
            self.food_image = Image.open(path_to_food)
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print("Errore nel caricamento delle immagini:", error)
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(35, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10)
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")
        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def start_game_text(self):
        self.update_idletasks()

        self.create_text(
                self.winfo_width() / 2, 
                self.winfo_height() / 2,
                text="Welcome into Snake game! Use arrows to play ←↑↓→\n\nPress Enter to start the game!",
                fill="#fff", 
                font=14, 
                anchor="center", 
                tag="welcome_text"
            )
        
        self.bind_all("<Return>", self.start_game)

    def start_game(self, event=None):
        #cancello testo di inizio
        self.delete("welcome_text")

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"
        self.score = 0  # Inizializza il punteggio
        self.load_assets()
        self.create_objects()
        self.bind_all("<Key>", self.on_key_press)
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (head_x_position in (0, 600) or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:])

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 20,
                         text=f"Game over! You scored {self.score}!", fill="#fff", font=14)

        # Crea il pulsante "Restart"
        restart_button = tk.Button(
            root, 
            text="Restart", 
            command=self.restart_game, 
            cursor="hand2",
            font=("Arial", 4, "bold"),  # Font più carino e in grassetto
            bg="#4CAF50",  # Colore di sfondo verde
            fg="white",    # Testo bianco
            activebackground="#45a049",  # Colore quando viene premuto
            activeforeground="white",    # Testo bianco quando attivo
            width=10,  # Larghezza del pulsante
            height=1,  # Altezza del pulsante
            relief="raised",  # Bordo del pulsante
            bd=3  # Spessore del bordo
        )
        restart_button.pack()
        
        # Posiziona il pulsante al centro sotto il messaggio di "Game over"
        self.create_window(
            self.winfo_width() / 2, 
            self.winfo_height() / 2 + 40,  # Posiziona sotto il messaggio di "Game over"
            window=restart_button
        )
        
    def restart_game(self):
        # Cancella gli oggetti del canvas e riavvia il gioco
        self.delete(tk.ALL)

        # Chiama il metodo per iniziare il gioco
        self.start_game()

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        if new_direction in all_directions and {new_direction, self.direction} not in opposites:
            self.direction = new_direction

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
        else:
            self.check_food_collision()
            self.move_snake()
            self.after(GAME_SPEED, self.perform_actions)

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions:
                return food_position


try:
    root = tk.Tk()
    root.title("Snake")
    root.resizable(False, False)

    try:
        path_image = os.path.join(os.path.dirname(__file__), "assets/icon.png")
        icon = tk.PhotoImage(file=path_image)
        root.iconphoto(True, icon)
    except:
        pass

    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets/icon.ico")
        root.iconbitmap(icon_path)  # Rimuovi root.set_app_icon(icon_path)
    except:
        pass

    root.tk.call("tk", "scaling", 4.0)
    board = Snake()
    root.mainloop()
except Exception as error:
    import traceback
    traceback.print_exc()
    input("Press Enter to close the window...")
