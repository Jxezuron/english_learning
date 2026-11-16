/**
 * Interactive Speaking Presentation Timer & Speech Recognition Pad
 */

class SpeakingWorkstation {
  constructor() {
    this.timerDisplay = document.getElementById('timer-display');
    this.timerStatus = document.getElementById('timer-status');
    this.timerBar = document.getElementById('timer-bar');
    this.startBtn = document.getElementById('start-speaking-btn');
    this.pauseBtn = document.getElementById('pause-speaking-btn');
    this.resetBtn = document.getElementById('reset-speaking-btn');
    this.prepBtn = document.getElementById('prep-timer-btn');
    this.transcriptArea = document.getElementById('recorded-transcript');
    this.durationInput = document.getElementById('duration_seconds');
    this.wordCountDisplay = document.getElementById('transcript-word-count');
    this.micStatus = document.getElementById('mic-status');
    this.micToggleBtn = document.getElementById('toggle-mic-btn');

    this.timerInterval = null;
    this.elapsedSeconds = 0;
    this.mode = 'idle'; // 'prep', 'speaking', 'paused'
    this.prepSecondsLeft = 30;

    this.recognition = null;
    this.isRecording = false;

    this.initTimer();
    this.initSpeechRecognition();
  }

  initTimer() {
    if (this.startBtn) {
      this.startBtn.addEventListener('click', () => this.startSpeaking());
    }
    if (this.pauseBtn) {
      this.pauseBtn.addEventListener('click', () => this.pauseTimer());
    }
    if (this.resetBtn) {
      this.resetBtn.addEventListener('click', () => this.resetTimer());
    }
    if (this.prepBtn) {
      this.prepBtn.addEventListener('click', () => this.startPreparation());
    }
    if (this.transcriptArea) {
      this.transcriptArea.addEventListener('input', () => this.updateTranscriptMetrics());
    }
  }

  startPreparation() {
    this.resetTimer();
    this.mode = 'prep';
    this.prepSecondsLeft = 30;
    this.timerStatus.textContent = '⏱️ PREPARATION TIME: Outline your main points (30s)';
    this.timerDisplay.className = 'timer-display prep';

    clearInterval(this.timerInterval);
    this.timerInterval = setInterval(() => {
      this.prepSecondsLeft--;
      const s = this.prepSecondsLeft;
      this.timerDisplay.textContent = `0:${s < 10 ? '0' : ''}${s}`;
      this.timerBar.style.width = `${((30 - s) / 30) * 100}%`;

      if (this.prepSecondsLeft <= 0) {
        clearInterval(this.timerInterval);
        this.timerStatus.textContent = '🚀 TIME IS UP! Start your presentation now!';
        if ('speechSynthesis' in window) {
          speakEnglish("Time is up. Begin your presentation now!");
        }
        setTimeout(() => this.startSpeaking(), 1000);
      }
    }, 1000);
  }

  startSpeaking() {
    if (this.mode === 'speaking') return;
    this.mode = 'speaking';
    this.timerDisplay.className = 'timer-display speaking';

    if (this.startBtn) this.startBtn.disabled = true;
    if (this.pauseBtn) this.pauseBtn.disabled = false;

    // Start speech recognition automatically if desired
    if (this.recognition && !this.isRecording) {
      try { this.recognition.start(); } catch (e) {}
    }

    clearInterval(this.timerInterval);
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds++;
      this.renderTimer();
    }, 1000);
  }

  pauseTimer() {
    this.mode = 'paused';
    clearInterval(this.timerInterval);
    if (this.startBtn) this.startBtn.disabled = false;
    if (this.pauseBtn) this.pauseBtn.disabled = true;
    if (this.timerStatus) this.timerStatus.textContent = '⏸️ Presentation Paused';

    if (this.recognition && this.isRecording) {
      try { this.recognition.stop(); } catch (e) {}
    }
  }

  resetTimer() {
    clearInterval(this.timerInterval);
    this.elapsedSeconds = 0;
    this.mode = 'idle';
    if (this.startBtn) this.startBtn.disabled = false;
    if (this.pauseBtn) this.pauseBtn.disabled = true;
    if (this.timerDisplay) {
      this.timerDisplay.textContent = '0:00';
      this.timerDisplay.className = 'timer-display';
    }
    if (this.timerBar) this.timerBar.style.width = '0%';
    if (this.timerStatus) this.timerStatus.textContent = 'Target Presentation: 2:00 – 3:00 Minutes';
    if (this.durationInput) this.durationInput.value = '0';
  }

  renderTimer() {
    const mins = Math.floor(this.elapsedSeconds / 60);
    const secs = this.elapsedSeconds % 60;
    this.timerDisplay.textContent = `${mins}:${secs < 10 ? '0' : ''}${secs}`;

    if (this.durationInput) {
      this.durationInput.value = this.elapsedSeconds;
    }

    // 180 seconds target (3 minutes = 100% progress)
    const progressPct = Math.min(100, (this.elapsedSeconds / 180) * 100);
    this.timerBar.style.width = `${progressPct}%`;

    // Visual pacing cues
    if (this.elapsedSeconds < 120) {
      this.timerStatus.textContent = `🎙️ In Progress: Building body points (${120 - this.elapsedSeconds}s to minimum 2m benchmark)`;
      this.timerDisplay.className = 'timer-display speaking';
    } else if (this.elapsedSeconds >= 120 && this.elapsedSeconds < 150) {
      this.timerStatus.textContent = '🎯 Target Reached! (2:00 - 2:30) You are in the ideal presentation zone!';
      this.timerDisplay.className = 'timer-display speaking';
      this.timerBar.style.background = 'linear-gradient(90deg, #10b981, #0d9488)';
    } else if (this.elapsedSeconds >= 150 && this.elapsedSeconds <= 180) {
      this.timerStatus.textContent = '⚠️ Concluding Window: Deliver your final memorable takeaway!';
      this.timerDisplay.className = 'timer-display prep';
    } else {
      this.timerStatus.textContent = '🛑 Over 3 Minutes: Please conclude your speech to respect standard time limits.';
      this.timerDisplay.className = 'timer-display warning';
    }
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (this.micStatus) {
        this.micStatus.innerHTML = '<span style="color:#d97706;"><i class="fas fa-exclamation-triangle"></i> Browser Note: Real-time speech-to-text requires Google Chrome, Edge, or a Web Speech-supported browser. You can still type your speech notes freely!</span>';
      }
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-US';

    this.recognition.onstart = () => {
      this.isRecording = true;
      if (this.micStatus) {
        this.micStatus.innerHTML = '<span style="color:#16a34a;font-weight:700;"><i class="fas fa-microphone"></i> Microphone Active: Transcribing your speech...</span>';
      }
      if (this.micToggleBtn) {
        this.micToggleBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Mic';
        this.micToggleBtn.className = 'btn btn-sm btn-outline';
      }
    };

    this.recognition.onresult = (event) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript + ' ';
        }
      }
      if (finalTranscript && this.transcriptArea) {
        this.transcriptArea.value = (this.transcriptArea.value + ' ' + finalTranscript).trim();
        this.updateTranscriptMetrics();
      }
    };

    this.recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
    };

    this.recognition.onend = () => {
      this.isRecording = false;
      if (this.micStatus) {
        this.micStatus.innerHTML = '<span style="color:#6b7280;"><i class="fas fa-microphone-slash"></i> Microphone idle. Click to start recording.</span>';
      }
      if (this.micToggleBtn) {
        this.micToggleBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Mic';
        this.micToggleBtn.className = 'btn btn-sm btn-secondary';
      }
    };

    if (this.micToggleBtn) {
      this.micToggleBtn.addEventListener('click', () => {
        if (this.isRecording) {
          this.recognition.stop();
        } else {
          this.recognition.start();
        }
      });
    }
  }

  updateTranscriptMetrics() {
    if (!this.transcriptArea) return;
    const words = this.transcriptArea.value.trim().split(/\s+/).filter(w => w.length > 0);
    const count = words.length;
    if (this.wordCountDisplay) {
      this.wordCountDisplay.textContent = `${count} words`;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('timer-display')) {
    window.speakingApp = new SpeakingWorkstation();
  }
});
