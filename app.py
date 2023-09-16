from flask import Flask, request, jsonify
import pandas as pd
import time
import threading

app = Flask(__name__)

# This will hold the processing results
results = {}

def process_file(file_path):
    # Simulate 10 minutes of processing
    time.sleep(3)

    # Read the CSV file
    df = pd.read_csv(file_path)
    print(df)

    # Perform your data processing here...

    # Update the results
    results[file_path] = "Processing completed."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400

    file_path = "./app_db/" + file.filename
    file.save(file_path)

    # Start a new thread to process the file
    threading.Thread(target=process_file, args=(file_path,)).start()

    return jsonify({'message': 'File is being processed.'}), 200

@app.route('/report', methods=['GET'])
def report():
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
