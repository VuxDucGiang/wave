import urllib.request
import json
import os
import datetime

# 1. Read parameters from environment variables
USERNAME = os.environ.get("GITHUB_USER_NAME")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "profile/wave-commits.svg")
TOKEN = os.environ.get("GITHUB_TOKEN")
THEME_NAME = os.environ.get("COLOR_PALETTE", "cyberpunk").lower()

if not USERNAME:
    print("[ERROR] GITHUB_USER_NAME environment variable is required.")
    exit(1)

if not TOKEN:
    print("[ERROR] GITHUB_TOKEN environment variable is required.")
    exit(1)

# 2. Premium Theme Configurations
THEMES = {
    "cyberpunk": {
        "bg": "#0b0f19",
        "border": "#1f2937",
        "title": "#f3f4f6",
        "subtitle": "#9ca3af",
        "label": "#6b7280",
        "colors": ["#161b22", "#1e3a8a", "#3b82f6", "#8b5cf6", "#ec4899"]
    },
    "ocean": {
        "bg": "#020617",
        "border": "#1e293b",
        "title": "#f8fafc",
        "subtitle": "#94a3b8",
        "label": "#64748b",
        "colors": ["#1e293b", "#0369a1", "#0284c7", "#38bdf8", "#06b6d4"]
    },
    "sunset": {
        "bg": "#180808",
        "border": "#3c1515",
        "title": "#fdf2f2",
        "subtitle": "#fca5a5",
        "label": "#f87171",
        "colors": ["#2d1919", "#b91c1c", "#ea580c", "#f97316", "#facc15"]
    },
    "classic-green": {
        "bg": "#0d1117",
        "border": "#30363d",
        "title": "#c9d1d9",
        "subtitle": "#8b949e",
        "label": "#8b949e",
        "colors": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    }
}

theme = THEMES.get(THEME_NAME, THEMES["cyberpunk"])

# 3. GraphQL Query
query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            weekday
          }
        }
      }
    }
  }
}
"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": {"login": USERNAME}}).encode("utf-8"),
    headers={
        "Authorization": f"bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Wave-Commits-Generator"
    }
)

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        if "errors" in res_data:
            print(f"[ERROR] API returned errors: {res_data['errors']}")
            exit(1)
        calendar = res_data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
except Exception as e:
    print(f"[ERROR] Failed to fetch data: {e}")
    exit(1)

total_commits = calendar["totalContributions"]
weeks = calendar["weeks"]

# 4. Color Palette Mapping based on Contribution Count
def get_color(count):
    colors = theme["colors"]
    if count == 0:
        return colors[0]
    elif count <= 2:
        return colors[1]
    elif count <= 5:
        return colors[2]
    elif count <= 8:
        return colors[3]
    else:
        return colors[4]

# 5. Map Month Labels to Columns
month_labels = []
months_map = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
}
prev_month = None
for col_idx, week in enumerate(weeks):
    if week["contributionDays"]:
        first_day = week["contributionDays"][0]
        month_str = first_day["date"].split("-")[1]
        curr_month = months_map[month_str]
        if curr_month != prev_month:
            month_labels.append((col_idx, curr_month))
            prev_month = curr_month

# 6. Generate SVG content
svg_width = 760
svg_height = 175

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&amp;display=swap');
    
    .card {{
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    
    .title {{
      font-size: 15px;
      font-weight: 600;
      fill: {theme["title"]};
    }}
    
    .subtitle {{
      font-size: 11px;
      fill: {theme["subtitle"]};
    }}
    
    .label {{
      font-size: 9px;
      fill: {theme["label"]};
    }}
    
    /* Keyframes for the wave sweep effect */
    @keyframes wave-reveal {{
      0% {{
        opacity: 0;
        transform: translateY(8px) scale(0.8);
      }}
      100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
      }}
    }}
    
    .cell {{
      opacity: 0;
      animation: wave-reveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      transform-box: fill-box;
      transform-origin: center;
    }}
    
    .fade-in {{
      opacity: 0;
      animation: fadeInEffect 0.8s ease-out forwards;
    }}
    
    @keyframes fadeInEffect {{
      100% {{ opacity: 1; }}
    }}
  </style>

  <!-- Card Background -->
  <rect width="{svg_width}" height="{svg_height}" rx="12" fill="{theme["bg"]}" stroke="{theme["border"]}" stroke-width="1.5" />
  
  <g class="card">
    <!-- Header -->
    <text x="25" y="30" class="title fade-in" style="animation-delay: 0.1s;">{USERNAME}'s Contribution Wave</text>
    <text x="25" y="48" class="subtitle fade-in" style="animation-delay: 0.2s;">{total_commits} contributions in the last year</text>

    <!-- Month Labels (fades in synchronized with the wave) -->
"""

# Append month labels
for col_idx, text in month_labels:
    x_pos = 35 + col_idx * 13
    delay = col_idx * 0.03
    svg_content += f'    <text x="{x_pos}" y="70" class="label" style="opacity: 0; animation: fadeInEffect 0.5s ease-out forwards; animation-delay: {delay:.2f}s;">{text}</text>\n'

# Append weekday labels
svg_content += f"""
    <!-- Weekday Labels -->
    <text x="15" y="93" class="label fade-in" style="animation-delay: 0.1s;">Mon</text>
    <text x="15" y="119" class="label fade-in" style="animation-delay: 0.1s;">Wed</text>
    <text x="15" y="145" class="label fade-in" style="animation-delay: 0.1s;">Fri</text>
    
    <!-- Commits Grid (Wave Delay) -->
"""

# Append grid of cells
for col_idx, week in enumerate(weeks):
    delay = col_idx * 0.03  # Sweep delay of 30ms per column
    for day in week["contributionDays"]:
        row_idx = day["weekday"]
        count = day["contributionCount"]
        color = get_color(count)
        
        x_pos = 35 + col_idx * 13
        y_pos = 85 + row_idx * 13
        
        svg_content += f'    <rect class="cell" x="{x_pos}" y="{y_pos}" width="10" height="10" rx="2" fill="{color}" style="animation-delay: {delay:.2f}s;" />\n'

# Append Legend
svg_content += f"""
    <!-- Legend -->
    <g transform="translate({svg_width - 150}, {svg_height - 25})" class="fade-in" style="animation-delay: 1.8s;">
      <text x="-30" y="9" class="label">Less</text>
      <rect x="0" y="0" width="10" height="10" rx="2" fill="{theme["colors"][0]}" />
      <rect x="15" y="0" width="10" height="10" rx="2" fill="{theme["colors"][1]}" />
      <rect x="30" y="0" width="10" height="10" rx="2" fill="{theme["colors"][2]}" />
      <rect x="45" y="0" width="10" height="10" rx="2" fill="{theme["colors"][3]}" />
      <rect x="60" y="0" width="10" height="10" rx="2" fill="{theme["colors"][4]}" />
      <text x="75" y="9" class="label">More</text>
    </g>
  </g>
</svg>
"""

# Ensure output path parent directory exists
os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_PATH)), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"[SUCCESS] Generated animated wave commit SVG at {OUTPUT_PATH} (Theme: {THEME_NAME})")
