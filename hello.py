from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hsiaoguo:Qwerzxcv123@localhost/flasky'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, role_id=3):
        self.username = username
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.username


class Phone(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64))
    uhash = db.Column(db.String(32), db.ForeignKey('idens.uhash'))

    def __repr__(self):
        return '<Phone %r>' % self.phone

class Iden(db.Model):
    __tablename__ = 'idens'
    idd = db.Column(db.Integer, primary_key=True)
    UID = db.Column(db.String(200))
    _version_ = db.Column(db.String(200))
    addresses = db.Column(db.String(300))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    finished = db.Column(db.Integer)
    firstname = db.Column(db.String(50))
    id = db.Column(db.Integer)
    lastname = db.Column(db.String(50))
    locality = db.Column(db.String(50))
    middlename = db.Column(db.String(50))
    nameid = db.Column(db.String(20))
    phone = db.Column(db.String(300))
    postcode = db.Column(db.String(10))
    region = db.Column(db.String(10))
    relatives = db.Column(db.String(100))
    street  =db.Column(db.String(200))
    ups = db.Column(db.String(10))
    uhash = db.Column(db.String(32))
    phones = db.relationship('Phone', backref='iden')

    def __repr__(self):
        return '<Iden %r>' % self.UID


class NameForm(FlaskForm):
    name = StringField('Input the phone number here:',  validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            session['result'] = None
        else:
            session['known'] = True
            session['result'] = str(user.username)+'\t'+str(user.role.name)
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), result=session.get('result'))
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        toQuery = re.sub('\D', '', form.name.data)
        user = Phone.query.filter_by(phone=toQuery).first()
        if user is None:
            session['result'] = "There is no results"
            db.session.commit()
        else:
            session['result'] = str(user.phone)+'\t'+str(user.iden.UID)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, result=session.get('result'))

if __name__ == "__main__":
    app.run()

