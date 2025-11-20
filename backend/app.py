"""
Arjun AI Text Tools - Main Flask Application
Author: Arjun
Description: Backend server for AI-powered translation and summarization
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from models.translator import TranslationService
from models.summarizer import SummarizationService
from utils.helpers import validate_text, format_error_response
import config

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize services
translator = TranslationService()
summarizer = SummarizationService()


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Arjun AI Text Tools API is running',
        'version': '1.0.0'
    })


@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate text from source language to target language
    
    Request Body:
    {
        "text": "Text to translate",
        "source": "en",  # Source language code
        "target": "hi",  # Target language code
        "model": "nllb"  # Model identifier
    }
    """
    try:
        start_time = time.time()
        
        # Get request data
        data = request.get_json()
        
        if not data:
            return format_error_response("No data provided"), 400
        
        text = data.get('text', '').strip()
        source_lang = data.get('source', 'auto')
        target_lang = data.get('target', 'en')
        model_id = data.get('model', 'nllb')
        
        # Validate input
        is_valid, error_msg = validate_text(text)
        if not is_valid:
            return format_error_response(error_msg), 400
        
        # Perform translation
        translated_text = translator.translate(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            model_id=model_id
        )
        
        processing_time = round(time.time() - start_time, 2)
        
        return jsonify({
            'success': True,
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'model_used': model_id,
            'processing_time': processing_time
        })
        
    except Exception as e:
        return format_error_response(str(e)), 500


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize text using AI models
    
    Request Body:
    {
        "text": "Text to summarize",
        "model": "bart",  # Model identifier
        "length": "short",  # short, medium, or long
        "format": "paragraph"  # paragraph or bullets
    }
    """
    try:
        start_time = time.time()
        
        # Get request data
        data = request.get_json()
        
        if not data:
            return format_error_response("No data provided"), 400
        
        text = data.get('text', '').strip()
        model_id = data.get('model', 'bart')
        length = data.get('length', 'short')
        output_format = data.get('format', 'paragraph')
        
        # Validate input
        is_valid, error_msg = validate_text(text, min_length=50)
        if not is_valid:
            return format_error_response(error_msg), 400
        
        # Perform summarization
        summary = summarizer.summarize(
            text=text,
            model_id=model_id,
            length=length,
            output_format=output_format
        )
        
        processing_time = round(time.time() - start_time, 2)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'model_used': model_id,
            'length': length,
            'format': output_format,
            'processing_time': processing_time
        })
        
    except Exception as e:
        return format_error_response(str(e)), 500


@app.route('/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    try:
        languages = config.SUPPORTED_LANGUAGES
        return jsonify({
            'success': True,
            'languages': languages
        })
    except Exception as e:
        return format_error_response(str(e)), 500


@app.route('/models/translation', methods=['GET'])
def get_translation_models():
    """Get list of available translation models"""
    try:
        models = config.TRANSLATION_MODELS
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        return format_error_response(str(e)), 500


@app.route('/models/summarization', methods=['GET'])
def get_summarization_models():
    """Get list of available summarization models"""
    try:
        models = config.SUMMARIZATION_MODELS
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        return format_error_response(str(e)), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return format_error_response("Endpoint not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return format_error_response("Internal server error"), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Arjun AI Text Tools Server")
    print("=" * 60)
    print(f"📍 Server running at: http://localhost:{config.PORT}")
    print(f"🔧 Debug mode: {config.DEBUG}")
    print(f"🌐 CORS enabled for frontend")
    print("=" * 60)
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
