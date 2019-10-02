from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from caesar import encrypt as caesar_encrypt
from vigenere import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt
from monoalphabetic import generate_mapping as gen_alpha, encrypt as mono_encrypt, alpha_to_string as ats

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
    cipher = db.Column(db.String(255), nullable=False)
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
    # return render_template('form/index.html', plaintext=text, ciphertext=ciphertext, rot=rot, key=key,
    #                            decrypt_hide=True, last_method=method)
    return render_template('form/index.html', plaintext='', ciphertext='', rot=0, key='', decrypt_hide=True)


# TODO: Monoalphabetic Cipher


@app.route('/', methods=['POST'])
def home_post():
    decrypt_pressed = False
    text = request.form['plaintext']
    rot = int(request.form['rot'])
    key = request.form['key']
    method = request.form['encrypt-method']
    ciphertext = request.form['ciphertext']
    alpha = ""
    if request.form['submit_button'] == 'Encrypt':
        if method == 'mono':
            alphabet = gen_alpha()
            ciphertext = mono_encrypt(text, alphabet)
            alpha = ats(alphabet)
        else:
            ciphertext = caesar_encrypt(text, rot) if method == 'caesar' else vigenere_encrypt(text, key)
    elif request.form['submit_button'] == 'Decrypt':
        if method == 'mono':
            msg = "Mono Alphabetic cipher is not working for decryption"
            return render_template('form/index.html', plaintext=text, ciphertext=ciphertext, rot=rot, key=key,
                                   decrypt_hide=decrypt_pressed, last_method=method, msg=msg)
        decrypt_pressed = True
        text = caesar_encrypt(ciphertext, abs(
            26 - rot)) if method == 'caesar' else vigenere_decrypt(ciphertext, key)
    elif request.form['submit_button'] == 'Load Last':
        cipher_list = Cipher.query.filter_by(method=method).all()
        if len(cipher_list) > 0:
            last_cipher = cipher_list[len(cipher_list) - 1]
            text = ""
            ciphertext = last_cipher.cipher
            key = last_cipher.key
            rot = last_cipher.rotby
            method = last_cipher.method
        else:
            text = ''
            ciphertext = ''
            key = ''
            rot = 0
            method = ''
        return render_template('form/index.html', plaintext=text, ciphertext=ciphertext, rot=rot, key=key,
                               decrypt_hide=True, last_method=method)
    elif request.form['submit_button'] == 'Save':
        # Check for validity
        if ciphertext == caesar_encrypt(text, rot) if method == 'caesar' else vigenere_encrypt(text, key):
            new_cipher = Cipher(plaintext=text, cipher=ciphertext,
                                method=method, key=key, nochar=len(text), rotby=rot)
            db.session.add(new_cipher)
            db.session.commit()
            return render_template('form/index.html', plaintext='', ciphertext='', rot=0, key='', decrypt_hide=True)
        else:
            return "Invalid Cipher and Plaintext"
    return render_template('form/index.html', plaintext=text, ciphertext=ciphertext, rot=rot, key=key,
                           decrypt_hide=decrypt_pressed, last_method=method, alpha=alpha)

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


answers = ["Pikachu", "Charizard", "Squirtle", "Jigglypuff",
           "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]

Ducks = []


@app.route('/bruteforce')
def bruteforce():
    return render_template("form/index2.html", len=len(Ducks), answers=Ducks)


@app.route('/bruteforce', methods=['POST'])
def bruteforce_done():
    plaintexts = []
    ciphertext = request.form['cipher32']
    rot = 0
    for i in range(0, 26):
        text = caesar_encrypt(ciphertext, abs(26 - i))
        plaintexts.append(text)
    return render_template("form/index2.html", cipher32=ciphertext, len=len(plaintexts), answers=plaintexts)


# @app.route('/')
# def get_last():
#     cipher_list = Cipher.query.all()
#     if len(cipher_list) > 0:
#         last_cipher = cipher_list[len(cipher_list) - 1]
#         text = ""
#         ciphertext = last_cipher.cipher
#         key = last_cipher.key
#         rot = last_cipher.rotby
#         method = last_cipher.method
#     else:
#         text = ""
#         ciphertext = ""
#         key = ""
#         rot = ""
#         method = ""
#     return render_template('form/index.html', plaintext=text, ciphertext=ciphertext, rot=rot, key=key,
#                            decrypt_hide=True, last_method=method)


if __name__ == '__main__':
    app.run()
