/**
 * Advanced English Learning Platform - Global Application Script
 */

// Text-to-Speech Engine via Web Speech API
function speakEnglish(text, rate = 1.0) {
  if (!('speechSynthesis' in window)) {
    alert("Text-to-speech is not supported in your browser.");
    return;
  }
  
  window.speechSynthesis.cancel(); // Stop any pending speech
  
  const cleanText = text.replace(/\[.*?\]/g, '').trim();
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = 'en-US';
  utterance.rate = parseFloat(rate) || 1.0;
  utterance.pitch = 1.0;
  
  // Try to pick natural English voice
  const voices = window.speechSynthesis.getVoices();
  const naturalVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Siri')));
  if (naturalVoice) {
    utterance.voice = naturalVoice;
  }
  
  window.speechSynthesis.speak(utterance);
}

// CSRF Token Helper for fetch requests
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : '';
}

// Generic Fetch Wrapper with CSRF header
async function postData(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify(data)
  });
  return response.json();
}

// Simple Toast Notification
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
    document.body.appendChild(container);
  }
  
  const toast = document.createElement('div');
  const bg = type === 'success' ? '#16a34a' : (type === 'danger' ? '#dc2626' : '#1e40af');
  toast.style.cssText = `background:${bg};color:#fff;padding:12px 20px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);font-weight:600;display:flex;align-items:center;gap:8px;animation:fadeIn 0.3s ease;`;
  toast.innerHTML = message;
  
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

// Mobile Navbar Toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('nav-toggle-btn');
  const navLinks = document.getElementById('nav-links');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }
  
  // Pre-load synthesis voices
  if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => {
      window.speechSynthesis.getVoices();
    };
  }
});
