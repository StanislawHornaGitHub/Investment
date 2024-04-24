import os

from Investment_API import app


if __name__ == "__main__":
    DEBUG_MODE = os.getenv('FLASK_DEBUG', True)
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0'
    )