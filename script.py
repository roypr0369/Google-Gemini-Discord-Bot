from flask import Flask
import run  # Import your main Python script

app = Flask(__name__)

@app.route('/')
def home():
    # Run your main Python script here
    result = run.main_function()  # Replace with your main function name
    return f"Script executed: {result}", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
