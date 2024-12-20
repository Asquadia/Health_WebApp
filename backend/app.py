from flask import Flask, request, jsonify, send_from_directory
import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_dir = os.path.dirname(current_dir)
# Add the project root to sys.path
sys.path.append(project_dir)

from bmi_service.bmi import bmi
from bmr_service.bmr import bmr

app = Flask(__name__, static_folder='../frontend')

@app.route('/api/bmi', methods=['GET'])
def api_calculate_bmi():
    """
    Endpoint to calculate BMI.
    """
    weight = request.args.get('weight', type=float)
    height = request.args.get('height', type=float)

    if weight is None or height is None:
        return jsonify({'error': 'Weight and height are required parameters.'}), 400

    try:
        bmi_result = bmi(weight, height)
        return jsonify({'bmi': bmi_result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except TypeError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/bmr', methods=['GET'])
def api_calculate_bmr():
    """
    Endpoint to calculate BMR.
    """
    weight = request.args.get('weight', type=float)
    height = request.args.get('height', type=float)
    age = request.args.get('age', type=int)
    gender = request.args.get('gender')

    if weight is None or height is None or age is None or gender is None:
        return jsonify({'error': 'Weight, height, age, and gender are required parameters.'}), 400

    try:
        bmr_result = bmr(weight, height, age, gender)
        return jsonify({'bmr': bmr_result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except TypeError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
