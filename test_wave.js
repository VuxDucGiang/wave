const fs = require('fs');
const path = require('path');

// Theme definitions matching generate_wave.py
const theme = {
  bg: "#0b0f19",
  border: "#1f2937",
  colors: ["#161b22", "#1e3a8a", "#3b82f6", "#8b5cf6", "#ec4899"]
};

// 4. Color Palette Mapping based on Contribution Count
function getColor(count) {
  const colors = theme.colors;
  if (count === 0) return colors[0];
  if (count <= 2) return colors[1];
  if (count <= 5) return colors[2];
  if (count <= 8) return colors[3];
  return colors[4];
}

// Generate mock contribution calendar data (53 weeks, 7 days per week)
const weeks = [];
for (let w = 0; w < 53; w++) {
  const contributionDays = [];
  for (let d = 0; d < 7; d++) {
    // Generate a random contribution count with a bias towards 0 or low counts
    const rand = Math.random();
    let count = 0;
    if (rand > 0.4) {
      count = Math.floor(Math.random() * 12);
    }
    contributionDays.push({
      weekday: d,
      contributionCount: count
    });
  }
  weeks.push({ contributionDays });
}

// Generate SVG content
const svg_width = 706;
const svg_height = 108;

let svg_content = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${svg_width} ${svg_height}" width="100%" height="100%">
  <style>
    /* Keyframes for the wave sweep effect */
    @keyframes wave-reveal {
      0% {
        opacity: 0;
        transform: translateY(8px) scale(0.8);
      }
      20% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
      90% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
      100% {
        opacity: 0;
        transform: translateY(8px) scale(0.8);
      }
    }
    
    .cell {
      opacity: 0;
      animation: wave-reveal 6s cubic-bezier(0.16, 1, 0.3, 1) infinite;
      transform-box: fill-box;
      transform-origin: center;
    }
  </style>

  <!-- Commits Grid (Wave Delay) -->
`;

// Append grid of cells
weeks.forEach((week, col_idx) => {
  week.contributionDays.forEach((day) => {
    const row_idx = day.weekday;
    const delay = (col_idx + row_idx) * 0.06; // Diagonal delay starting from top-left (0,0)
    const count = day.contributionCount;
    const color = getColor(count);
    
    const x_pos = 10 + col_idx * 13;
    const y_pos = 10 + row_idx * 13;
    
    svg_content += `  <rect class="cell" x="${x_pos}" y="${y_pos}" width="10" height="10" rx="2" fill="${color}" style="animation-delay: ${delay.toFixed(2)}s;" />\n`;
  });
});

svg_content += `</svg>\n`;

const outputPath = path.join(__dirname, 'profile', 'wave-commits.svg');
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, svg_content, 'utf8');

console.log(`[SUCCESS] Generated mock animated wave commit SVG at: ${outputPath}`);
