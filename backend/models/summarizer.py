"""
Summarization Service Module
Handles all text summarization operations using AI models
"""

import requests
import config


class SummarizationService:
    """Service class for handling text summarization"""
    
    def __init__(self):
        """Initialize the summarization service"""
        self.api_token = config.API_TOKEN
        self.api_base_url = config.API_BASE_URL
        self.models = {model['id']: model for model in config.SUMMARIZATION_MODELS}
        
    def _get_model_path(self, model_id):
        """Get the full model path for a given model ID"""
        if model_id not in self.models:
            model_id = 'bart'  # Default to BART
        return self.models[model_id]['model_path']
    
    def _prepare_headers(self):
        """Prepare API request headers"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _get_length_params(self, length):
        """
        Get max and min length parameters for summary
        
        Args:
            length: 'short', 'medium', or 'long'
            
        Returns:
            Dictionary with max_length and min_length
        """
        if length not in config.SUMMARY_LENGTH:
            length = 'short'
        return config.SUMMARY_LENGTH[length]
    
    def _format_as_bullets(self, text):
        """
        Format text as bullet points
        
        Args:
            text: Summary text to format
            
        Returns:
            Bullet-pointed text
        """
        # Split by sentences
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Format as bullets
        bullets = '\n'.join([f"• {sentence}" for sentence in sentences])
        return bullets
    
    def _make_api_request(self, model_path, payload):
        """
        Make API request to the summarization service
        
        Args:
            model_path: Full path to the model
            payload: Request payload
            
        Returns:
            Summarized text or error message
        """
        url = f"{self.api_base_url}{model_path}"
        headers = self._prepare_headers()
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if 'summary_text' in result[0]:
                        return result[0]['summary_text']
                    elif 'generated_text' in result[0]:
                        return result[0]['generated_text']
                elif isinstance(result, dict):
                    if 'summary_text' in result:
                        return result['summary_text']
                    elif 'generated_text' in result:
                        return result['generated_text']
                
                return str(result)
            
            elif response.status_code == 503:
                return "⏳ Model is loading, please wait a moment and try again..."
            else:
                return f"Error: Unable to summarize (Status: {response.status_code})"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error: Connection failed - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def summarize(self, text, model_id='bart', length='short', output_format='paragraph'):
        """
        Summarize text using AI models
        
        Args:
            text: Text to summarize
            model_id: Model identifier to use
            length: 'short', 'medium', or 'long'
            output_format: 'paragraph' or 'bullets'
            
        Returns:
            Summarized text
        """
        # Get model path
        model_path = self._get_model_path(model_id)
        
        # Get length parameters
        length_params = self._get_length_params(length)
        
        # Prepare payload
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": length_params['max_length'],
                "min_length": length_params['min_length'],
                "do_sample": False
            }
        }
        
        # Make API request
        summary = self._make_api_request(model_path, payload)
        
        # Format output if needed
        if output_format == 'bullets' and not summary.startswith('Error'):
            summary = self._format_as_bullets(summary)
        
        return summary
    
    def get_summary_stats(self, original_text, summary):
        """
        Get statistics about the summarization
        
        Args:
            original_text: Original text before summarization
            summary: Summarized text
            
        Returns:
            Dictionary with statistics
        """
        original_words = len(original_text.split())
        summary_words = len(summary.split())
        
        compression_ratio = round((1 - summary_words / original_words) * 100, 1) if original_words > 0 else 0
        
        return {
            'original_words': original_words,
            'summary_words': summary_words,
            'compression_ratio': compression_ratio
        }
