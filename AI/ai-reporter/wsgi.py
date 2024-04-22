from webapi.app.main import app
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('FLASK_PORT', 5001), debug=True)