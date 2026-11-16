/**
 * Lightweight Standalone HTML5 Canvas Charts (Zero CDN Dependency)
 */

const LearningCharts = {
  // Weekly Activity Bar Chart
  renderWeeklyActivity: function(canvasId, dailyData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    if (!dailyData || dailyData.length === 0) {
      ctx.fillStyle = "#64748b";
      ctx.font = "14px sans-serif";
      ctx.fillText("No activity logged this week yet.", width / 2 - 90, height / 2);
      return;
    }

    const maxVal = Math.max(...dailyData.map(d => d.xp || 10), 50);
    const paddingBottom = 30;
    const paddingTop = 25;
    const barWidth = Math.floor((width - 60) / dailyData.length) - 10;
    const startX = 40;

    // Grid line
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(startX - 10, height - paddingBottom);
    ctx.lineTo(width - 20, height - paddingBottom);
    ctx.stroke();

    dailyData.forEach((day, idx) => {
      const x = startX + idx * (barWidth + 10);
      const barHeight = ((day.xp || 0) / maxVal) * (height - paddingBottom - paddingTop);
      const y = height - paddingBottom - barHeight;

      // Draw Bar
      const grad = ctx.createLinearGradient(0, y, 0, height - paddingBottom);
      grad.addColorStop(0, '#3b82f6');
      grad.addColorStop(1, '#1e40af');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(x, y, barWidth, barHeight, [4, 4, 0, 0]) : ctx.rect(x, y, barWidth, barHeight);
      ctx.fill();

      // Value text
      ctx.fillStyle = "#1e293b";
      ctx.font = "bold 11px sans-serif";
      ctx.textAlign = "center";
      if (day.xp > 0) {
        ctx.fillText(`${day.xp} XP`, x + barWidth / 2, y - 6);
      }

      // Day label
      ctx.fillStyle = "#64748b";
      ctx.font = "11px sans-serif";
      const shortDay = day.label ? day.label.split(' ')[0] : `D${idx+1}`;
      ctx.fillText(shortDay, x + barWidth / 2, height - 10);
    });
  },

  // Category Grammar Accuracy Horizontal Bar Chart
  renderCategoryBars: function(canvasId, categories) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    if (!categories || categories.length === 0) {
      ctx.fillStyle = "#64748b";
      ctx.font = "14px sans-serif";
      ctx.fillText("Complete quizzes or the placement test to see topic diagnostics.", 20, height / 2);
      return;
    }

    const rowHeight = Math.min(36, Math.floor((height - 20) / categories.length));
    const labelWidth = 180;
    const maxBarWidth = width - labelWidth - 70;

    categories.slice(0, 8).forEach((cat, idx) => {
      const y = 20 + idx * rowHeight;
      const pct = cat.percentage || 0;
      const barW = (pct / 100) * maxBarWidth;

      // Category Name
      ctx.fillStyle = "#1e293b";
      ctx.font = "12px sans-serif";
      ctx.textAlign = "right";
      const truncatedName = cat.category.length > 22 ? cat.category.substring(0, 20) + '...' : cat.category;
      ctx.fillText(truncatedName, labelWidth - 10, y + 14);

      // Bar Background
      ctx.fillStyle = "#f1f5f9";
      ctx.fillRect(labelWidth, y, maxBarWidth, 16);

      // Bar Fill (Color-coded based on mastery)
      if (pct >= 75) {
        ctx.fillStyle = "#16a34a"; // Strong green
      } else if (pct >= 50) {
        ctx.fillStyle = "#f59e0b"; // Medium orange
      } else {
        ctx.fillStyle = "#dc2626"; // Weak red
      }
      ctx.fillRect(labelWidth, y, barW, 16);

      // Pct text
      ctx.fillStyle = "#475569";
      ctx.font = "bold 11px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(`${pct}%`, labelWidth + maxBarWidth + 10, y + 13);
    });
  },

  // Retention Donut Chart
  renderRetentionDonut: function(canvasId, mastered, learning, newWords) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    const total = (mastered || 0) + (learning || 0) + (newWords || 0);
    if (total === 0) {
      ctx.fillStyle = "#64748b";
      ctx.font = "14px sans-serif";
      ctx.fillText("No vocabulary data yet.", width / 2 - 70, height / 2);
      return;
    }

    const cx = width / 2;
    const cy = height / 2 - 10;
    const radius = Math.min(cx, cy) - 20;
    const innerRadius = radius * 0.6;

    const slices = [
      { count: mastered, color: '#16a34a', label: 'Mastered' },
      { count: learning, color: '#3b82f6', label: 'Learning' },
      { count: newWords, color: '#e2e8f0', label: 'New' }
    ];

    let startAngle = -0.5 * Math.PI;

    slices.forEach(slice => {
      const sliceAngle = (slice.count / total) * 2 * Math.PI;
      ctx.fillStyle = slice.color;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, startAngle, startAngle + sliceAngle);
      ctx.arc(cx, cy, innerRadius, startAngle + sliceAngle, startAngle, true);
      ctx.closePath();
      ctx.fill();
      startAngle += sliceAngle;
    });

    // Center text
    ctx.fillStyle = "#0f172a";
    ctx.font = "bold 20px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(total, cx, cy + 4);

    ctx.fillStyle = "#64748b";
    ctx.font = "11px sans-serif";
    ctx.fillText("TOTAL WORDS", cx, cy + 20);
  }
};
