# The Project Formerly Known as Twitter

This repository contains the final project for the *Internet and Distributed Computing* course. The assignment was to create a scaled-down version of Twitter with core micro-blogging functionality, including user authentication, posting, replying, feeds, and profile picture uploads.

The project was deployed using [PythonAnywhere](https://www.pythonanywhere.com) and AWS cloud services for data storage and media handling.

## 🚀 Features

### User Authentication
* Sign up with email, username, and password
* Login using email or username
* Session-based access control

### Posting System
* Create new posts
* Reply to existing posts
* View individual post threads

### Feeds
* Global feed showing recent posts from all users
* User-specific profile feeds showing only their posts

### Profile Management
* Upload a profile picture
* Display user photo, username, and posts on profile page
* Default avatar if no image is uploaded

## 🛠 Technologies Used

### Frontend
* HTML / CSS / Javascript

### Backend
* Python / Flask
* RESTful API design

### Cloud Services
* **AWS DynamoDB**: Stores user data, posts, and replies
* **AWS S3**: Stores uploaded profile images

### Hosting
* [PythonAnywhere](https://www.pythonanywhere.com): Hosts the web application at [jr09427n.pythonanywhere.com/static/final_signup.html](https://jr09427n.pythonanywhere.com/static/final_signup.html)

## 🔐 Authentication & Routing
* If a user is not logged in and attepts to access a restricted page, they are restricted to the login/signup screen.
* After successful login/signup, users are redirected to their own profile.

## 📷 Profile Pictures
* Uploaded via the profile page using a file input
* Stored securely on AWS S3
* Fallback image shown if none uploaded

## 💻 Screenshots
### Home Page
<p align="center"> <img src="homepage.png" alt="Home Page" width="600"/> </p>

### Profile Page
<p align="center"> <img src="profile.png" alt="Profile Page" width="600"/> </p>

### Feed Page
<p align="center"> <img src="feed.png" alt="Feed Page" width="600"/> </p>

## 👥 Team
Developed by: **Jean-Sebastien Rateau**
Course: Internet and Distributed Computing
Instructor: Carmine Guida
