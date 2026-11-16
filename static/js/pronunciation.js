/**
 * Pronunciation Laboratory - Web Speech Comparison & Recognition Engine
 */

class PronunciationLab {
  constructor() {
    this.recognition = null;
    this.activeCard = null;
    this.initSpeechRecognition();
    this.bindCards();
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Web Speech Recognition not supported in this browser.");
      return;
    }
    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    this.recognition.lang = 'en-US';

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (this.activeCard) {
        this.evaluatePronunciation(this.activeCard, transcript);
      }
    };

    this.recognition.onerror = (event) => {
      if (this.activeCard) {
        const statusBox = this.activeCard.querySelector('.pronunciation-status');
        if (statusBox) {
          statusBox.innerHTML = `<span style="color:#dc2626;"><i class="fas fa-exclamation-circle"></i> Recognition note: ${event.error}. Please check mic permissions and try speaking again.</span>`;
        }
      }
    };
  }

  bindCards() {
    document.querySelectorAll('.pronunciation-item').forEach(item => {
      const targetText = item.getAttribute('data-target');
      
      // Listen buttons
      const listenBtn = item.querySelector('.btn-listen');
      if (listenBtn) {
        listenBtn.addEventListener('click', () => {
          speakEnglish(targetText, 1.0);
        });
      }
      
      const listenSlowBtn = item.querySelector('.btn-listen-slow');
      if (listenSlowBtn) {
        listenSlowBtn.addEventListener('click', () => {
          speakEnglish(targetText, 0.7);
        });
      }

      // Record / Speak button
      const recordBtn = item.querySelector('.btn-record-speech');
      if (recordBtn) {
        recordBtn.addEventListener('click', () => {
          if (!this.recognition) {
            alert("Speech recognition is supported primarily in Google Chrome, Microsoft Edge, and Safari. Please use a supported browser for voice testing.");
            return;
          }
          this.activeCard = item;
          const statusBox = item.querySelector('.pronunciation-status');
          if (statusBox) {
            statusBox.innerHTML = '<span style="color:#16a34a;font-weight:700;"><i class="fas fa-microphone fa-bounce"></i> Listening... Speak the phrase clearly now!</span>';
          }
          try {
            this.recognition.start();
          } catch (e) {
            this.recognition.stop();
            setTimeout(() => this.recognition.start(), 200);
          }
        });
      }
    });
  }

  evaluatePronunciation(card, recognizedText) {
    const targetText = card.getAttribute('data-target').toLowerCase().replace(/[^\w\s]/g, '');
    const cleanRecognized = recognizedText.toLowerCase().replace(/[^\w\s]/g, '');

    const targetWords = targetText.split(/\s+/).filter(w => w.length > 0);
    const recognizedWords = cleanRecognized.split(/\s+/).filter(w => w.length > 0);

    let matchCount = 0;
    const diffMarkup = targetWords.map(tw => {
      if (recognizedWords.includes(tw)) {
        matchCount++;
        return `<span class="word-match-correct">${tw}</span>`;
      } else {
        return `<span class="word-match-diff">${tw}</span>`;
      }
    }).join(' ');

    const similarity = Math.round((matchCount / Math.max(1, targetWords.length)) * 100);
    const statusBox = card.querySelector('.pronunciation-status');

    let badgeClass = 'success';
    let feedback = '';
    if (similarity >= 80) {
      feedback = '🎉 Outstanding articulation! Highly accurate pronunciation.';
      badgeClass = 'success';
    } else if (similarity >= 50) {
      feedback = '👍 Good attempt! Review the highlighted words and try speaking a bit slower.';
      badgeClass = 'warning';
    } else {
      feedback = '🔁 Keep practicing. Listen to the slow audio sample and practice shadowing.';
      badgeClass = 'danger';
    }

    if (statusBox) {
      statusBox.innerHTML = `
        <div style="margin-top:10px;padding:12px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div><strong>Recognized Speech:</strong> "<em>${recognizedText}</em>"</div>
            <div class="badge badge-${similarity >= 80 ? 'a1' : 'b2'}" style="font-size:0.9rem;">${similarity}% Match</div>
          </div>
          <div style="font-size:1.05rem;margin-bottom:6px;"><strong>Word Breakdown:</strong> ${diffMarkup}</div>
          <div style="font-size:0.9rem;color:#475569;">${feedback}</div>
        </div>
      `;
    }

    // Award XP
    postData('/pronunciation/award-xp', {
      similarity: similarity,
      target: targetText
    }).then(res => {
      if (res && res.xp_earned) {
        showToast(`Earned <b>+${res.xp_earned} XP</b> in Pronunciation Lab!`, "success");
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.pronunciation-item')) {
    window.pronunciationApp = new PronunciationLab();
  }
});
