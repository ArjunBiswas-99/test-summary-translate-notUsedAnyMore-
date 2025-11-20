"""
Configuration file for Arjun AI Text Tools
Contains all API endpoints, model configurations, and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server Configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# API Configuration
API_TOKEN = os.getenv('API_TOKEN', '')  # Your API token from .env file
API_BASE_URL = "https://api-inference.huggingface.co/models/"

# Translation Models Configuration
TRANSLATION_MODELS = [
    {
        'id': 'nllb',
        'name': 'NLLB-200 Distilled (Best for Indian Languages)',
        'model_path': 'facebook/nllb-200-distilled-600M',
        'recommended': True
    },
    {
        'id': 'opus',
        'name': 'Helsinki-NLP OPUS (Fast)',
        'model_path': 'Helsinki-NLP/opus-mt-en-mul',
        'recommended': False
    },
    {
        'id': 'mbart',
        'name': 'mBART-50 (Multilingual)',
        'model_path': 'facebook/mbart-large-50-one-to-many-mmt',
        'recommended': False
    }
]

# Summarization Models Configuration
SUMMARIZATION_MODELS = [
    {
        'id': 'bart',
        'name': 'BART-large-CNN (Best Quality)',
        'model_path': 'facebook/bart-large-cnn',
        'recommended': True
    },
    {
        'id': 'distilbart',
        'name': 'DistilBART (Faster)',
        'model_path': 'sshleifer/distilbart-cnn-12-6',
        'recommended': False
    },
    {
        'id': 't5',
        'name': 'T5-base (Balanced)',
        'model_path': 't5-base',
        'recommended': False
    },
    {
        'id': 'mbart',
        'name': 'mBART-50 (Multilingual)',
        'model_path': 'facebook/mbart-large-50',
        'recommended': False
    }
]

# Summary Length Configuration
SUMMARY_LENGTH = {
    'short': {
        'max_length': 130,
        'min_length': 30
    },
    'medium': {
        'max_length': 250,
        'min_length': 100
    },
    'long': {
        'max_length': 400,
        'min_length': 200
    }
}

# Supported Languages (with focus on Indian languages)
SUPPORTED_LANGUAGES = [
    {'code': 'auto', 'name': 'Auto-detect', 'native': 'Auto-detect'},
    {'code': 'en', 'name': 'English', 'native': 'English'},
    {'code': 'hi', 'name': 'Hindi', 'native': 'हिन्दी'},
    {'code': 'bn', 'name': 'Bengali', 'native': 'বাংলা'},
    {'code': 'te', 'name': 'Telugu', 'native': 'తెలుగు'},
    {'code': 'mr', 'name': 'Marathi', 'native': 'मराठी'},
    {'code': 'ta', 'name': 'Tamil', 'native': 'தமிழ்'},
    {'code': 'gu', 'name': 'Gujarati', 'native': 'ગુજરાતી'},
    {'code': 'ur', 'name': 'Urdu', 'native': 'اردو'},
    {'code': 'kn', 'name': 'Kannada', 'native': 'ಕನ್ನಡ'},
    {'code': 'ml', 'name': 'Malayalam', 'native': 'മലയാളം'},
    {'code': 'pa', 'name': 'Punjabi', 'native': 'ਪੰਜਾਬੀ'},
    {'code': 'or', 'name': 'Odia', 'native': 'ଓଡ଼ିଆ'},
    {'code': 'as', 'name': 'Assamese', 'native': 'অসমীয়া'},
    {'code': 'es', 'name': 'Spanish', 'native': 'Español'},
    {'code': 'fr', 'name': 'French', 'native': 'Français'},
    {'code': 'de', 'name': 'German', 'native': 'Deutsch'},
    {'code': 'zh', 'name': 'Chinese', 'native': '中文'},
    {'code': 'ar', 'name': 'Arabic', 'native': 'العربية'},
    {'code': 'ja', 'name': 'Japanese', 'native': '日本語'},
    {'code': 'ko', 'name': 'Korean', 'native': '한국어'},
    {'code': 'pt', 'name': 'Portuguese', 'native': 'Português'},
    {'code': 'ru', 'name': 'Russian', 'native': 'Русский'},
    {'code': 'it', 'name': 'Italian', 'native': 'Italiano'},
    {'code': 'nl', 'name': 'Dutch', 'native': 'Nederlands'},
    {'code': 'tr', 'name': 'Turkish', 'native': 'Türkçe'},
    {'code': 'pl', 'name': 'Polish', 'native': 'Polski'},
    {'code': 'vi', 'name': 'Vietnamese', 'native': 'Tiếng Việt'},
    {'code': 'th', 'name': 'Thai', 'native': 'ไทย'},
    {'code': 'id', 'name': 'Indonesian', 'native': 'Bahasa Indonesia'}
]

# Text Validation Configuration
MAX_TEXT_LENGTH = 10000  # Maximum characters for translation/summarization
MIN_SUMMARY_LENGTH = 50  # Minimum characters required for summarization

# Request Timeout Configuration
REQUEST_TIMEOUT = 30  # Seconds
