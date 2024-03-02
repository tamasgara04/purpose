import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Initialize Firebase Admin SDK
json_path = os.path.join(os.getcwd(), "purpose-tamas-firebase-adminsdk-bmj7j-5712f0f0a3.json")
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email
        }
    
class APIUser:
    def __init__(self, name, password):
        self.username = name
        self.password = password

    def to_dict(self):
        return {
            "username": self.name,
            "password": self.password
        }

class Post:
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "timestamp": self.timestamp
        }

class Comment:
    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "content": self.content,
            "user_id": self.user_id,
            "timestamp": self.timestamp
        }

class Like:
    def __init__(self, user_id):
        self.user_id = user_id

    def to_dict(self):
        return {
            "user_id": self.user_id
        }

# Add a user to Firestore
def add_user(user):
    user_ref = db.collection('users').add(user.to_dict())
    return user_ref[1].id

# Add a API user to Firestore
def add_api_user(user):
    user_ref = db.collection('api_users').add(user.to_dict())
    return user_ref[1].id

# Add a post to Firestore
def add_post(post):
    post_ref = db.collection('posts').add(post.to_dict())
    return post_ref[1].id

# Add a comment to a post in Firestore
def add_comment(post_id, comment):
    comment_ref = db.collection('posts').document(post_id).collection('comments').add(comment.to_dict())
    return comment_ref[1].id

# Add a like to a post in Firestore
def add_like(post_id, like):
    like_ref = db.collection('posts').document(post_id).collection('likes').add(like.to_dict())
    return like_ref[1].id

# Delete a user and all associated data from Firestore
def delete_user(user_id):
    # Delete user document
    db.collection('users').document(user_id).delete()

    # Delete user's posts
    posts_ref = db.collection('posts').where('user_id', '==', user_id).stream()
    for post in posts_ref:
        post_id = post.id
        # Delete post
        delete_post(post_id)
        # Delete comments of the post
        comments_ref = db.collection('posts').document(post_id).collection('comments').stream()
        for comment in comments_ref:
            delete_comment(post_id, comment.id)
        # Delete likes of the post
        likes_ref = db.collection('posts').document(post_id).collection('likes').stream()
        for like in likes_ref:
            delete_like(post_id, like.id)

# Delete a API user from Firestore
def delete_post(user_id):
    db.collection('api_users').document(user_id).delete()

# Delete a post from Firestore
def delete_post(post_id):
    db.collection('posts').document(post_id).delete()

# Delete a comment from a post in Firestore
def delete_comment(post_id, comment_id):
    db.collection('posts').document(post_id).collection('comments').document(comment_id).delete()

# Delete a like from a post in Firestore
def delete_like(post_id, like_id):
    db.collection('posts').document(post_id).collection('likes').document(like_id).delete()

# Get all posts for a user from Firestore
def get_user_posts(user_id):
    posts_ref = db.collection('posts').where('user_id', '==', user_id).stream()
    posts = [post.to_dict() for post in posts_ref]
    return posts

# Get all comments for a post from Firestore
def get_post_comments(post_id):
    comments_ref = db.collection('posts').document(post_id).collection('comments').stream()
    comments = [comment.to_dict() for comment in comments_ref]
    return comments

# Get all likes for a post from Firestore
def get_post_likes(post_id):
    likes_ref = db.collection('posts').document(post_id).collection('likes').stream()
    likes = [like.to_dict() for like in likes_ref]
    return likes

# Get all users from Firestore
def get_all_users():
    users_ref = db.collection('users').stream()
    users = [user.to_dict() for user in users_ref]
    return users

def get_user_id_from_email(email):
    # Perform a query to retrieve the user document based on email
    query = db.collection('users').where('email', '==', email).stream()

    # Iterate through the query results
    for user_doc in query:
        # Extract the user ID from the retrieved user document
        user_id = user_doc.id
        return user_id

    # Return None if no user with the given email is found
    return None

def get_all_api_users():
    users_ref = db.collection('api_users').stream()
    users = [user.to_dict() for user in users_ref]
    return users

if __name__ == "__main__":
    # Create a user
    user1 = User(name="Alice", email="alice@example.com")

    # Add the user to Firestore
    user_id = add_user(user1)
    print("User ID:", user_id)

    # Create a post
    post1 = Post(title="First Post", content="Hello World!", user_id=user_id)

    # Add the post to Firestore
    post_id = add_post(post1)
    print("Post ID:", post_id)

    # Create a comment
    comment1 = Comment(content="Great post!", user_id=user_id)

    # Add the comment to the post in Firestore
    comment_id = add_comment(post_id, comment1)
    print("Comment ID:", comment_id)

    # Create a like
    like1 = Like(user_id=user_id)

    # Add the like to the post in Firestore
    like_id = add_like(post_id, like1)
    print("Like ID:", like_id)

    #delete_user(user_id)
