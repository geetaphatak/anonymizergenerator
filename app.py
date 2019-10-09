from flask import Flask, send_from_directory, url_for, jsonify
import os
import numpy as np
import pandas as pd
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from anonymizer import Anonymizer
from demographics_anon import *

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True

filepath = ""

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/index_full')
def index_full():
    return render_template('index_full.html')

@app.route('/get_data')
def get_data():
    rows = request.args.get('n')
    male_percentage = request.args.get('m')
    exclude_locations = request.args.get('exclude_loc')
    print(exclude_locations)
    records = get_anon_data(int(rows), float(male_percentage), exclude_locations, 'non-indian')
    return records

@app.route('/get_indian_data')
def get_indian_data():
    rows = request.args.get('n')
    male_percentage = request.args.get('m')
    exclude_locations = request.args.get('exclude_loc')
    print(exclude_locations)
    records = get_anon_data(int(rows), float(male_percentage), exclude_locations, 'indian')
    return records

@app.route('/get_modified_data', methods=['POST'])
def get_modified_data():
    if request.method == "POST":
        rows = request.form['rows']
        male_percentage = request.form['percent']
        exclude_loc = request.form['exclude_loc']
        records = get_anon_data(int(rows), float(male_percentage), exclude_loc, 'non-indian')
        df = pd.DataFrame.from_dict(records['data'])
        df.columns = ['id|name|first_name|middle_name|last_name|suffix|martial_status|preferred_communication|ethnicity|email|sex|address_line1|city|state|zip|country|driverlicense|dob|deceased_flag|death_date|phone_cell|phone_fax|phone_home|ssn']
        df.to_csv('static/generated_data_records.csv', index = None, header=True)
        link = "<a href='static/generated_data_records.csv' class='link_dwn' download='generated_data_records.csv'>Save File</a>"
        return jsonify({"status":"success","response":link})

    else:
        return "Kindly do post request"



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def main():
    if request.method == 'POST':
        if request.form['submit'] == 'Upload':
            return upload_file()
        elif request.form['submit'] == 'Anonymize':
            return anonymize()
        elif request.form['submit'] == 'Generate Data':
            return generate_data()
    else:
        return "main"


def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global filepath
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(filepath)
        flash('File successfully uploaded:' + filepath)
        data = pd.read_csv(filepath, sep='|')
        headers = list(data)
        return render_template('index.html',dropdown = headers)
    else:
        flash('Allowed file type is csv')
        return redirect(request.url)


def anonymize():
    try:
        global filepath
        data = pd.read_csv(filepath,sep='|')
        rows, c = data.shape
        selected_name = request.form.get('options_name')
        selected_city = request.form.get('options_city')
        selected_country = request.form.get('options_country')
        selected_address = request.form.get('options_address')
        selected_url = request.form.get('options_uri')

        anonymize_data = Anonymizer()

        if selected_name != 'None':
            fake_names,fake_first_names,fake_second_names = anonymize_data.fake_name_generator(rows)
            data[str(selected_name)] = fake_names
        if selected_city != 'None':
            data[str(selected_city)] = anonymize_data.get_fake_cities(rows)
        if selected_country != 'None':
            data[str(selected_country)] = anonymize_data.get_fake_countries(rows)
        if selected_address != 'None':
            data[str(selected_address)] = anonymize_data.get_fake_addresses(rows)
        if selected_url != 'None':
            data[str(selected_url)] = anonymize_data.get_fake_uris(rows)

        data.to_csv ('static/export_data.csv', sep='|', index = None, header=True)
        flash('File successfully anonymized')
        return render_template('index.html', path_anonymize = 'static/export_data.csv')
    except:
        return render_template('index.html')


def generate_data():
    try:
        generate_data = pd.DataFrame()
        rows = int(request.form.get('num_rows'))
        anonymize_data = Anonymizer()
        fake_names,fake_first_names,fake_second_names = anonymize_data.fake_name_generator(rows)
        generate_data['name'] = fake_names
        generate_data['first_name'] = fake_first_names
        generate_data['last_name'] = fake_second_names
        generate_data['city'] = anonymize_data.get_fake_cities(rows)
        generate_data['country'] = anonymize_data.get_fake_countries(rows)
        generate_data['street_address'] = anonymize_data.get_fake_addresses(rows)
        generate_data['url'] = anonymize_data.get_fake_uris(rows)
        generate_data.to_csv ('static/generated_data.csv', sep='|', index = None, header=True)
        flash('File successfully generated')
        return render_template('index.html', path_generated_data = 'static/generated_data.csv')

    except:
        return render_template('index.html')


@app.route('/unstructured', methods=['POST'])
def unstructured():
    if request.method == "POST":
        if request.form['inputText']:
            return get_structured_data()
    else:
        return "unstructured"

def get_structured_data():
    inputText = request.form['inputText']
    print(inputText)
    anonymize_data = Anonymizer()
    anonymizedText = anonymize_data.get_anonymize_text(inputText)
    return jsonify({"status":"success","response":anonymizedText})

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
