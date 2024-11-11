import os
from flask import Flask, request, render_template, send_from_directory
from Logic.mlb_app import handle_mlb_logic
from Logic.nfl_app import handle_nfl_logic
from Logic.mlb_app import mlb_bp
from Logic.nfl_app import nfl_bp

app = Flask(__name__)

app.register_blueprint(mlb_bp)
app.register_blueprint(nfl_bp)

@app.route('/', methods=['GET'])
def index():
    return render_template('Bet_program2.html')

@app.route('/generate-url', methods=['POST'])
def generate_url():
    if request.method == 'POST':
        league = request.form.get('league').lower()

        # Calls the MLB logic file
        if league == 'mlb':
            return handle_mlb_logic(request)
        # Calls the NFL logic file
        elif league == 'nfl':
            return handle_nfl_logic(request)

        else:
            return "Unsupported league", 400

@app.route('/static/data/<path:filename>')
def serve_static_data(filename):
    data_dir = 'Backend/Names'
    return send_from_directory(data_dir, filename)

if __name__ == '__main__':
    # Listen on the PORT environment variable for Cloud Run
    port = int(os.environ.get('PORT', 5000))  # Defaults to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)
