from flask import Flask, render_template, request
import os
import subprocess
import platform

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
OUTPUT_FILE = 'output.txt'  # Make sure main.c writes here

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        uploaded_file = request.files.get('cfile')

        if uploaded_file and uploaded_file.filename.endswith(('.c', '.cpp')):
            # Save uploaded file
            input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(input_path)

            try:
                # Run your compiled C syntax checker (main.exe or ./main)
                if platform.system() == "Windows":
                    subprocess.run(['main.exe', input_path], check=True)
                else:
                    subprocess.run(['./main', input_path], check=True)

                # Read the analysis output
                if os.path.exists(OUTPUT_FILE):
                    with open(OUTPUT_FILE, 'r') as f:
                        result = f.read()
                else:
                    result = "No output file generated."

            except Exception as e:
                result = f"Error while analyzing: {e}"

    return render_template('index4.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
