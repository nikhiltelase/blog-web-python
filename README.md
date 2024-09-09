# Blog Application

## Description

This is a web-based blog application built with Python and Flask. It allows users to view blog posts, add comments, and interact with various features. The application is designed to provide a clean and functional interface for both administrators and users to manage and view blog content.

## Output Video

For a demonstration of the project, watch the output video below:

[![Video Thumbnail](https://img.youtube.com/vi/GOt6FxsuUZI/hqdefault.jpg)](https://www.youtube.com/watch?v=GOt6FxsuUZI)
click on image to play video👆

## Features

- **View Blog Posts:** Users can browse through a list of blog posts, each with a title, subtitle, and content.
- **Add Comments:** Authenticated users can add comments to blog posts.
- **Comment Management:** Comments are displayed in reverse chronological order.
- **User Authentication:** Users must log in to add comments.
- **Dynamic Content:** Blog posts and comments are dynamically rendered based on the database.

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- A virtual environment tool (e.g., `venv`)

### Setting Up the Project

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/nikhiltelase/blog-web-python.git
    ```

2. **Navigate to the Project Directory:**
    ```bash
    cd blog-web-python
    ```

3. **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install Required Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up the Database:**
    ```bash
    flask db upgrade
    ```

6. **Run the Application:**
    ```bash
    flask run
    ```

7. **Navigate to** `http://127.0.0.1:5000` **to view the application.**

## Usage

- **Viewing Posts:** Browse through the main page to view a list of blog posts.
- **Adding Comments:** Log in to add comments to a blog post. The comment form is available at the bottom of each post.
- **Managing Posts and Comments:** Admins can manage blog posts and comments through the admin interface.


## Code Overview

- **Routes:**
  - `/post/<int:post_id>`: Displays a specific blog post along with comments and a form to add new comments.

- **Models:**
  - `BlogPost`: Represents a blog post with attributes like title, subtitle, and content.
  - `Comment`: Represents a comment with attributes like text, author, and associated blog post.

- **Forms:**
  - `CommentForm`: Used for adding comments to blog posts.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. **Fork the Repository.**
2. **Create a New Branch:**
    ```bash
    git checkout -b feature-branch
    ```
3. **Make Your Changes and Commit:**
    ```bash
    git commit -am 'Add new feature'
    ```
4. **Push to the Branch:**
    ```bash
    git push origin feature-branch
    ```
5. **Create a Pull Request.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Flask:** The web framework used for building the application.
- **SQLAlchemy:** The ORM used for database management.
