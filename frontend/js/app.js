/**
 * Main Application Module
 * Initializes the application and handles all events
 */

const App = {
    // Application state
    state: {
        languages: [],
        currentInputText: '',
        currentOutputText: ''
    },
    
    /**
     * Initialize the application
     */
    async init() {
        console.log('🚀 Initializing Arjun AI Text Tools...');
        
        // Load theme
        UI.loadTheme();
        
        // Load languages
        await this.loadLanguages();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Set default language selections
        this.setDefaultLanguages();
        
        console.log('✓ Application initialized successfully!');
    },
    
    /**
     * Load languages from backend
     */
    async loadLanguages() {
        try {
            const response = await API.getLanguages();
            
            if (response.success && response.languages) {
                this.state.languages = response.languages;
                
                // Populate language dropdowns
                UI.populateLanguageDropdown('sourceLanguage', this.state.languages);
                UI.populateLanguageDropdown('targetLanguage', this.state.languages, true);
                
                console.log('✓ Languages loaded:', this.state.languages.length);
            } else {
                console.error('Failed to load languages');
                UI.showStatus('Failed to load languages', 'error');
            }
        } catch (error) {
            console.error('Error loading languages:', error);
            UI.showStatus('Error loading languages', 'error');
        }
    },
    
    /**
     * Set default language selections
     */
    setDefaultLanguages() {
        const sourceSelect = document.getElementById('sourceLanguage');
        const targetSelect = document.getElementById('targetLanguage');
        
        if (sourceSelect) sourceSelect.value = 'auto';
        if (targetSelect) targetSelect.value = 'hi'; // Default to Hindi
    },
    
    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => UI.toggleTheme());
        }
        
        // Input text changes
        const inputText = document.getElementById('inputText');
        if (inputText) {
            inputText.addEventListener('input', () => {
                this.state.currentInputText = inputText.value;
                UI.updateStats('inputText', 'inputStats');
            });
        }
        
        // Clear input button
        const clearInput = document.getElementById('clearInput');
        if (clearInput) {
            clearInput.addEventListener('click', () => this.clearInput());
        }
        
        // Swap languages button
        const swapLanguages = document.getElementById('swapLanguages');
        if (swapLanguages) {
            swapLanguages.addEventListener('click', () => UI.swapLanguages());
        }
        
        // Translate button
        const translateBtn = document.getElementById('translateBtn');
        if (translateBtn) {
            translateBtn.addEventListener('click', () => this.handleTranslate());
        }
        
        // Copy output button
        const copyOutput = document.getElementById('copyOutput');
        if (copyOutput) {
            copyOutput.addEventListener('click', () => this.handleCopy());
        }
        
        // Download output button
        const downloadOutput = document.getElementById('downloadOutput');
        if (downloadOutput) {
            downloadOutput.addEventListener('click', () => this.handleDownload());
        }
        
        // Summary section toggle
        const summaryToggle = document.getElementById('summaryToggle');
        if (summaryToggle) {
            summaryToggle.addEventListener('click', () => UI.toggleSummarySection());
        }
        
        // Summarize button
        const summarizeBtn = document.getElementById('summarizeBtn');
        if (summarizeBtn) {
            summarizeBtn.addEventListener('click', () => this.handleSummarize());
        }
    },
    
    /**
     * Clear input text
     */
    clearInput() {
        const inputText = document.getElementById('inputText');
        if (inputText) {
            inputText.value = '';
            this.state.currentInputText = '';
            UI.updateStats('inputText', 'inputStats');
        }
    },
    
    /**
     * Handle translation
     */
    async handleTranslate() {
        const inputText = document.getElementById('inputText');
        const outputText = document.getElementById('outputText');
        const sourceLanguage = document.getElementById('sourceLanguage');
        const targetLanguage = document.getElementById('targetLanguage');
        const translationModel = document.getElementById('translationModel');
        
        if (!inputText || !outputText) return;
        
        const text = inputText.value.trim();
        
        // Validate input
        if (!UI.validateInput(text)) return;
        
        // Show loading
        UI.showLoading('translateBtn', 'translateSpinner');
        UI.showStatus('Translating...', 'info', 0);
        
        try {
            const response = await API.translate(
                text,
                sourceLanguage.value,
                targetLanguage.value,
                translationModel.value
            );
            
            if (response.success) {
                outputText.value = response.translated_text;
                this.state.currentOutputText = response.translated_text;
                UI.updateStats('outputText', 'outputStats');
                UI.updateOutputButtons(true);
                UI.showStatus(
                    `✓ Translated in ${response.processing_time}s`,
                    'success',
                    3000
                );
            } else {
                outputText.value = '';
                UI.showStatus(
                    response.error || 'Translation failed',
                    'error',
                    5000
                );
            }
        } catch (error) {
            console.error('Translation error:', error);
            UI.showStatus('An error occurred during translation', 'error');
        } finally {
            UI.hideLoading('translateBtn', 'translateSpinner');
        }
    },
    
    /**
     * Handle summarization
     */
    async handleSummarize() {
        const inputText = document.getElementById('inputText');
        const outputText = document.getElementById('outputText');
        const summaryModel = document.getElementById('summaryModel');
        
        if (!inputText || !outputText) return;
        
        // Get summary settings
        const length = UI.getRadioValue('summaryLength') || 'short';
        const format = UI.getRadioValue('summaryFormat') || 'paragraph';
        const source = UI.getRadioValue('summarySource') || 'original';
        
        // Determine which text to summarize
        let text;
        if (source === 'translated') {
            text = outputText.value.trim();
            if (!UI.validateInput(text, 50)) {
                UI.showStatus('Please translate text first or select "Original Text"', 'error');
                return;
            }
        } else {
            text = inputText.value.trim();
            if (!UI.validateInput(text, 50)) {
                UI.showStatus('Text must be at least 50 characters for summarization', 'error');
                return;
            }
        }
        
        // Show loading
        UI.showLoading('summarizeBtn', 'summarizeSpinner');
        UI.showStatus('Summarizing...', 'info', 0);
        
        try {
            const response = await API.summarize(
                text,
                summaryModel.value,
                length,
                format
            );
            
            if (response.success) {
                outputText.value = response.summary;
                this.state.currentOutputText = response.summary;
                UI.updateStats('outputText', 'outputStats');
                UI.updateOutputButtons(true);
                UI.showStatus(
                    `✓ Summarized in ${response.processing_time}s`,
                    'success',
                    3000
                );
            } else {
                UI.showStatus(
                    response.error || 'Summarization failed',
                    'error',
                    5000
                );
            }
        } catch (error) {
            console.error('Summarization error:', error);
            UI.showStatus('An error occurred during summarization', 'error');
        } finally {
            UI.hideLoading('summarizeBtn', 'summarizeSpinner');
        }
    },
    
    /**
     * Handle copy output
     */
    handleCopy() {
        const outputText = document.getElementById('outputText');
        if (outputText && outputText.value) {
            UI.copyToClipboard(outputText.value);
        }
    },
    
    /**
     * Handle download output
     */
    handleDownload() {
        const outputText = document.getElementById('outputText');
        if (outputText && outputText.value) {
            const timestamp = new Date().toISOString().split('T')[0];
            const filename = `arjun-ai-tools-${timestamp}.txt`;
            UI.downloadText(outputText.value, filename);
        }
    }
};

// Initialize application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}
