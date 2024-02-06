from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import validators
import os
import time

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
    files = os.listdir('files')
    return render_template('page2.html', files=files)

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
        
        # Create a folder named 'files' if it doesn't exist
        folder_path = os.path.join(os.getcwd(), 'files')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Generate the report file name with creation time
        report_filename = f"report_{int(time.time())}.txt"
        report_filepath = os.path.join(folder_path, report_filename)
        
        # Write content to the report file
        with open(report_filepath, 'w') as file:
            file.write(f"Input URL: {input_value}\n")
            file.write(f"Page Title: {page_title}\n")
            file.write("Selected Options:\n")
            if option1:
                file.write("Option 1\n")
            if option2:
                file.write("Option 2\n")
            if option3:
                file.write("Option 3\n")
        
        return render_template('page1_result.html', input_value=input_value, page_title=page_title, option1=option1, option2=option2, option3=option3)
    else:
        error_message = "Invalid URL. Please enter a valid URL."
        return render_template('page1.html', error_message=error_message)

@app.route('/page2_result', methods=['POST'])
def page2_result():
    file1 = request.form.get('file1')
    file2 = request.form.get('file2')
    
    # Create a folder named 'comparison' if it doesn't exist
    comparison_folder = os.path.join(os.getcwd(), 'comparison')
    if not os.path.exists(comparison_folder):
        os.makedirs(comparison_folder)
    
    # Save the content of both selected files into a new file in the comparison folder
    comparison_file_path = os.path.join(comparison_folder, f'comparison_{int(time.time())}.txt')
    with open(comparison_file_path, 'w') as comparison_file:
        with open(os.path.join('files', file1), 'r') as file1_content:
            comparison_file.write(f'Contents of {file1}:\n')
            comparison_file.write(file1_content.read())
            comparison_file.write('\n\n')
        with open(os.path.join('files', file2), 'r') as file2_content:
            comparison_file.write(f'Contents of {file2}:\n')
            comparison_file.write(file2_content.read())
    
    return render_template('page2_result.html', comparison_file_path=comparison_file_path)



@app.route('/page3_result', methods=['POST'])
def page3_result():
    # Perform any necessary processing
    return render_template('page3_result.html')

if __name__ == '__main__':
    app.run(debug=True)
