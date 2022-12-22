from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.models_user import User
from flask_app.models.models_post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_user')
def login_user():
    return render_template('login.html')

@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "occupation": request.form['occupation'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# Account
@app.route('/account/<int:user_id>')
def user_account(user_id):
    data = {
        'id' : user_id
    }
    user = User.get_by_id(data)
    posts = Post.all_posts_user(data)
    return render_template('account.html', user = user, posts = posts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')