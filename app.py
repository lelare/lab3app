import json
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)


def read_messages_from_file():
    """ Read all messages from a JSON file"""
    with open('/mnt/data.json') as messages_file:
        return json.load(messages_file)


def append_message_to_file(content):
    """ Read the contents of JSON file, add this message to it's contents, then write it back to disk. """
    data = read_messages_from_file()
    new_message = {
        'content': content,
        'timestamp': datetime.now().isoformat(" ", "seconds")
    }
    data['messages'].append(new_message)
    with open('/mnt/data.json', mode='w') as messages_file:
        json.dump(data, messages_file)


# The Flask route, defining the main behaviour of the webserver:
@app.route("/")
def home():
    new_message = request.args.get('msg')
    if new_message:
        append_message_to_file(new_message)

    data = read_messages_from_file()

    # Return a Jinja HTML template, passing the messages as an argument to the template:
    return render_template('home.html', messages=data['messages'])
