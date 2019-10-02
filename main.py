from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from caesar import encrypt as caesar_encrypt
from vigenere import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt

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


# db.create_all()  # create all the tables
# cipher = Cipher(plaintext="", method="", key="", nochar="", rotby="")


# db.create_all()
# admin = User(username='admin', email='admin@example.com')
# guest = User(username='guest', email='guest@example.com')
# db.session.add(admin)
# db.session.commit()

# print User.query.filter_by(username='admin').first().email


# @app.route('/')
# def index():
#     return '<h1> Welcome!<h1/>'


@app.route('/')
def home():
    lcipher = Cipher.query.all()
    print lcipher[len(lcipher) - 1].id
    return render_template('form/index.html', plaintext='', ciphertext='', rot=0, key='', decrypt_hide=True)


@app.route('/', methods=['POST'])
def handle_post():
    decrypt_pressed = False
    text = request.form['plaintext']
    rot = int(request.form['rot'])
    key = request.form['key']
    method = request.form['encrypt-method']
    ciphertext = request.form['ciphertext']
    if request.form['submit_button'] == 'Encrypt':
        ciphertext = caesar_encrypt(text, rot) if method == 'caesar' else vigenere_encrypt(text, key)
    elif request.form['submit_button'] == 'Decrypt':
        decrypt_pressed = True
        text = caesar_encrypt(ciphertext, abs(26 - rot)) if method == 'caesar' else vigenere_decrypt(ciphertext, key)
    elif request.form['submit_button'] == 'Save':
        # Check for validity
        if ciphertext == caesar_encrypt(text, rot) if method == 'caesar' else vigenere_encrypt(text, key):
            new_cipher = Cipher(plaintext=text, method=method, key=key, nochar=len(text), rotby=rot)
            db.session.add(new_cipher)
            db.session.commit()
            return render_template('form/index.html', plaintext='', ciphertext='', rot=0, key='', decrypt_hide=True)
        else:
            return "Invalid Cipher and Plaintext"

    return render_template('form/index.html', plaintext=text, ciphertext=ciphertext, rot=rot, key=key,
                           decrypt_hide=decrypt_pressed, last_method=method)

    # try:
    #     decrypt_pressed = bool(request.form['decrypt'])
    # except KeyError:
    #     decrypt_pressed = False
    # text = request.form['plaintext']
    # rot = int(request.form['rot'])
    # key = request.form['key']
    # method = request.form['encrypt-method']
    # if not decrypt_pressed:
    #     cipher = caesar_encrypt(text, rot) if method == 'caesar' else vigenere_encrypt(text, key)
    # else:
    #     cipher = caesar_encrypt(text, abs(26 - rot)) if method == 'caesar' \
    #         else vigenere_decrypt(text, key)
    # return render_template('form/index.html', plaintext=text, ciphertext=cipher, rot=rot, key=key,
    #                        decrypt_hide=decrypt_pressed, last_method=method)



if __name__ == '__main__':
    app.run()
