/**
 * UI Module - Handles all UI interactions and updates
 */

const UI = {
    /**
     * Update text statistics
     */
    updateStats(textAreaId, statsId) {
        const textArea = document.getElementById(textAreaId);
        const stats = document.getElementById(statsId);
        
        if (!textArea || !stats) return;
        
        const text = textArea.value;
        const charCount = text.length;
        const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
        
        stats.textContent = `Characters: ${charCount} | Words: ${wordCount}`;
    },
    
    /**
     * Show loading state on button
     */
    showLoading(buttonId, spinnerId) {
        const button = document.getElementById(buttonId);
        const spinner = document.getElementById(spinnerId);
        const btnText = button.querySelector('.btn-text');
        
        if (button && spinner) {
            button.disabled = true;
            spinner.classList.add('active');
            if (btnText) {
                btnText.style.opacity = '0.7';
            }
        }
    },
    
    /**
     * Hide loading state on button
     */
    hideLoading(buttonId, spinnerId) {
        const button = document.getElementById(buttonId);
        const spinner = document.getElementById(spinnerId);
        const btnText = button.querySelector('.btn-text');
        
        if (button && spinner) {
            button.disabled = false;
            spinner.classList.remove('active');
            if (btnText) {
                btnText.style.opacity = '1';
            }
        }
    },
    
    /**
     * Show status message
     */
    showStatus(message, type = 'info', duration = 3000) {
        const statusBar = document.getElementById('statusBar');
        const statusMessage = document.getElementById('statusMessage');
        
        if (!statusBar || !statusMessage) return;
        
        // Remove existing classes
        statusBar.classList.remove('success', 'error', 'show');
        
        // Set message and type
        statusMessage.textContent = message;
        if (type === 'success') {
            statusBar.classList.add('success');
        } else if (type === 'error') {
            statusBar.classList.add('error');
        }
        
        // Show status bar
        statusBar.classList.add('show');
        
        // Auto-hide after duration
        if (duration > 0) {
            setTimeout(() => {
                statusBar.classList.remove('show');
            }, duration);
        }
    },
    
    /**
     * Copy text to clipboard
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showStatus('✓ Copied to clipboard!', 'success', 2000);
            return true;
        } catch (error) {
            console.error('Copy failed:', error);
            this.showStatus('Failed to copy to clipboard', 'error');
            return false;
        }
    },
    
    /**
     * Download text as file
     */
    downloadText(text, filename = 'translated-text.txt') {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        this.showStatus('✓ File downloaded!', 'success', 2000);
    },
    
    /**
     * Populate language dropdown
     */
    populateLanguageDropdown(selectId, languages, excludeAuto = false) {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        select.innerHTML = '';
        
        languages.forEach(lang => {
            if (excludeAuto && lang.code === 'auto') return;
            
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = `${lang.name} (${lang.native})`;
            select.appendChild(option);
        });
    },
    
    /**
     * Toggle theme
     */
    toggleTheme() {
        const html = document.documentElement;
        const themeIcon = document.querySelector('.theme-icon');
        
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        if (themeIcon) {
            themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        }
    },
    
    /**
     * Load saved theme
     */
    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        const html = document.documentElement;
        const themeIcon = document.querySelector('.theme-icon');
        
        html.setAttribute('data-theme', savedTheme);
        
        if (themeIcon) {
            themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        }
    },
    
    /**
     * Toggle summary section
     */
    toggleSummarySection() {
        const summarySection = document.getElementById('summarySection');
        if (summarySection) {
            summarySection.classList.toggle('collapsed');
        }
    },
    
    /**
     * Enable/disable output buttons
     */
    updateOutputButtons(hasText) {
        const copyBtn = document.getElementById('copyOutput');
        const downloadBtn = document.getElementById('downloadOutput');
        
        if (copyBtn) copyBtn.disabled = !hasText;
        if (downloadBtn) downloadBtn.disabled = !hasText;
    },
    
    /**
     * Swap language selection
     */
    swapLanguages() {
        const sourceSelect = document.getElementById('sourceLanguage');
        const targetSelect = document.getElementById('targetLanguage');
        
        if (!sourceSelect || !targetSelect) return;
        
        // Don't swap if source is auto-detect
        if (sourceSelect.value === 'auto') {
            this.showStatus('Cannot swap with auto-detect', 'error', 2000);
            return;
        }
        
        // Swap values
        const temp = sourceSelect.value;
        sourceSelect.value = targetSelect.value;
        targetSelect.value = temp;
        
        this.showStatus('Languages swapped', 'success', 1500);
    },
    
    /**
     * Get selected radio value
     */
    getRadioValue(name) {
        const radio = document.querySelector(`input[name="${name}"]:checked`);
        return radio ? radio.value : null;
    },
    
    /**
     * Validate input text
     */
    validateInput(text, minLength = 1) {
        if (!text || !text.trim()) {
            this.showStatus('Please enter some text', 'error');
            return false;
        }
        
        if (text.trim().length < minLength) {
            this.showStatus(`Text must be at least ${minLength} characters`, 'error');
            return false;
        }
        
        return true;
    }
};
