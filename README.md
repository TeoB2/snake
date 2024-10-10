# Snake
Software for Snake game 🐍

Snake is a classic arcade game where players control a snake that continuously moves across the screen. The main goal is to eat food (usually represented as small squares) to grow the snake and increase the score while avoiding collisions with walls or its own body.

### Controls:
 - Up Arrow: Move up.
 - Down Arrow: Move down.
 - Left Arrow: Move left.
 - Right Arrow: Move right.

### Objectives:
 - Collect Food: Guide the snake to eat food that appears randomly on the screen. Each time the snake eats, it grows longer.
 - Avoid Collisions: Do not run into the walls or the snake's body. Hitting either will end the game.
 - Score Points: Each piece of food eaten adds to the player's score, aiming for the highest score possible.


For execute code install all pip dependences:
```
pip install pillow
```

For create a .exe file
```
pip install pyinstaller
```
```
pyinstaller .\app.py --clean --add-data="assets;assets" --onefile --windowed --namesnake --icon=assets/icon.ico   
```

See the .exe file in folder into dist/snake.exe

You can download file .exe from git, if when you open the .exe file Windows Defender reveals an unsafe program is because the code is not encrypted as it is the same code present in the repository. Please continue as the code is not malicious 😊
