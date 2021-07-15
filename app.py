from flask import Flask

# create new instance called app
app = Flask(__name__)

# define the starting point, also known as the root
@app.route('/')
def hello_world():
    return 'Hello world'