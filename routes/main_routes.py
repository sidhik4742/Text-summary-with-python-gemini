from flask import Blueprint, render_template, jsonify, request
from utils.gemini import get_gemini_response
from utils.helper import str_to_dict
import asyncio

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/process', methods=['POST'])
def process_input():
    prompt = request.get_json().get('prompt', '')
    print(f"Received prompt: {prompt}")
    # Here you can add any processing logic you need
    # Calling gemini AI to get the summarization of the prompt
    response = get_gemini_response(prompt)
    print(f"Gemini response: {response}")
    response = {
        'status': True, # boolean
        'message': response
    }
    return jsonify(response)

# enpoint for returning the summary of the text using gemini AI
@main_bp.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Call Gemini API to get the summary
    # creating prompt for getting summary of the text
    prompt = f"""Can you summarize the following text in a concise manner, highlighting the key points and main ideas?
    Text: {text}"""
    try:
        summary = get_gemini_response(prompt)
        return jsonify({'status': True, 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# endpoint for extract data as JSON format with given JSON schema using gemini AI
@main_bp.route('/extract', methods=['POST'])
def extract_data():
    data = request.get_json()
    text = data.get('text', '')
    schema = data.get('schema', {})
    if not text or not schema:
        return jsonify({'error': 'Text or schema not provided'}), 400

    # Call Gemini API to extract data based on the provided schema
    prompt = f"""Extract the following data from the text according to this JSON schema: {schema}, 
    note: the output should be in JSON format only.
    Text: {text}"""
    try:
        extracted_data = get_gemini_response(prompt)
        # remove json code block if present
        if extracted_data.startswith("```json") and extracted_data.endswith("```"):
            extracted_data = extracted_data.replace("```json", "").replace("```", "").strip()
        extracted_data = str_to_dict(extracted_data)  # convert string to dict
        return jsonify({'status': True, 'data': extracted_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


