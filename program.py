from flask import Flask
# import pdb
# pdb.set_trace()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug=True)