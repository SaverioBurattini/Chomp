  <div class="center-content">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Chomp_gameplay.png/1920px-Chomp_gameplay.png" alt="Chomp Game Logo" width="600"/>
  </div>

  <h2>General Information</h2>
  <ul>
      <li><strong>University</strong>: "G. d'Annunzio" University (Pescara, Italy)</li>
      <li><strong>Degree Program</strong>: Computer Science, First Year (A.Y. 2024/2025)</li>
      <li><strong>Course</strong>: Programming Laboratory</li>
      <li><strong>Professor</strong>: Gianluca Amato</li>
  </ul>

  <h2>Description</h2>
  <p>
      This project implements the classic game of Chomp, a two-player strategy game played on a rectangular grid that represents a chocolate bar. The game follows the following rules:
  </p>
  <ol>
      <li>Players take turns choosing a square of chocolate</li>
      <li>When a square is selected, that piece and all pieces below and to the right are "eaten" (removed)</li>
      <li>The top-left square is "poisoned" (marked in green)</li>
      <li>The player who is forced to eat the poisoned square loses</li>
  </ol>

  <h2>Features</h2>
  <ul>
      <li>Three game modes:
          <ul>
              <li>Player vs Player</li>
              <li>Player vs CPU</li>
              <li>CPU vs CPU</li>
          </ul>
      </li>
      <li>Interactive graphical interface using ezgraphics</li>
      <li>Visual feedback showing whose turn it is</li>
      <li>Game state tracking with appropriate win conditions</li>
  </ul>

  <h2>Project Structure</h2>
  <pre><code>
├── main.py                    # Entry point
├── lib/
│   ├── core_functions.py      # Core game logic and control flow
│   ├── graphics_functions.py  # Functions for drawing game elements
│   └── matrix_functions.py    # Operations on the game matrix
├── vars/
│   ├── global_vars.py         # Global constants and configuration
│   └── game_vars.py           # Game state variables
├── assets/                    # Contains game assets (e.g., the chocolate image)
│   ├── img/
│       └── chocolate.png      # Chocolate image
</code></pre>

  <h2>How to Play</h2>
  <ol>
      <li>Run <code>main.py</code> to start the game</li>
      <li>Click on one of three sections to select a game mode</li>
      <li>In player modes, click on a chocolate square to make a move</li>
      <li>The game continues until one player is forced to take the poisoned square</li>
  </ol>

  <h2>Implementation Details</h2>
  <p>
      The game uses a matrix representation for the chocolate bar, where:
  </p>
  <ul>
      <li><code>1</code> represents an uneaten piece of chocolate</li>
      <li><code>0</code> represents an eaten piece</li>
  </ul>
  <p>
      The game tracks valid moves using the <code>last_valid_move</code> variable, which gets updated after each turn to ensure CPU players make legal moves within the current boundaries of the remaining chocolate.
  </p>
  <p>
      The turn system alternates between players (or CPU) after each valid move, and the interface is updated to reflect the current game state.
  </p>
