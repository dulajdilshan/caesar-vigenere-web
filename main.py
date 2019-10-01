from flask import Flask,render_template, g

app = Flask(__name__)


@app.route('/')
def index():
    return 'This is index!'

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
