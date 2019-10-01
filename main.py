from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/cvw_db'
db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
# 
#     def __repr__(self):
#         return '<User %r>' % self.username


class Cipher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plaintext = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(32), nullable=True)
    method = db.Column(db.String(10), nullable=False)
    nochar = db.Column(db.Integer, nullable=True)
    rotby = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Cipher %r>' % self.id


db.create_all()  # create all the tables


# db.create_all()
# admin = User(username='admin', email='admin@example.com')
# guest = User(username='guest', email='guest@example.com')
# db.session.add(admin)
# db.session.commit()

# print User.query.filter_by(username='admin').first().email


@app.route('/')
def index():
    return 'Welcome!'


@app.route('/form')
def register():
    return render_template('form/index.html')


if __name__ == '__main__':
    app.run()
