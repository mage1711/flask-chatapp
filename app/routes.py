from flask import render_template, url_for, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.database import User
from flask_login import login_user, current_user, logout_user, login_required


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


@app.route("/rooms")
@login_required
def rooms():
    return render_template('rooms.html', title='Rooms')
