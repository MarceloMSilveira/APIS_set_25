from flask import Flask

app = Flask(__name__)

@app.route('/')
def basic():
    return 'Hello Flask!'

@app.route('/returnJSON')
def returnJSON():
    return {
        'name':'Marcelo',
        'age':51
    }