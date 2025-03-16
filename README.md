# Ball Collision Simulation

This project simulates the motion and collision of balls using Pygame and NumPy. The simulation includes fixed balls and user-added balls that interact with each other through collisions and boundary constraints.

## Features

- Simulates ball motion with gravity, friction, and wall collisions.
- Handles ball-to-ball collisions using impulse-based physics.
- Allows user to add new balls by clicking on the screen.
- Visualizes the simulation using Pygame.

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ball-collision.git
    cd ball-collision
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the simulation:
    ```sh
    python object-collision.py
    ```

2. The simulation window will open. You can add new balls by clicking on the screen.

## Project Structure

- `object-collision.py`: Main script to run the simulation.
- `ball_system.py`: Contains the `BallSystem` class that handles ball physics and collisions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- Pygame: https://www.pygame.org/
- NumPy: https://numpy.org/

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
