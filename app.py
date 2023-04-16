from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Data structures to store user data
users = {}
progress = {}

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Create a new user with email and password
        users[email] = password
        # Initialize progress for the user
        progress[email] = {
            'current_step': 1,
            'start_time': datetime.datetime.now(),
            'end_time': None,
            'solution_accuracy': 0
        }
        return redirect(url_for('puzzle', email=email))
    return render_template('register.html')

# Route for puzzle
@app.route('/puzzle/<email>', methods=['GET', 'POST'])
def puzzle(email):
    if request.method == 'POST':
        # Update user progress
        current_step = progress[email]['current_step']
        progress[email]['current_step'] = current_step + 1
        progress[email]['end_time'] = datetime.datetime.now()
        # Update solution accuracy (you can implement your own logic to calculate accuracy)
        solution_accuracy = progress[email]['solution_accuracy']
        progress[email]['solution_accuracy'] = solution_accuracy + 1

        # Check for puzzle completion
        if current_step == 5:
            return redirect(url_for('completed', email=email))
        else:
            return redirect(url_for('puzzle', email=email))
    return render_template('puzzle.html', step=progress[email]['current_step'])

@app.route('/success/<email>')
def success(email):
    return render_template('success.html', email=email)

# Route for displaying the dead-end page
@app.route('/deadend/<email>')
def deadend(email):
    return render_template('deadend.html', email=email)

if __name__ == '__main__':
    app.run(debug=True)
