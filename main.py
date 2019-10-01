from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/cvw_db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# db.create_all()
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')
# db.session.add(admin)
# db.session.commit()

print User.query.filter_by(username='admin').first().email

@app.route('/')
def index():
    return 'This is index!'


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
