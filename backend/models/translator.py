"""
Translation Service Module
Handles all translation operations using AI models
"""

import requests
from huggingface_hub import InferenceClient
import config


class TranslationService:
    """Service class for handling text translation"""
    
    def __init__(self):
        """Initialize the translation service"""
        self.api_token = config.API_TOKEN
        self.api_base_url = config.API_BASE_URL
        self.models = {model['id']: model for model in config.TRANSLATION_MODELS}
        # Use the serverless inference endpoint
        self.client = InferenceClient(token=self.api_token, base_url="https://api-inference.huggingface.co/models")
        
    def _get_model_path(self, model_id):
        """Get the full model path for a given model ID"""
        if model_id not in self.models:
            model_id = 'nllb'  # Default to NLLB
        return self.models[model_id]['model_path']
    
    def _prepare_headers(self):
        """Prepare API request headers"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_api_request(self, model_path, payload):
        """
        Make API request to the translation service
        
        Args:
            model_path: Full path to the model
            payload: Request payload
            
        Returns:
            Translated text or error message
        """
        url = f"{self.api_base_url}{model_path}"
        headers = self._prepare_headers()
        
        try:
            print(f"🔄 Requesting translation from: {url}")
            print(f"📦 Payload: {payload}")
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=config.REQUEST_TIMEOUT
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response data: {result}")
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if 'translation_text' in result[0]:
                        return result[0]['translation_text']
                    elif 'generated_text' in result[0]:
                        return result[0]['generated_text']
                elif isinstance(result, dict):
                    if 'translation_text' in result:
                        return result['translation_text']
                    elif 'generated_text' in result:
                        return result['generated_text']
                
                return str(result)
            
            elif response.status_code == 503:
                return "⏳ Model is loading, please wait a moment and try again..."
            elif response.status_code == 404:
                error_msg = f"❌ Model not found (404). Model: {model_path}"
                print(error_msg)
                try:
                    error_detail = response.json()
                    print(f"Error details: {error_detail}")
                except:
                    pass
                return "Error: Translation model not found. The model may have been moved or is temporarily unavailable. Please try a different model."
            elif response.status_code == 410:
                error_msg = f"❌ Model endpoint no longer available (410). Model: {model_path}"
                print(error_msg)
                try:
                    error_detail = response.json()
                    print(f"Error details: {error_detail}")
                except:
                    pass
                return "Error: This translation model is no longer available. Please try a different model or contact support."
            else:
                error_msg = f"Error: Unable to translate (Status: {response.status_code})"
                print(f"❌ {error_msg}")
                try:
                    error_detail = response.json()
                    print(f"Error details: {error_detail}")
                except:
                    pass
                return error_msg
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error: Connection failed - {str(e)}"
        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            return f"Error: {str(e)}"
    
    def translate(self, text, source_lang, target_lang, model_id='nllb'):
        """
        Translate text from source language to target language using post request directly
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            model_id: Model identifier to use
            
        Returns:
            Translated text
        """
        # Get model path
        model_path = self._get_model_path(model_id)
        
        try:
            print(f"🔄 Requesting translation using direct API call")
            print(f"📦 Model: {model_path}")
            print(f"📝 Text: {text[:100]}...")  # Show first 100 chars
            
            # Prepare request
            url = f"https://api-inference.huggingface.co/models/{model_path}"
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "x-use-cache": "false"  # Bypass cache to use latest endpoint
            }
            
            # Prepare payload
            if model_id == 'nllb':
                src_lang_code = self._convert_lang_code(source_lang, 'nllb')
                tgt_lang_code = self._convert_lang_code(target_lang, 'nllb')
                print(f"🌐 Source: {src_lang_code} → Target: {tgt_lang_code}")
                
                payload = {
                    "inputs": text,
                    "parameters": {
                        "src_lang": src_lang_code,
                        "tgt_lang": tgt_lang_code
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": False
                    }
                }
            else:
                payload = {
                    "inputs": text,
                    "options": {
                        "wait_for_model": True
                    }
                }
            
            print(f"📤 Sending request to: {url}")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response data: {result}")
                
                # Extract translation text
                if isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], dict):
                        translated_text = result[0].get('translation_text', result[0].get('generated_text', str(result[0])))
                    else:
                        translated_text = str(result[0])
                elif isinstance(result, dict):
                    translated_text = result.get('translation_text', result.get('generated_text', str(result)))
                else:
                    translated_text = str(result)
                
                print(f"✅ Translation successful: {translated_text[:100]}...")
                return translated_text
            
            elif response.status_code == 503:
                return "⏳ Model is loading, please wait 20-30 seconds and try again..."
            elif response.status_code == 410:
                # Endpoint deprecated - provide helpful message
                return "Error: The Hugging Face Inference API endpoint has been deprecated. Please update your API configuration or use a different translation service."
            else:
                error_detail = ""
                try:
                    error_json = response.json()
                    error_detail = str(error_json)
                except:
                    error_detail = response.text
                print(f"❌ Error response: {error_detail}")
                return f"Error: Translation failed (Status {response.status_code}). {error_detail[:200]}"
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be loading - please try again in a moment."
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Translation error: {error_msg}")
            
            if "410" in error_msg or "Gone" in error_msg:
                return "Error: The Hugging Face Inference API endpoint has been deprecated. Please contact support for updated configuration."
            elif "503" in error_msg or "loading" in error_msg.lower():
                return "⏳ Model is loading, please wait a moment and try again..."
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                return "Error: Invalid API token. Please check your Hugging Face API token in the .env file."
            else:
                return f"Error: Translation failed - {error_msg}"
    
    def _convert_lang_code(self, lang_code, model_type='nllb'):
        """
        Convert language code to model-specific format
        
        Args:
            lang_code: Standard language code (e.g., 'en', 'hi')
            model_type: Type of model ('nllb', 'opus', etc.)
            
        Returns:
            Model-specific language code
        """
        if model_type == 'nllb':
            # NLLB uses format like 'eng_Latn', 'hin_Deva', etc.
            nllb_codes = {
                'en': 'eng_Latn',
                'hi': 'hin_Deva',
                'bn': 'ben_Beng',
                'te': 'tel_Telu',
                'mr': 'mar_Deva',
                'ta': 'tam_Taml',
                'gu': 'guj_Gujr',
                'ur': 'urd_Arab',
                'kn': 'kan_Knda',
                'ml': 'mal_Mlym',
                'pa': 'pan_Guru',
                'or': 'ory_Orya',
                'as': 'asm_Beng',
                'es': 'spa_Latn',
                'fr': 'fra_Latn',
                'de': 'deu_Latn',
                'zh': 'zho_Hans',
                'ar': 'arb_Arab',
                'ja': 'jpn_Jpan',
                'ko': 'kor_Hang',
                'pt': 'por_Latn',
                'ru': 'rus_Cyrl',
                'it': 'ita_Latn',
                'nl': 'nld_Latn',
                'tr': 'tur_Latn',
                'pl': 'pol_Latn',
                'vi': 'vie_Latn',
                'th': 'tha_Thai',
                'id': 'ind_Latn'
            }
            return nllb_codes.get(lang_code, 'eng_Latn')
        
        # For other models, return as-is
        return lang_code
    
    def detect_language(self, text):
        """
        Detect the language of the given text
        Note: This is a placeholder - actual implementation would require
        a language detection model or service
        
        Args:
            text: Text to detect language for
            
        Returns:
            Detected language code
        """
        # For now, return 'en' as default
        # In production, you would use a language detection API
        return 'en'
