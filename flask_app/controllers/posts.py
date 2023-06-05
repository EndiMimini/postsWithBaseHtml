from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
import os
from flask import render_template, redirect, session, request, flash, jsonify
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename

# Check if the format is right 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add/post')
def addPost():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        return render_template('addPost.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/post', methods = ['POST'])
def createPost():
    if 'user_id' in session:
        if not Post.validate_post(request.form):
            return redirect(request.referrer)
        

        if not request.files['image']:
            flash('Post image is required!', 'postImage')
            return redirect(request.referrer)
   
        image = request.files['image']
        if not allowed_file(image.filename):
            flash('Image should be in png, jpg, jpeg format!', 'postImage')
            return redirect(request.referrer)
        
        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        

        data = {
            'title': request.form['title'],
            'content': request.form['content'],
            'user_id': session['user_id'],
            'image': filename1
        }
        Post.save(data)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/edit/post/<int:id>')
def editPost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data)
        if loggedUser['id'] == post['user_id']:
            return render_template('editPost.html', loggedUser = loggedUser, post= post)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/post/<int:id>')
def viewPost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data)
        likesNr = Post.get_post_likers(data)
        print('/////////////////////////////////////////')
        print(likesNr)
        return render_template('showOne.html', loggedUser = loggedUser, post= post, likesNr= likesNr)
    return redirect('/')

@app.route('/edit/post/<int:id>', methods = ['POST'])
def updatePost(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data1)
        if loggedUser['id'] == post['user_id']:
            if not Post.validate_post(request.form):
                return redirect(request.referrer)
            data = {
                'title': request.form['title'],
                'content': request.form['content'],
                'post_id': id
            }
            Post.update(data)
            return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')

@app.route('/delete/post/<int:id>')
def deletePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data)
        if loggedUser['id'] == post['user_id']:
            Post.deleteAllLikes(data)
            Post.delete(data)
            return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')

@app.route('/like/<int:id>')
def likePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        likedPost = User.get_user_liked_posts(data)
        if id not in likedPost:
            Post.addLike(data)
            num_likes = len(Post.get_num_likes(data))
            
            return jsonify({'likesCount': num_likes})

    return jsonify({'error': 'User not authenticated'})

@app.route('/unlike/<int:id>')
def unlikePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        Post.unLike(data)
        return redirect(request.referrer)
    return redirect('/')
