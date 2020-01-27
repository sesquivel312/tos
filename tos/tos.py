from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '\n@@@ hello from TOS @@@\n@@@ I am {} @@@\n\n'.format(__name__)

if __name__ == '__main__':

    app.run(host='127.0.0.1')
