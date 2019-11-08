from flask import render_template, url_for, redirect, request
from app import app, db, bcrypt, socketio
from app.forms import RegistrationForm, LoginForm, MessageForm
from app.database import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit


@app.route('/')
def index():
    return render_template("index.html", title="home")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            if nextPage:
                return redirect(nextPage)
            else:
                return redirect(url_for('index'))
        else:
            return render_template("login.html", title='login', form=form)
    return render_template("login.html", title='login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("register.html", title='Register', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/rooms", methods=['GET', 'POST'])
@login_required
def rooms():
    form = MessageForm()
    if form.validate_on_submit():
        print(form.message.data)
        emit('message', {'msg': current_user.username +
                         ':' + form.message.data})
        print(form.message.data)
    return render_template("rooms.html", title='Rooms', form=form)


@socketio.on('joined')
def joined(message):

    emit('status', {'msg': current_user.username +
                    ' has joined the room.'})


@socketio.on('left')
def left(message):
    emit('status', {'msg': current_user.username +
                    ' has left the room.'})


@socketio.on('message_handler')
def HandleMessage(message, methods=['GET', 'POST']):
    message['user_name'] = current_user.username
    socketio.emit('message', message)
