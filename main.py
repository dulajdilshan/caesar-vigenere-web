from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from vigenere import encrypt as vig_enc, decrypt as vig_dec
from caesar import encrypt as caesar_enc
from monoalphabetic import generate_mapping as gen_alpha, encrypt as mono_encrypt, alpha_to_string as alpha2string

app = Flask(__name__)
DB_TYPE = 'mysql'
USERNAME = 'root'
PASSWORD = ''
URL = '127.0.0.1:3306'
DB_NAME = 'ciphers_db'

SQLALCHEMY_DATABASE_URI = DB_TYPE + '://' + USERNAME + ':' + PASSWORD + '@' + URL + '/' + DB_NAME

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    enc_text = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(32), nullable=True)
    method = db.Column(db.String(10), nullable=False)
    shift = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Data %r>' % self.id


db.create_all()


# Page
@app.route('/')
def home_page():
    # return render_template('public__.html', plaintext='', ciphertext='', rot=0, key='', decrypt_hide=True)
    return redirect('/caesar', code=302)


# Page
@app.route('/caesar')
def caesar_page():
    # return render_template('caesar_public.html', text='', enc_text='', shift_by=0, decrypt_hide=True)
    return render_template('caesar_public.html', text='', enc_text='', shift=0)


# Page
@app.route('/vigenere')
def vigenere_page():
    return render_template('vigenere_public.html', text='', enc_text='', key='')


# Page
@app.route('/mono')
def mono_page():
    return render_template('mono_public.html', text='', enc_text='', alpha='')


# Page
@app.route('/bruteforce')
def bruteforce_page():
    empty = []
    return render_template("brute_public.html", len=len(empty), answers=empty)


# Controller
@app.route('/caesar', methods=['POST'])
def caesar_controller():
    text = request.form['text']
    shift = int(request.form['shift'])
    method = 'caesar'
    enc_text = request.form['enc_text']

    if request.form['submit_button'] == 'Encrypt':
        print "Came Here"
        enc_text = caesar_enc(text, shift)
    elif request.form['submit_button'] == 'Decrypt':
        text = caesar_enc(enc_text, abs(26 - shift))
    elif request.form['submit_button'] == 'Load Last':
        cipher_list = Data.query.filter_by(method=method).all()
        if len(cipher_list) > 0:
            last_data = cipher_list[len(cipher_list) - 1]
            text = ""  # Make this empty, so it will not be in presentation
            enc_text = last_data.enc_text
            shift = last_data.shift
        else:
            text = ""
            enc_text = ""
            shift = 0
    elif request.form['submit_button'] == 'Save':
        data = Data(text=text, enc_text=enc_text, shift=shift, method=method)
        save(data)
        msg = "Successfully Saved"
    return render_template('caesar_public.html', text=text, enc_text=enc_text, shift=shift)


# Controller
@app.route('/vigenere', methods=['POST'])
def vigenere_controller():
    text = request.form['text']
    key = request.form['key']
    method = 'vigenere'
    enc_text = request.form['enc_text']

    if request.form['submit_button'] == 'Encrypt':
        enc_text = vig_enc(text, key)
    elif request.form['submit_button'] == 'Decrypt':
        text = vig_dec(enc_text, key)
    elif request.form['submit_button'] == 'Load Last':
        cipher_list = Data.query.filter_by(method=method).all()
        if len(cipher_list) > 0:
            last_data = cipher_list[len(cipher_list) - 1]
            text = ""  # Make this empty, so it will not be in presentation
            enc_text = last_data.enc_text
            key = last_data.key
        else:
            text = ""
            enc_text = ""
            key = ""
    elif request.form['submit_button'] == 'Save':
        data = Data(text=text, enc_text=enc_text, key=key, method=method)
        save(data)
        msg = "Successfully Saved"
    return render_template('vigenere_public.html', text=text, enc_text=enc_text, key=key)


# Controller
@app.route('/mono', methods=['POST'])
def mono_controller():
    text = request.form['text']
    method = 'mono'
    enc_text = request.form['enc_text']
    alpha = ""
    if request.form['submit_button'] == 'Encrypt':
        alphabet = gen_alpha()
        enc_text = mono_encrypt(text, alphabet)
        alpha = alpha2string(alphabet)
    elif request.form['submit_button'] == 'Decrypt':
        msg = "Mono Alphabetic cipher is not working for decryption"
    elif request.form['submit_button'] == 'Load Last':
        cipher_list = Data.query.filter_by(method=method).all()
        if len(cipher_list) > 0:
            last_data = cipher_list[len(cipher_list) - 1]
            text = ""  # Make this empty, so it will not be in presentation
            enc_text = last_data.enc_text
        else:
            text = ""
            enc_text = ""
    elif request.form['submit_button'] == 'Save':
        data = Data(text=text, enc_text=enc_text, method=method)
        save(data)
        msg = "Successfully Saved"
    return render_template('mono_public.html', text=text, enc_text=enc_text, alpha=alpha)


# Controller
@app.route('/bruteforce', methods=['POST'])
def bruteforce_controller():
    texts = []
    cipher32 = request.form['cipher32']
    for i in range(0, 26):
        text = caesar_enc(cipher32, abs(i))
        texts.append(text)
    return render_template("brute_public.html", cipher32=cipher32, len=len(texts), answers=texts)


# help function
def save(data):
    db.session.add(data)
    db.session.commit()


@app.route('/', methods=['POST'])
def home_page_controller():
    decrypt_pressed = False
    text = request.form['plaintext']
    shift_by = int(request.form['rot'])
    method = request.form['encrypt-method']
    key = request.form['key']
    enc_text = request.form['ciphertext']
    alpha = ""
    if request.form['submit_button'] == 'Encrypt':
        if method == 'mono':
            alphabet = gen_alpha()
            enc_text = mono_encrypt(text, alphabet)
            alpha = alpha2string(alphabet)
        else:
            enc_text = caesar_enc(text, shift_by) if method == 'caesar' else vig_enc(text, key)
    elif request.form['submit_button'] == 'Decrypt':
        if method == 'mono':
            msg = "Mono Alphabetic cipher is not working for decryption"
            return render_template('form/index.html', plaintext=text, ciphertext=enc_text, rot=shift_by, key=key,
                                   decrypt_hide=decrypt_pressed, last_method=method, msg=msg)
        decrypt_pressed = True
        text = caesar_enc(enc_text, abs(
            26 - shift_by)) if method == 'caesar' else vig_dec(enc_text, key)
    elif request.form['submit_button'] == 'Load Last':
        cipher_list = Data.query.filter_by(method=method).all()
        if len(cipher_list) > 0:
            last_cipher = cipher_list[len(cipher_list) - 1]
            text = ""
            enc_text = last_cipher.cipher
            key = last_cipher.key
            shift_by = last_cipher.rotby
            method = last_cipher.method
        else:
            text = ''
            enc_text = ''
            key = ''
            shift_by = 0
            method = ''
        return render_template('form/index.html', plaintext=text, ciphertext=enc_text, rot=shift_by, key=key,
                               decrypt_hide=True, last_method=method)
    elif request.form['submit_button'] == 'Save':
        # Check for validity
        # if method != 'mono':
        #     if ciphertext == caesar_encrypt(text, rot) if method == 'caesar' else vigenere_encrypt(text, key):
        if True:
            new_cipher = Data(plaintext=text, cipher=enc_text,
                              method=method, key=key, nochar=len(text), rotby=shift_by)
            db.session.add(new_cipher)
            db.session.commit()
            return render_template('form/index.html', plaintext='', ciphertext='', rot=0, key='', decrypt_hide=True)
        else:
            return "Invalid Cipher and Plaintext"
    return render_template('form/index.html', plaintext=text, ciphertext=enc_text, rot=shift_by, key=key,
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

# @app.route('/bruteforce')
# def bruteforce():
#     return render_template("form/index2.html", len=len(Ducks), answers=Ducks)


# @app.route('/bruteforce', methods=['POST'])
# def bruteforce_done():
#     plaintexts = []
#     ciphertext = request.form['cipher32']
#     rot = 0
#     for i in range(0, 26):
#         text = caesar_enc(ciphertext, abs(26 - i))
#         plaintexts.append(text)
#     return render_template("form/index2.html", cipher32=ciphertext, len=len(plaintexts), answers=plaintexts)


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
