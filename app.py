from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user

from datetime import datetime as dt
import db

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def none():
    return redirect(app.config['ROOT_URL'])

@app.route('/admin', methods=('GET', 'POST'))
@login_required
def admin():
    if request.method == 'POST':
        nick, address = request.form['nick'], request.form['address']

        if not nick or not address:
            flash('Missing either URL nick or address.')
            return redirect(url_for('admin'))
        if nick == 'admin':
            flash("You can't replace /admin!")
            return redirect(url_for('admin'))

        if address[:7] != 'http://' and address[:8] != 'https://':
            address = "https://" + address

        db.insert(nick, address)

    all_links = []
    for link in db.select_all():
        link = dict(link)
        link['created'] = dt.strftime(link['created'], '%b %e, %Y @ %H:%M')
        all_links.append(link)

    return render_template('admin.html', all_links=all_links)

@app.route('/<nick>')
def url_redirect(nick):
    out = db.get(nick)
    if not out:
        abort(404)
    return redirect(out)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('e404.html'), 404

# AUTHENTICATION

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id=''):
    user = UserMixin()
    user.id = 'user'
    return user

@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash("You're already logged in.")
        return redirect(url_for('admin'))

    if request.method == 'POST':
        if request.form.get('pass') == app.config['ADMIN_PASS']:
            user = load_user()
            login_user(user)
            return redirect(url_for('admin'))
        flash('Incorrect password.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("You're logged out.")
    return redirect(url_for('login'))