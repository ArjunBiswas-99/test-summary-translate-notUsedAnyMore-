"""
Helper utility functions
"""

from flask import jsonify
import config


def validate_text(text, min_length=1, max_length=None):
    """
    Validate input text
    
    Args:
        text: Text to validate
        min_length: Minimum required length
        max_length: Maximum allowed length (defaults to config.MAX_TEXT_LENGTH)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if max_length is None:
        max_length = config.MAX_TEXT_LENGTH
    
    # Check if text is empty
    if not text or not text.strip():
        return False, "Text cannot be empty"
    
    # Check minimum length
    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters long"
    
    # Check maximum length
    if len(text) > max_length:
        return False, f"Text cannot exceed {max_length} characters"
    
    return True, None


def format_error_response(error_message):
    """
    Format error message as JSON response
    
    Args:
        error_message: Error message string
        
    Returns:
        JSON response with error
    """
    return jsonify({
        'success': False,
        'error': error_message
    })


def format_success_response(data):
    """
    Format success response with data
    
    Args:
        data: Data to include in response
        
    Returns:
        JSON response with data
    """
    response = {'success': True}
    response.update(data)
    return jsonify(response)


def count_words(text):
    """
    Count words in text
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


def count_characters(text):
    """
    Count characters in text
    
    Args:
        text: Text to count characters in
        
    Returns:
        Number of characters
    """
    return len(text)


def truncate_text(text, max_length=100):
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def clean_text(text):
    """
    Clean and normalize text
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text
