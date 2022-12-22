from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.models_user import User
from flask_app.models.models_post import Post

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    all = Post.get_all_who_liked()
    return render_template("dashboard.html", user = user, all = all)

# Resources Page
@app.route('/resources')
def resources():
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    all = Post.get_all_who_liked()
    return render_template("resources.html", user = user, all = all)

# Messages page
@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    all = Post.get_all_who_liked()
    return render_template("messages.html", user = user, all = all)

# Create a new post page
@app.route('/new_post')
def new_post():
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    return render_template('new_post.html', user = user)

# Create Post, adds to db
@app.route('/create_post', methods=['POST'])
def create_post():
    data = {
        'title' : request.form['title'],
        'content' : request.form['content'],
        'user_id' : session['user_id'],
    }
    post = Post.create_post(data)
    return redirect('/dashboard')

# show post
@app.route('/show_post/<int:post_id>')
def show_post(post_id):
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    data = {
        'id' : post_id
    }
    user = User.get_by_id(user_data)
    post = Post.get_one(data)
    return render_template("show.html", user = user, post = post)

# Like a post
@app.route('/like_post/<int:post_id>')
def like_post(post_id):
    data = {
        'post_id' : post_id,
        'user_id' : session['user_id']
    }
    Post.like_post(data)
    return redirect('/dashboard')

# Comment on a post
@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    data = {
        'post_id' : post_id,
        'user_id' : session['user_id']
    }
    Post.comment(data)
    return redirect('/show<int:post_id>')

# Dislike a post
@app.route('/dislike_post/<int:post_id>')
def dislike_post(post_id):
    data = {
        'post_id' : post_id,
        'user_id' : session['user_id']
    }
    Post.dislike_post(data)
    return redirect('/dashboard')

# Edit Post
@app.route('/edit_post/<int:post_id>')
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    data = {
        'id' : post_id
    }
    user = User.get_by_id(user_data)
    post = Post.get_one(data)
    return render_template("edit_post.html", user = user, post = post)

# Update one post
@app.route('/update_post/<int:post_id>', methods = ['POST'])
def update_post(post_id):
    Post.update_post(request.form, post_id)
    return redirect('/dashboard')

# delete a post
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    data = {
        'id' : post_id
    }
    Post.delete_post(data)
    return redirect('/dashboard')