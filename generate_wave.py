import urllib.request
import json
import os
import datetime

# 1. Read parameters from environment variables
USERNAME = os.environ.get("GITHUB_USER_NAME")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "profile/wave-commits.svg")
TOKEN = os.environ.get("GITHUB_TOKEN")
THEME_NAME = os.environ.get("COLOR_PALETTE", "cyberpunk").lower()
ANIMATION_STYLE = os.environ.get("ANIMATION_STYLE", "1")

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
    },
    "mono": {
        "bg": "#000000",
        "border": "#262626",
        "title": "#ffffff",
        "subtitle": "#a3a3a3",
        "label": "#737373",
        "colors": ["#161b22", "#404040", "#737373", "#a3a3a3", "#ffffff"]
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

# 5. Generate SVG content
svg_width = 706
svg_height = 108

if ANIMATION_STYLE == "2":
    duration = "6s"
    keyframes = """      0% {
        opacity: 0;
      }
      20% {
        opacity: 1;
      }
      90% {
        opacity: 1;
      }
      100% {
        opacity: 0;
      }"""
else:
    duration = "6s"
    keyframes = """      0% {
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
      }"""

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">
  <style>
    /* Keyframes for the wave sweep effect */
    @keyframes wave-reveal {{
{keyframes}
    }}
    
    .cell {{
      opacity: 0;
      animation: wave-reveal {duration} cubic-bezier(0.16, 1, 0.3, 1) infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
  </style>
  <!-- Commits Grid (Wave Delay) -->
"""

# Append grid of cells
for col_idx, week in enumerate(weeks):
    for day in week["contributionDays"]:
        row_idx = day["weekday"]
        delay = (col_idx + row_idx) * 0.06
        count = day["contributionCount"]
        color = get_color(count)
        
        x_pos = 10 + col_idx * 13
        y_pos = 10 + row_idx * 13
        
        svg_content += f'  <rect class="cell" x="{x_pos}" y="{y_pos}" width="10" height="10" rx="2" fill="{color}" style="animation-delay: {delay:.2f}s;" />\n'

svg_content += """</svg>
"""

# Ensure output path parent directory exists
os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_PATH)), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"[SUCCESS] Generated animated wave commit SVG at {OUTPUT_PATH} (Theme: {THEME_NAME})")
