"""
Eventually will be the tos application, a flask app.
right now it doesn't do much
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return '\n@@@ hello from TOS @@@\n@@@ I am {} @@@\n\n'.format(__name__)


if __name__ == '__main__':
    # this bit should only be used by the dev server

    app.run(host='127.0.0.1')

