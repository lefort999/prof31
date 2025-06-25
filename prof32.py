import os
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, world!'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render attribue automatiquement un port
    app.run(host="0.0.0.0", port=port)

