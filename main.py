from flask import Flask
from config import env_variables
from route import app

config = env_variables()

if __name__ == "__main__":
    print(f"\nYour verification token is: {config['TOKEN']}")
    print("Use this token in Meta Developer Dashboard")
    print("Server running on http://localhost:5001")
    app.run(port=5001, debug=True)

