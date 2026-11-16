/**
 * Writing Workshop - Interactive Linguistic Assistant
 */

class WritingWorkshop {
  constructor() {
    this.textarea = document.getElementById('writing-textarea');
    this.wordCountEl = document.getElementById('live-word-count');
    this.sentenceCountEl = document.getElementById('live-sentence-count');
    this.avgWordsEl = document.getElementById('live-avg-words');
    
    this.checklistEl = document.getElementById('writing-checklist');
    this.grammarFlagsEl = document.getElementById('writing-grammar-flags');
    this.linkingFoundEl = document.getElementById('linking-words-found');
    this.linkingMissingEl = document.getElementById('linking-words-missing');
    this.vocabSugEl = document.getElementById('vocab-suggestions-list');

    this.debounceTimer = null;
    this.bindEvents();
    if (this.textarea && this.textarea.value.trim().length > 0) {
      this.triggerAnalysis();
    }
  }

  bindEvents() {
    if (this.textarea) {
      this.textarea.addEventListener('input', () => {
        this.updateLiveCounters();
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => this.triggerAnalysis(), 600);
      });
    }

    // Prompt selection cards
    document.querySelectorAll('.prompt-card-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const title = e.currentTarget.getAttribute('data-title');
        const desc = e.currentTarget.getAttribute('data-desc');
        const cat = e.currentTarget.getAttribute('data-category');

        const titleInput = document.getElementById('writing-title-input');
        const catInput = document.getElementById('writing-cat-input');
        const promptDescEl = document.getElementById('active-prompt-description');

        if (titleInput) titleInput.value = title;
        if (catInput) catInput.value = cat;
        if (promptDescEl) {
          promptDescEl.innerHTML = `<strong>Prompt Goal:</strong> ${desc}`;
          promptDescEl.style.display = 'block';
        }
        showToast(`Loaded writing challenge: <em>${title}</em>`, "info");
      });
    });
  }

  updateLiveCounters() {
    const text = this.textarea.value.trim();
    const words = text ? text.split(/\s+/).filter(w => w.length > 0) : [];
    const sentences = text ? text.split(/[.!?]+/).filter(s => s.trim().length > 0) : [];

    const wCount = words.length;
    const sCount = sentences.length;
    const avg = sCount > 0 ? (wCount / sCount).toFixed(1) : 0;

    if (this.wordCountEl) this.wordCountEl.textContent = wCount;
    if (this.sentenceCountEl) this.sentenceCountEl.textContent = sCount;
    if (this.avgWordsEl) this.avgWordsEl.textContent = avg;
  }

  async triggerAnalysis() {
    const content = this.textarea.value.trim();
    if (!content) return;

    try {
      const data = await postData('/writing/analyze', { content: content });
      this.renderChecklist(data.checklist);
      this.renderGrammarFlags(data.grammar_flags);
      this.renderLinkingWords(data.linking_words_found, data.linking_suggestions);
      this.renderVocabSuggestions(data.vocab_suggestions);
    } catch (e) {
      console.error("Writing analysis error:", e);
    }
  }

  renderChecklist(checklist) {
    if (!this.checklistEl) return;
    this.checklistEl.innerHTML = (checklist || []).map(item => `
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;font-size:0.92rem;">
        <i class="fas ${item.passed ? 'fa-check-circle' : 'fa-times-circle'}" 
           style="color:${item.passed ? '#16a34a' : '#dc2626'};margin-top:4px;"></i>
        <div>
          <strong>${item.item}:</strong> 
          <span style="color:#475569;">${item.detail}</span>
        </div>
      </div>
    `).join('');
  }

  renderGrammarFlags(flags) {
    if (!this.grammarFlagsEl) return;
    if (!flags || flags.length === 0) {
      this.grammarFlagsEl.innerHTML = '<div style="color:#16a34a;font-size:0.92rem;"><i class="fas fa-check-double"></i> No common ESL grammatical patterns flagged! Great structure.</div>';
      return;
    }

    this.grammarFlagsEl.innerHTML = flags.map(f => `
      <div style="background:#fef2f2;border-left:4px solid #dc2626;padding:10px 14px;border-radius:6px;margin-bottom:8px;font-size:0.9rem;">
        <div style="color:#991b1b;font-weight:700;">Flagged phrase: "<em>${f.matched_text}</em>"</div>
        <div style="color:#334155;">${f.explanation}</div>
      </div>
    `).join('');
  }

  renderLinkingWords(found, missing) {
    if (this.linkingFoundEl) {
      const foundEntries = Object.entries(found || {});
      if (foundEntries.length === 0) {
        this.linkingFoundEl.innerHTML = '<span style="color:#94a3b8;font-size:0.9rem;">No discourse connectors detected yet. Try using "Furthermore", "However", or "Therefore".</span>';
      } else {
        this.linkingFoundEl.innerHTML = foundEntries.map(([cat, list]) => `
          <div style="margin-bottom:6px;">
            <span class="badge badge-b1">${cat}</span>: 
            <span style="font-weight:600;color:#0f766e;">${list.join(', ')}</span>
          </div>
        `).join('');
      }
    }

    if (this.linkingMissingEl) {
      if (!missing || missing.length === 0) {
        this.linkingMissingEl.innerHTML = '<span style="color:#16a34a;font-size:0.9rem;"><i class="fas fa-star"></i> Outstanding variety of transitions across all categories!</span>';
      } else {
        this.linkingMissingEl.innerHTML = `<span style="font-size:0.88rem;color:#64748b;">Consider adding transitions for: <strong>${missing.join(', ')}</strong></span>`;
      }
    }
  }

  renderVocabSuggestions(suggestions) {
    if (!this.vocabSugEl) return;
    if (!suggestions || suggestions.length === 0) {
      this.vocabSugEl.innerHTML = '<div style="color:#475569;font-size:0.9rem;">No overused basic words detected. Your vocabulary choices appear varied!</div>';
      return;
    }

    this.vocabSugEl.innerHTML = suggestions.map(s => `
      <div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:8px 12px;border-radius:6px;margin-bottom:8px;font-size:0.88rem;">
        <div><strong>Found basic word:</strong> "${s.original}"</div>
        <div style="color:#78350f;"><strong>Expressive alternatives:</strong> ${s.alternatives.join(', ')}</div>
      </div>
    `).join('');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('writing-textarea')) {
    window.writingApp = new WritingWorkshop();
  }
});
