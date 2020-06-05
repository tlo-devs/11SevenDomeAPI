"""
This file exists so that the Server can be run in Debug mode if necessary.
"""
from application import app
from uvicorn import run


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5000)
