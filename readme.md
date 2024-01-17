# Music Streaming Application

This is a music streaming application developed using Flask and SQLAlchemy for managing a vast collection of songs, albums, and playlists. The application focuses on providing a seamless experience for users, creators, and administrators while ensuring data security and efficient management.

## Features

- **User-centric Views**: The application provides an intuitive user dashboard where users can explore songs, albums, and playlists. They can interact by listening to music, reading lyrics, rating songs, and leaving comments.
  
- **Creator Dashboard**: Creators have dedicated functionalities for uploading songs, managing album creation, editing song information, and viewing ratings and comments.

- **Administrator Functions**: Administrators have access to monitor best-performing music, manage user interactions, and even block certain creators from uploading songs.

## Project Structure

The project's architecture follows a modular approach:

- **Instance Directory**: Houses the SQLite3 database and structured folders for streamlined data management.
  
- **Static Folder**: Contains tailwind CSS source files for styling purposes.
  
- **Templates Directory**: Hosts HTML files for diverse user views, including user_dashboard, manager_login, creator_register, and more.

- **Python Files**: Includes essential files such as app.py for application initialization, auth.py for user security, models.py for database management, and routes.py for linking page logic.

## Installation

To run the application locally:

1. Clone this repository.
2. Set up a virtual environment using `virtualenv`.
3. Install the required dependencies from `requirements.txt`.
4. Initialize the Flask application using `flask run`.

## Usage

Once the application is running:

- Access the user dashboard through the provided URL.
- Login with appropriate credentials (users, managers, creators, or administrators).
- administratos username-admin,password-admin
- for listener account create one
- Explore music, create playlists, rate songs, and enjoy a seamless music streaming experience.

