from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint

db = "final_project_db"

class Post:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None
        self.user = []
        self.all_who_liked = []

# Create Post
    @classmethod
    def create_post(cls, data):
        query = """
                INSERT INTO posts (title, content, user_id)
                VALUES (%(title)s, %(content)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

# Display all posts
    @classmethod
    def all_posts(cls):
        query = """
                SELECT * FROM posts
                JOIN users ON users.id = posts.user_id
                """
        results = connectToMySQL(db).query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

# get one
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM posts
                JOIN users ON users.id = posts.user_id
                WHERE posts.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        post = cls(results[0])
        owner_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'occupation' : results[0]['occupation'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        }
        post.owner = User(owner_data)
        return post

# update
    @classmethod
    def update_post(cls, form_data, post_id):
        query = f"UPDATE posts SET title = %(title)s, content = %(content)s WHERE id = {post_id}"
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def all_posts_user(cls, data):
        query = """
                SELECT * FROM posts
                LEFT JOIN users
                ON users.id = posts.user_id
                WHERE users.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        posts = []
        for post in results:
            post_user = cls(post)
            user_data = {
                'id' : post['users.id'],
                'first_name' : post['first_name'],
                'last_name' : post['last_name'],
                'email' : post['email'],
                'occupation' : post['occupation'],
                'password' : post['password'],
                'created_at' : post['created_at'],
                'updated_at' : post['updated_at']
            }
            post_user.user = User(user_data)
            posts.append(post_user)
        return posts

    @classmethod
    def delete_post(cls, data):
        query = """
                DELETE FROM posts
                WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def like_post(cls, data):
        query = """
                INSERT INTO likes (user_id, post_id)
                VALUES (%(user_id)s, %(post_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_who_liked(cls):
        query = """
                SELECT * FROM posts
                JOIN users ON users.id = posts.user_id
                LEFT JOIN likes ON posts.id = likes.post_id
                LEFT JOIN users AS users2 ON users2.id = likes.user_id
                """
        results = connectToMySQL(db).query_db(query)
        pprint(results)
        likes = []
        for result in results:
            new_like = True
            liked_user_data = {
                'id' : result['users2.id'],
                'first_name' : result['users2.first_name'],
                'last_name' : result['users2.last_name'],
                'email' : result['users2.email'],
                'occupation' : result['users2.occupation'],
                'password' : result['users2.password'],
                'created_at' : result['users2.created_at'],
                'updated_at' : result['users2.updated_at']
            }
            if len(likes) > 0 and likes[len(likes)-1].id == result['id']:
                likes[len(likes)-1].all_who_liked.append(User(liked_user_data))
                new_like = False
            if new_like:
                like = cls(result)
                user_data = {
                    'id' : result['users.id'],
                    'first_name' : result['first_name'],
                    'last_name' : result['last_name'],
                    'email' : result['email'],
                    'occupation' : result['occupation'],
                    'password' : result['password'],
                    'created_at' : result['users.created_at'],
                    'updated_at' : result['users.updated_at']
                }
                user = User(user_data)
                like.user = user
                if result['users2.id'] is not None:
                    like.all_who_liked.append(User(liked_user_data))
                likes.append(like)
        pprint(likes)
        return likes

    @classmethod
    def dislike_post(cls, data):
        query = """
                DELETE FROM likes
                WHERE post_id = %(post_id)s
                AND user_id = %(user_id)s
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def comment(cls, data):
        query = """
                INSERT INTO comments (id, content, user_id, post_id)
                VALUES (%(id)s, %(content)s, %(user_id)s, %(post_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_who_commented(cls):
        query = """
                SELECT * FROM posts
                JOIN users ON users.id = posts.user_id
                LEFT JOIN comments ON posts.id = comments.post_id
                LEFT JOIN users AS users2 ON users2.id = comments.user_id
                """
        results = connectToMySQL(db).query_db(query)
        pprint(results)
        comments = ""
        for result in results:
            new_comment = True
            commented_user_data = {
                'id' : result['users2.id'],
                'first_name' : result['users2.first_name'],
                'last_name' : result['users2.last_name'],
                'email' : result['users2.email'],
                'occupation' : result['users2.occupation'],
                'password' : result['users2.password'],
                'created_at' : result['users2.created_at'],
                'updated_at' : result['users2.updated_at']
            }
            # if len(comments) > 0 and comments[len(comments)-1].id == result['id']:
            #     comments[len(comments)-1].all_who_commented.append(User(commented_user_data))
            #     new_comment = False
            if new_comment:
                comment = cls(result)
                user_data = {
                    'id' : result['users.id'],
                    'first_name' : result['first_name'],
                    'last_name' : result['last_name'],
                    'email' : result['email'],
                    'occupation' : result['occupation'],
                    'password' : result['password'],
                    'created_at' : result['users.created_at'],
                    'updated_at' : result['users.updated_at']
                }
                user = User(user_data)
                comment.user = user
                if result['users2.id'] is not None:
                    comment.all_who_commented.append(User(commented_user_data))
                comments.append(comment)
        pprint(comments)
        return comments