from flask import Flask
from flask_cors import CORS
from webapi.app.routes.chatBP import chatBP
from webapi.app.routes.attachmentBP import attachmentBP
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(chatBP)
app.register_blueprint(attachmentBP)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('FLASK_PORT', 5001), debug=True)
