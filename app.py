from flask import Flask, render_template, request, flash, redirect, url_for, abort

from datetime import datetime as dt
import db

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def none():
    return redirect(app.config['ROOT_URL'])

@app.route('/admin', methods=('GET', 'POST'))
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

    return render_template('index.html', all_links=all_links)

@app.route('/<nick>')
def url_redirect(nick):
    out = db.get(nick)
    if not out:
        abort(404)
    return redirect(out)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('e404.html'), 404