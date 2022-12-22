from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.models_user import User
from flask_app.models.models_message import Message
from flask_app.models import message
from flask import flash


@app.route("/messages/<int:user_id>")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    messages = Message.get_user_messages(session['user_id'])
    users = User.get_all()
    return render_template("messages.html",user = user, users = users, messages = messages)

@app.route('/post_message',methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect('/')
    Message.save(request.form)
    return redirect('/dashboard')

@app.route('/destroy/message/<int:message_id>')
def destroy_message(message_id):
    Message.destroy(message_id)
    return redirect('/dashboard')