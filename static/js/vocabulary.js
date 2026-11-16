/**
 * Spaced Repetition Flashcard Interactive Engine
 */

class VocabSRSDeck {
  constructor(cards) {
    this.cards = cards || [];
    this.currentIndex = 0;
    this.isFlipped = false;

    this.cardEl = document.getElementById('srs-flashcard');
    this.counterEl = document.getElementById('srs-counter');
    this.actionsEl = document.getElementById('srs-actions');
    this.finishedEl = document.getElementById('srs-finished');

    this.frontWord = document.getElementById('card-word');
    this.frontPhonetic = document.getElementById('card-phonetic');
    this.frontPos = document.getElementById('card-pos');
    this.frontCategory = document.getElementById('card-category');

    this.backDefEn = document.getElementById('card-def-en');
    this.backDefKm = document.getElementById('card-def-km');
    this.backExample = document.getElementById('card-example');

    this.favoriteBtn = document.getElementById('card-fav-btn');
    this.audioBtn = document.getElementById('card-audio-btn');

    this.bindEvents();
    this.renderCard();
  }

  bindEvents() {
    if (this.cardEl) {
      this.cardEl.addEventListener('click', (e) => {
        // Prevent flipping if clicking audio or favorite button
        if (e.target.closest('#card-audio-btn') || e.target.closest('#card-fav-btn')) return;
        this.flip();
      });
    }

    if (this.audioBtn) {
      this.audioBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.playAudio();
      });
    }

    if (this.favoriteBtn) {
      this.favoriteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleFavorite();
      });
    }

    // Rating buttons
    document.querySelectorAll('.btn-srs-rating').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const rating = e.currentTarget.getAttribute('data-rating');
        this.submitRating(rating);
      });
    });

    // Keyboard Shortcuts: Space to flip, 1-4 for ratings
    document.addEventListener('keydown', (e) => {
      // Don't trigger if typing in an input
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      if (e.code === 'Space') {
        e.preventDefault();
        this.flip();
      } else if (this.isFlipped) {
        if (e.key === '1') this.submitRating('again');
        else if (e.key === '2') this.submitRating('hard');
        else if (e.key === '3') this.submitRating('good');
        else if (e.key === '4') this.submitRating('easy');
      }
    });
  }

  renderCard() {
    if (this.currentIndex >= this.cards.length) {
      this.showFinished();
      return;
    }

    const card = this.cards[this.currentIndex];
    this.isFlipped = false;

    // Reset view to front
    document.getElementById('card-front').style.display = 'block';
    document.getElementById('card-back').style.display = 'none';
    if (this.actionsEl) this.actionsEl.style.display = 'none';

    // Populate data
    this.frontWord.textContent = card.word;
    this.frontPhonetic.textContent = card.phonetic || '';
    this.frontPos.textContent = card.part_of_speech || '';
    this.frontCategory.textContent = card.category || '';

    this.backDefEn.textContent = card.definition_en;
    this.backDefKm.textContent = card.definition_km;
    this.backExample.textContent = `"${card.example_sentence}"`;

    if (this.favoriteBtn) {
      this.favoriteBtn.innerHTML = card.is_favorite 
        ? '<i class="fas fa-star" style="color:#f59e0b;"></i>' 
        : '<i class="far fa-star"></i>';
    }

    if (this.counterEl) {
      this.counterEl.textContent = `Card ${this.currentIndex + 1} of ${this.cards.length}`;
    }

    // Play word audio automatically
    this.playAudio();
  }

  flip() {
    this.isFlipped = !this.isFlipped;
    const front = document.getElementById('card-front');
    const back = document.getElementById('card-back');

    if (this.isFlipped) {
      front.style.display = 'none';
      back.style.display = 'block';
      if (this.actionsEl) this.actionsEl.style.display = 'grid';
    } else {
      front.style.display = 'block';
      back.style.display = 'none';
      if (this.actionsEl) this.actionsEl.style.display = 'none';
    }
  }

  playAudio() {
    const card = this.cards[this.currentIndex];
    if (card && card.word) {
      speakEnglish(card.word);
    }
  }

  async toggleFavorite() {
    const card = this.cards[this.currentIndex];
    if (!card) return;

    try {
      const res = await postData(`/vocabulary/favorite/${card.vocab_id}`, {});
      card.is_favorite = res.is_favorite;
      this.favoriteBtn.innerHTML = card.is_favorite 
        ? '<i class="fas fa-star" style="color:#f59e0b;"></i>' 
        : '<i class="far fa-star"></i>';
      showToast(card.is_favorite ? "Added to favorites!" : "Removed from favorites", "info");
    } catch (e) {
      console.error(e);
    }
  }

  async submitRating(rating) {
    const card = this.cards[this.currentIndex];
    if (!card) return;

    try {
      await postData('/vocabulary/review', {
        vocab_id: card.vocab_id,
        rating: rating
      });
      showToast(`Scheduled with spaced repetition: <b>${rating.toUpperCase()}</b>`, "success");
    } catch (e) {
      console.error(e);
    }

    this.currentIndex++;
    this.renderCard();
  }

  showFinished() {
    if (this.cardEl) this.cardEl.style.display = 'none';
    if (this.actionsEl) this.actionsEl.style.display = 'none';
    if (this.counterEl) this.counterEl.style.display = 'none';
    if (this.finishedEl) this.finishedEl.style.display = 'block';
  }
}

// Global initialization helper
window.initVocabSRS = function(cardsData) {
  window.vocabApp = new VocabSRSDeck(cardsData);
};
