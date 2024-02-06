from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import validators

app = Flask(__name__)

# Define routes for each page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

# Define routes for result pages
@app.route('/page1_result', methods=['POST'])
def page1_result():
    input_value = request.form.get('input_value')
    option1 = 'option1' in request.form
    option2 = 'option2' in request.form
    option3 = 'option3' in request.form
    
    # Check if the input starts with http://, https://, or www
    if not input_value.startswith(('http://', 'https://', 'www.')):
        input_value = 'https://' + input_value

    # Validate the URL
    if validators.url(input_value):
        # Fetch the webpage content
        response = requests.get(input_value)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title
        page_title = soup.title.string if soup.title else 'Title not found'

        return render_template('page1_result.html', input_value=input_value, page_title=page_title, option1=option1, option2=option2, option3=option3)
    else:
        error_message = "Invalid URL. Please enter a valid URL."
        return render_template('page1.html', error_message=error_message)

@app.route('/page2_result', methods=['POST'])
def page2_result():
    # Perform any necessary processing
    return render_template('page2_result.html')

@app.route('/page3_result', methods=['POST'])
def page3_result():
    # Perform any necessary processing
    return render_template('page3_result.html')

if __name__ == '__main__':
    app.run(debug=True)
