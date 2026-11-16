/**
 * Interactive Quiz Engine with Immediate Pedagogical Feedback
 */

function setupInteractiveQuiz(containerId, submitUrl, onComplete) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const form = container.querySelector('form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    // Check if form should submit via AJAX
    if (form.getAttribute('data-ajax') !== 'true') return;
    
    e.preventDefault();
    const formData = new FormData(form);
    const answers = {};
    for (let [key, val] of formData.entries()) {
      if (key.startsWith('q_')) {
        answers[key.replace('q_', '')] = val;
      }
    }

    try {
      const res = await postData(submitUrl, answers);
      
      // Highlight answers in DOM
      if (res.results) {
        res.results.forEach(r => {
          const qBox = document.getElementById(`quiz-card-${r.quiz_id}`);
          if (qBox) {
            const expBox = qBox.querySelector('.quiz-explanation');
            if (expBox) {
              expBox.style.display = 'block';
              expBox.className = `quiz-explanation ${r.is_correct ? 'success' : 'danger'}`;
              expBox.innerHTML = `<strong>${r.is_correct ? '✅ Correct!' : '❌ Incorrect.'}</strong> ${r.explanation}`;
            }
          }
        });
      }

      showToast(`Quiz completed! You scored ${res.percentage}% and earned <b>+${res.xp_earned} XP</b>!`, "success");
      if (typeof onComplete === 'function') {
        onComplete(res);
      }
    } catch (err) {
      console.error("Quiz submission error:", err);
    }
  });
}
