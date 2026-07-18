# GitHub Contribution Wave Reveal Action

A GitHub Action that fetches your contribution calendar and generates a gorgeous, background-free SVG containing only your contribution cells with a diagonal sweeping wave animation. 

Perfect for blending seamlessly into your GitHub Profile README!

## Preview

Here is an example of the generated SVG with the **Mono** theme and transparent background:

<div align="center">
  <img src="./profile/wave-commits.svg" alt="Wave Commits Graph" width="800" />
</div>

## Features

- 🌊 **Diagonal Wave Reveal**: Commits fade in sequentially starting from the top-left corner, with the row above running 1 cell ahead of the row below.
- 🎨 **Seamless Integration**: Zero background and border, letting the contribution cells blend naturally into light or dark GitHub profiles.
- 🎬 **Multiple Animation Styles**: Choose between the classic pop-up bouncing wave (Style 1) or the clean, minimalist opacity-only fade (Style 2).
- 🎨 **Premium Palettes**: Features 5 curated color presets (Cyberpunk, Ocean, Sunset, Classic Green, and Grayscale Mono).
- ⚡ **Lightweight**: Pure CSS animations embedded inside the SVG, requiring no external fonts or JavaScript dependencies.

---

## How to Use

To add this contribution wave to your GitHub Profile README, create a workflow file (e.g. `.github/workflows/wave-commits.yml`) in your GitHub Profile repository:

```yaml
name: Generate Wave Commits

on:
  schedule:
    - cron: "0 0 * * *" # Run daily at midnight
  workflow_dispatch: # Run manually at any time
  push:
    branches:
      - main
      - master

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate Wave Commits SVG
        uses: VuxDucGiang/wave@main
        with:
          github_user_name: 'VuxDucGiang' # Change to your GitHub username
          output_path: 'profile/wave-commits.svg' # Path to save the SVG
          color_palette: 'mono' # Options: cyberpunk, ocean, sunset, classic-green, mono
          animation_style: '2' # Options: 1 (diagonal pop-up wave), 2 (diagonal pure opacity fade)

      - name: Commit and Push SVG
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add profile/wave-commits.svg
          git commit -m "Update animated wave commits SVG" || exit 0
          git push
```

After the workflow runs successfully, embed the image in your `README.md` file:

```markdown
<div align="center">
  <img src="./profile/wave-commits.svg" alt="Wave Commits Graph" width="800" />
</div>
```

---

## Inputs

| Input | Description | Required | Default |
| --- | --- | --- | --- |
| `github_user_name` | The GitHub username to retrieve contribution data for. | **Yes** | N/A |
| `output_path` | The path where the generated SVG file should be saved. | No | `profile/wave-commits.svg` |
| `color_palette` | The color theme of the contribution cells (`cyberpunk`, `ocean`, `sunset`, `classic-green`, `mono`). | No | `cyberpunk` |
| `animation_style` | The animation style preset (`1` for diagonal pop-up wave, `2` for diagonal pure opacity fade). | No | `1` |

---

## Color Palettes

### 1. Cyberpunk (Default)
- Accent: Blues, Purples, and Vibrant Pink
- Color Steps: `#161b22` ➔ `#1e3a8a` ➔ `#3b82f6` ➔ `#8b5cf6` ➔ `#ec4899`

### 2. Ocean
- Accent: Sky Blues & Cyans
- Color Steps: `#1e293b` ➔ `#0369a1` ➔ `#0284c7` ➔ `#38bdf8` ➔ `#06b6d4`

### 3. Sunset
- Accent: Reds, Oranges, and Yellows
- Color Steps: `#2d1919` ➔ `#b91c1c` ➔ `#ea580c` ➔ `#f97316` ➔ `#facc15`

### 4. Classic Green
- Accent: Default Green tones
- Color Steps: `#161b22` ➔ `#0e4429` ➔ `#006d32` ➔ `#26a641` ➔ `#39d353`

### 5. Mono
- Accent: Grayscale (Black, Grays, and White)
- Color Steps: `#161b22` ➔ `#404040` ➔ `#737373` ➔ `#a3a3a3` ➔ `#ffffff`

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute!
