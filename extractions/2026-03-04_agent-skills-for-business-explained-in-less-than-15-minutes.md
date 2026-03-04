![banner](https://img.youtube.com/vi/YqREHU0pvUc/maxresdefault.jpg)

# Agent Skills for business… explained in less than 15 minutes

> **Source:** YouTube | **Extracted:** 2026-03-04 22:01 UTC | **Method:** grok_api
> **URL:** https://www.youtube.com/watch?v=YqREHU0pvUc

---

### Summary
This comprehensive beginner tutorial by freeCodeCamp teaches how to build a fully functional Tetris game from scratch using vanilla JavaScript, HTML, and CSS. The step-by-step approach covers core game mechanics like tetromino movement, rotation, collision detection, line clearing, and scoring while reinforcing fundamental programming concepts like arrays, DOM manipulation, and event handling.

### Key Insights
- Building games like Tetris is an excellent way to learn fundamental programming concepts in a practical, engaging context
- Vanilla JavaScript without frameworks is sufficient to create complex interactive games, making this accessible to beginners
- Game development requires understanding of multiple programming concepts: 2D arrays for data representation, event handling for user input, DOM manipulation for visual updates, and timing functions for game loops
- Tetris mechanics break down into manageable components: grid representation, shape definitions, movement logic, collision detection, and state management
- The tutorial emphasizes proper project structure with separation of concerns between HTML structure, CSS styling, and JavaScript logic
- Testing and debugging are integral parts of the development process, especially for handling edge cases in game mechanics
- The modular approach to coding (separate functions for drawing, movement, rotation) makes the code maintainable and easier to understand

### Actions
- [ ] Set up a basic HTML file with a game grid container, score display, and start/pause button
- [ ] Create CSS styles for the 10x20 game grid, tetromino blocks, and UI elements
- [ ] Define the 7 tetromino shapes (I, J, L, O, S, T, Z) as 2D arrays with rotation variants
- [ ] Implement the game grid as an array and create DOM elements for each grid square
- [ ] Code the draw/undraw functions to visually represent tetrominoes on the grid
- [ ] Add keyboard event listeners for arrow key controls (left, right, down, rotate)
- [ ] Implement collision detection to prevent invalid moves and freeze tetrominoes
- [ ] Create line clearing logic that removes completed rows and updates the score
- [ ] Add game over detection when new tetrominoes can't spawn
- [ ] Test the game thoroughly, focusing on edge cases like rotation near boundaries
- [ ] Consider adding enhancements like a next piece preview or increasing difficulty levels

### Implementation Prompts

#### Prompt 1: HTML Structure Setup
*Creates the basic HTML foundation for the Tetris game with proper grid container and UI elements.*
> Create an HTML file for a Tetris game with the following requirements:
> - A main container div with class "container" that uses flexbox for centering
> - A game grid div with class "grid" that will hold 200 individual div elements (10x20 grid)
> - A score display showing "Score: 0" with an id="score" span
> - A start/pause button with id="start-button"
> - Internal CSS that styles the grid as 200px wide by 400px tall, with each grid square being 20px x 20px
> - CSS classes for "tetromino" (blue background) and "taken" (for frozen pieces)
> - Include a script tag linking to "app.js"
> Make it visually appealing with proper spacing and colors.

#### Prompt 2: Tetromino Shape Definitions
*Defines all seven tetromino shapes with their rotation states as 2D arrays for easy manipulation.*
> Create JavaScript code that defines all 7 Tetris tetromino shapes (I, J, L, O, S, T, Z) as arrays of rotation states. Each shape should be represented as arrays of numbers indicating positions in a 4x4 grid (0-15). For example:
> - The L-tetromino should have 4 rotation states
> - The I-tetromino should be a straight line in 4 orientations
> - The O-tetromino (square) should be the same in all rotations
> - Include a main array called "theTetrominoes" that contains all shapes
> - Add functions to randomly select a tetromino and cycle through rotations
> - Include comments explaining the grid positioning system (how numbers 0-15 map to a 4x4 grid)

#### Prompt 3: Game Grid and DOM Manipulation
*Sets up the game grid system and functions to interact with the DOM elements.*
> Write JavaScript code for Tetris grid management with these features:
> - Create an array of all grid squares using document.querySelectorAll
> - Initialize game variables: currentPosition (starting at 4), currentRotation (0), score (0)
> - Write a draw() function that adds the "tetromino" class to grid squares based on current piece position
> - Write an undraw() function that removes the "tetromino" class
> - Create a function to generate the initial 200 grid divs and append them to the grid container
> - Add a function to update the score display in the DOM
> - Include proper error handling for invalid grid positions

#### Prompt 4: Movement and Controls System
*Implements keyboard controls and basic tetromino movement with boundary checking.*
> Create the movement system for Tetris with these functions:
> - moveDown(): moves tetromino down by 10 grid positions (one row)
> - moveLeft(): moves tetromino left by 1 position with boundary checking
> - moveRight(): moves tetromino right by 1 position with boundary checking
> - rotate(): cycles to next rotation state with collision checking
> - Add keyboard event listener for arrow keys (37=left, 39=right, 40=down, 38=rotate)
> - Implement boundary detection to prevent pieces from moving outside the 10-column grid
> - Use setInterval to automatically move pieces down every 1000ms
> - Include functions to start/pause the game timer
> Each movement should undraw the piece, change position, then redraw it.

#### Prompt 5: Collision Detection and Freezing Logic
*Handles collision detection, piece freezing, and spawning new tetrominoes.*
> Implement collision detection and piece management for Tetris:
> - Create a freeze() function that detects when a piece hits the bottom or another piece
> - When freezing occurs, add "taken" class to all squares of the current piece
> - After freezing, spawn a new random tetromino at the top (position 4)
> - Add collision checking for rotations to prevent invalid moves
> - Implement game over detection when a new piece can't spawn due to occupied squares
> - Create helper functions to check if a position is valid (within bounds and not taken)
> - Include logic to prevent pieces from rotating into occupied spaces or outside boundaries
> - Add debugging console.log statements to track piece states

#### Prompt 6: Line Clearing and Scoring System
*Implements the core Tetris mechanic of clearing completed lines and updating the score.*
> Create the line clearing system for Tetris:
> - Write a function addScore() that checks for completed rows after each piece freezes
> - A completed row has all 10 squares with the "taken" class
> - When a row is completed: remove all "taken" and "tetromino" classes from that row, remove the row's divs from the DOM, create 10 new empty divs at the top of the grid
> - Update the score by 10 points for each cleared line
> - Handle multiple line clears simultaneously (double, triple, tetris)
> - Update the score display in the DOM after each clear
> - Add visual feedback or animations for line clearing
> - Ensure the grid maintains exactly 200 squares after clearing lines

#### Prompt 7: Game State Management
*Creates start/pause functionality and overall game state control.*
> Implement complete game state management for Tetris:
> - Create start/pause functionality tied to the start button
> - Track game state variables: isGameRunning, timerId, gameOver
> - Implement proper game initialization that resets score, clears grid, and spawns first piece
> - Add game over screen with option to restart
> - Create a function to reset the entire game state
> - Implement proper cleanup when pausing (clear intervals, save state)
> - Add keyboard controls for pausing (spacebar) and restarting (R key)
> - Include error handling for rapid button clicks or invalid game states
> - Add local storage to save high scores between sessions

#### Prompt 8: Testing and Enhancement Features
*Provides a comprehensive testing framework and suggests game improvements.*
> Create a testing and enhancement system for the Tetris game:
> - Write automated tests that verify: pieces spawn correctly, movement respects boundaries, rotation works in all positions, lines clear properly, score updates correctly
> - Add debug mode with console logging for piece positions and game events
> - Implement enhancements: next piece preview, hold piece functionality, increasing speed levels, different scoring for different line clears (single=100, double=300, triple=500, tetris=800)
> - Add sound effects using Web Audio API for piece drop, line clear, game over
> - Create visual improvements: smooth piece movement animations, particle effects for line clears, better color scheme
> - Add mobile touch controls for playing on phones/tablets
> - Include performance monitoring to ensure smooth 60fps gameplay

### Links & Resources
- [freeCodeCamp.org](https://www.freecodecamp.org) - Source of the tutorial and additional programming resources
- [Original YouTube Tutorial](https://www.youtube.com/watch?v=YqREHU0pvUc) - Direct link to the Tetris coding tutorial

### Tags
`#javascript` `#game-development` `#tutorial` `#beginner-coding` `#html-css` `#dom-manipulation`

### Category
Game Development

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
