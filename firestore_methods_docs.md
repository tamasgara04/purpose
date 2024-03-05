## Code Documentation

### Overview
This code defines several classes for interacting with Firestore, including classes for users, API users, posts, comments, and likes. It also provides methods for adding, deleting, and retrieving data from Firestore.

### Dependencies
- **firebase_admin**: Python library for Firebase.
- **dotenv**: Python library for loading environment variables from a .env file.
- **os**: Module for interacting with the operating system.
- **datetime**: Module for working with dates and times.

### Classes
1. **User**: Represents a user with name and email attributes.
2. **APIUser**: Represents an API user with username and password attributes.
3. **Post**: Represents a post with title, content, user ID, and timestamp attributes.
4. **Comment**: Represents a comment with content, user ID, and timestamp attributes.
5. **Like**: Represents a like with user ID attribute.

### Firestore Methods
- **__init__**: Initializes Firebase Admin SDK and Firestore client.
- **add_user**: Adds a user to Firestore.
- **add_api_user**: Adds an API user to Firestore.
- **add_post**: Adds a post to Firestore.
- **add_comment**: Adds a comment to a post in Firestore.
- **add_like**: Adds a like to a post in Firestore.
- **delete_user**: Deletes a user and associated data from Firestore.
- **delete_post**: Deletes a post from Firestore.
- **delete_comment**: Deletes a comment from a post in Firestore.
- **delete_like**: Deletes a like from a post in Firestore.
- **get_user_posts**: Retrieves all posts for a user from Firestore.
- **get_post_comments**: Retrieves all comments for a post from Firestore.
- **get_post_likes**: Retrieves all likes for a post from Firestore.
- **get_all_users**: Retrieves all users from Firestore.
- **get_user_id_from_email**: Retrieves the user ID from Firestore based on email.
- **get_all_api_users**: Retrieves all API users from Firestore.

### Execution
- Initializes Firestore methods with Firebase credentials from environment variables.
- Creates instances of User, APIUser, Post, Comment, and Like classes.
- Adds instances to Firestore using Firestore methods.
- Optionally, deletes a user and associated data from Firestore.

### Note
- Ensure correct setup and authentication with Firebase Admin SDK.
- Verify Firestore data model and document structure for compatibility.
- Environment variables should be properly configured for Firebase credentials.
