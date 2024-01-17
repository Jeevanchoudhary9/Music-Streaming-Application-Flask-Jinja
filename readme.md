# Music Streaming Application

## Project Overview

Welcome to the Music Streaming Application, a cutting-edge platform designed to immerse users in an unparalleled audio experience. This dynamic application caters to music enthusiasts, providing not only a gateway to discover and listen to their favorite tunes but also a canvas to curate personalized playlists.

## Project Goals

The Music Streaming Application sets out to accomplish the following objectives:

- **Intuitive Design:** Develop a visually appealing and user-friendly music streaming website.
- **User Profiles:** Implement both general user profiles and dedicated creator profiles for music artists.
- **Song Management:** Enable robust features for adding, editing, and organizing users' music collections.
- **Playlist Management:** Provide seamless capabilities for creating and curating personalized playlists.
- **Powerful Search:** Implement a sophisticated search functionality for effortless song discovery.
- **Audio File Support:** Support the addition and playback of diverse .mp3 audio files.
- **Interaction Features:** Create functionality for users to interact with albums, songs, and playlists.
- **CRUD Operations:** Implement CRUD (Create, Read, Update, Delete) operations for both songs and playlists.
- **Admin Dashboard:** Develop features for generating insightful graphs and statistics for administrators.
- **Validation:** Implement stringent validation for form inputs, ensuring data integrity.
- **Aesthetics:** Enhance the website's visual appeal and user interface for an enjoyable experience.
- **Authentication:** Establish a secure login system for user accounts and authentication.
- **Admin Empowerment:** Provide tools for administrators to flag and manage content from creators.

## Technology Stack

The Music Streaming Application leverages cutting-edge technologies and tools, including:

- **Flask:** A robust Python web framework for scalable web applications.
- **SQLite:** A lightweight and efficient relational database system, ideal for managing music data.
- **HTML:** The standard markup language for structuring web content.
- **TAILWINDCSS:** A utility-first CSS framework for designing and styling web pages.
- **JavaScript:** A versatile scripting language for adding interactivity and dynamic features.

## How to Run the Web App Locally

To run the Music Streaming Application locally on your machine, follow these steps:

1. **Create a Virtual Environment:**
    ```bash
    python3 -m venv env
    ```

2. **Activate the Virtual Environment:**
    ```bash
    source env/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Web App:**
    ```bash
    flask run
    ```

Note: For Windows users encountering issues, consider using Linux or macOS for a smoother experience.

## Project Structure

```bash
Music Streaming Application/
    ├── instance/
    |   └──  db.sqlite3
    ├── static/
    |   └──  css/
    |        └──  style.css
    ├── templates/
    |   ├── dashboard/
    |   |   ├── admin_album_allsongs.html
    |   |   ├── admin_album.html
    |   |   ├── admin_album_alltracks.html
    |   |   ├── admin_creator_management.html
    |   |   ├── admin_dashboard.html
    |   |   ├── admin_album_allsongs.html
    |   |   └──  ...
    |   ├── layout/
    |   |   ├── layout_admin.html
    |   |   ├── layout.html
    |   |   ├── navbar_admin.html
    |   |   └── navbar.html
    |   ├── login_register/
    |   |   ├── login_admin.html
    |   |   ├── login.html
    |   |   └── register.html
    |   └── welcome.html
    ├── uploads/
    |   ├──  lyrics_id.txt
    |   └──  song_id.mp3
    ├── app.py
    ├── .env
    ├── auth.py
    ├── config.py
    ├── models.py
    ├── requirements.txt
    └── routes.txt
```

## Screenshots

*Include screenshots of your application in action.*

## Conclusion

With a compelling technology stack and a meticulously planned development process, the Music Streaming Application is poised to revolutionize the music streaming experience. This platform caters to the diverse needs of music enthusiasts, offering an immersive and enjoyable journey through the world of sound.

## Document Author

Jeevan Choudhary
