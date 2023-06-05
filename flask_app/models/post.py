from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash



class Post:
    db_name = 'firstFullStack'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.image = data['image']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_post_by_id(cls, data):
        query = "SELECT * FROM posts WHERE posts.id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    #READ
    @classmethod
    def get_all(cls):
        query = "SELECT posts.id, posts.user_id, posts.title, posts.image, posts.content, users.first_name, users.last_name, COUNT(likes.post_id) as num_likes FROM posts  LEFT JOIN users ON posts.user_id = users.id LEFT JOIN likes ON posts.id = likes.post_id GROUP BY posts.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        posts = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for post in results:
                posts.append(post)
            return posts
        return posts
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (title, content, image, user_id) VALUES ( %(title)s, %(content)s, %(image)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET title = %(title)s, content = %(content)s WHERE posts.id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE posts.id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        #DELETE
    @classmethod
    def deleteAllLikes(cls, data):
        query = "DELETE FROM likes WHERE post_id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteAllUserLikes(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(person_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteAllUserPosts(cls, data):
        query = "DELETE FROM posts WHERE posts.user_id = %(person_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    
    #add like
    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (post_id, user_id) VALUES ( %(post_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def unLike(cls, data):
        query = "DELETE FROM likes WHERE post_id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_post_likers(cls, data):
        query = "SELECT * from likes LEFT JOIN users on likes.user_id = users.id WHERE post_id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfLikes = []
        if results:
            for row in results:
                nrOfLikes.append(row['email'])
            return nrOfLikes
        return nrOfLikes
    
    @classmethod
    def get_num_likes(cls, data):
        query = "SELECT COUNT(*) AS num_likes FROM likes WHERE likes.post_id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]['num_likes']
        return 0


    @staticmethod
    def validate_post(post):
        is_valid = True
        
        if len(post['title']) <2:
            flash('Post title should be more than 2 characters!', 'titlePost')
            is_valid= False
        if len(post['content']) <2:
            flash('Content should be more than 2 characters!', 'contentPost')
            is_valid= False
        return is_valid
        