from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, Blueprint
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db


auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static')

'''AUTH'''


@auth.route('/sign-up-login', methods=['GET', 'POST'])
def sign_up_login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        login_email = request.form.get('login-email')
        login_password = request.form.get('login-password')

        if login_email == None and login_password == None:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists!',
                      category='error')
            elif len(email) < 8:
                flash('Hey! email is too short!', category='error')
            elif len(username) < 4:
                flash('Username is too short!', category='error')
            elif len(password1) < 6:
                flash('Password is too short!', category='error')
            elif password1 != password2:
                flash('Passwords must be the same buddy!', category='error')
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully created account!', category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))

        else:
            user = User.query.filter_by(email=login_email).first()
            if user:
                if check_password_hash(user.password, login_password):
                    flash('Logged in successfully', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Hey! passwords must match.', category='error')
            else:
                flash('This user does not exist, please try again', category='error')

    return render_template('sign_up.html', user=current_user)


@auth.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.sign_up_login'))
