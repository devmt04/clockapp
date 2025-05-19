from flask import Flask, render_template, jsonify
import helper
import config
import threading
import time
# import helper

app = Flask(__name__)

# This is the variable you want to change dynamically
current_value = {"data": "0"}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(current_value)


def cast():
    while True:
        time.sleep(1)  # change every 1 seconds (for demo)
        current_value["data"] = helper.broadcast()

# Simulate dynamic updates (optional)
@app.route('/update/<int:new_value>')
def update_value(new_value):
    current_value["data"] = new_value
    return f"Value updated to {new_value}"

if __name__ == '__main__':
    helper.execute()
    thread = threading.Thread(target=cast)
    thread.daemon = True
    thread.start()
    app.run(host=config.IP, port=config.PORT, debug=True)
