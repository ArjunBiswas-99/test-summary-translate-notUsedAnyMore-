/**
 * API Module - Handles all backend communication
 */

const API = {
    baseURL: 'http://localhost:5000',
    
    /**
     * Make a POST request to the backend
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return {
                success: false,
                error: 'Failed to connect to server. Please ensure the backend is running.'
            };
        }
    },
    
    /**
     * Make a GET request to the backend
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return {
                success: false,
                error: 'Failed to connect to server. Please ensure the backend is running.'
            };
        }
    },
    
    /**
     * Translate text
     */
    async translate(text, sourceLang, targetLang, model) {
        return await this.post('/translate', {
            text: text,
            source: sourceLang,
            target: targetLang,
            model: model
        });
    },
    
    /**
     * Summarize text
     */
    async summarize(text, model, length, format) {
        return await this.post('/summarize', {
            text: text,
            model: model,
            length: length,
            format: format
        });
    },
    
    /**
     * Get supported languages
     */
    async getLanguages() {
        return await this.get('/languages');
    },
    
    /**
     * Get available translation models
     */
    async getTranslationModels() {
        return await this.get('/models/translation');
    },
    
    /**
     * Get available summarization models
     */
    async getSummarizationModels() {
        return await this.get('/models/summarization');
    }
};
