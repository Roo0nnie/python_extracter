from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route('/extract_pdf', methods=['POST'])

def extract_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
     
        try:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return jsonify({"content": text}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File is not a PDF"}), 400

if __name__ == '__main__':
    app.run(debug=True)