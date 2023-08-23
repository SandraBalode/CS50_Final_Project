# FitBudi
#### Video Demo:  <https://youtu.be/RBELO1fGfBU>
## Fitness App - CS50 Final Project

## Overview

Welcome to the Fitness App, an exceptional digital fitness companion meticulously developed as the crowning achievement of the CS50 final project. This all-encompassing application serves as a dedicated guide on users' transformative health and fitness journeys. Empowering each individual, the app offers personalized workout tracking, robust goal establishment, and vibrant visualization of their advancement. Powered by the synergy of Flask, Jinja templating, Python, HTML, JavaScript, and CSS, the Fitness App seamlessly integrates Bootstrap and Chart.js, ensuring a user-friendly and captivating experience across devices. The meticulously organized file structure encompasses essential components, including user authentication, dynamic data presentation, and interactive visual aids. With a database storing user achievements and workout progress, the Fitness App proves to be a powerful, intuitive, and aesthetically engaging tool that uplifts and inspires users on their path to better health.

## Features

- **User Registration and Authentication:** Users can create accounts, log in securely, and log out. Passwords are hashed for security.
- **Personalized Dashboards:** Each user has a unique dashboard where they can view their workout history and weight goal progress.
- **Workout Logging:** Users can log their workouts, including exercise details, sets, reps, and weights.
- **Exercise Library:** A library of exercises with descriptions, images, and videos helps users learn proper techniques.
- **Progress Tracking:** Interactive charts powered by Chart.js provide visual representations of users' progress over time.
- **Goal Setting:** Users can set specific weight goals and track their achievements.
- **Responsive Design:** Bootstrap is implemented for a seamless and responsive user experience across devices.

## Installation

1. Clone this repository: `git clone https://github.com/SandraBalode/CS50_Final_Project.git`
2. Navigate to the project directory: `cd CS50_Final_Project`
3. Install required dependencies: `pip install -r requirements.txt`
5. Run the app: `python -m flask run`

## Files Included

- `_pycache_` folder: Stores compiled Python files for faster execution.
- `flask_session` folder: Stores session files for user authentication.
- `node_modules` folder: Contains dependencies for Node.js packages (e.g., JavaScript libraries).
- `static` folder: Holds static assets such as images, videos, JavaScript, and CSS.
    - `img` folder: Contains images used in the app.
    - `video` folder: Contains videos for instructional content.
    - `interactions.js`: JavaScript code handling interactive features.
    - `stylesheet.css`: Custom CSS for styling.
- `templates` folder: Holds all the HTML templates used in the app.
- `app.py`: The main Python application file that contains the app's routes and logic.
- `database.db`: The SQLite database storing user information, workout data, and progress.
- `helpers.py`: A Python script containing helper functions.
- `queries.py`: A Python script with SQLite queries used in the app.
- `package.json` and `package-lock.json`: Configuration files for Node.js packages.

## Usage

1. Open your web browser and navigate to the specified port.
2. Register an account or log in if you already have one.
3. Explore the exercise library, log your workouts, set goals, and view your progress.
4. Enjoy your fitness journey with our app!

## Credits

- Developed by Sandra Balode
- Built using Flask, Jinja templating, Python, HTML, JavaScript, CSS
- Utilizes Bootstrap for responsive design and Chart.js for data visualization