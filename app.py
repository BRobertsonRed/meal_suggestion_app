from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import datetime
import random

app = Flask(__name__)

# Load the meal database
meals_df = pd.read_csv('meals.csv')

# Function to get daily meals based on type
def get_meal_suggestion(meal_type):
    meals = meals_df[meals_df['meal_type'] == meal_type]
    
    # Check if there are any meals of the specified type
    if meals.empty:
        return {
            'name': 'No meal available',
            'ingredients': 'N/A',
            'notes': 'Please add more options for this meal type.'
        }
    
    suggestion = meals.sample(n=1).iloc[0]
    return {
        'name': suggestion['meal_name'],
        'ingredients': suggestion['ingredients'],
        'notes': suggestion['notes']
    }


@app.route('/')
def index():
    # Get today's date for daily update
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    breakfast = get_meal_suggestion('breakfast')
    snack = get_meal_suggestion('snack')
    lunch = get_meal_suggestion('lunch')

    return render_template('index.html', today=today, breakfast=breakfast, snack=snack, lunch=lunch)

@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
