# GitHub Contribution Wave Reveal Action

A GitHub Action that fetches your contribution calendar and generates a gorgeous SVG with a sweeping wave-reveal animation from left to right.

Perfect for making your GitHub Profile README look vibrant and alive!

## Preview

Here is an example of the generated SVG with the default **Cyberpunk** theme:

![Preview Example](./profile/wave-commits.svg)

## Features

- 🌊 **Sweeping Wave Reveal Effect**: Commits fade and slide up sequentially from left to right.
- 🎨 **Multiple Premium Themes**: Customize the card design to fit your profile aesthetic.
- 📅 **Dynamic Alignments**: Months and weekdays are automatically calculated and aligned, fading in sync with the wave.
- ⚡ **Lightweight**: Pure CSS animations embedded inside the SVG, requiring no external JavaScript dependencies.

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
          color_palette: 'cyberpunk' # Options: cyberpunk, ocean, sunset, classic-green

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
| `color_palette` | The color theme of the graph card (`cyberpunk`, `ocean`, `sunset`, `classic-green`). | No | `cyberpunk` |

---

## Color Palettes

### 1. Cyberpunk (Default)
- Card Background: Space Dark (`#0b0f19`)
- Accent: Blues, Purples, and Vibrant Pink
- Color Steps: `#161b22` ➔ `#1e3a8a` ➔ `#3b82f6` ➔ `#8b5cf6` ➔ `#ec4899`

### 2. Ocean
- Card Background: Deep Navy (`#020617`)
- Accent: Sky Blues & Cyans
- Color Steps: `#1e293b` ➔ `#0369a1` ➔ `#0284c7` ➔ `#38bdf8` ➔ `#06b6d4`

### 3. Sunset
- Card Background: Dark Crimson (`#180808`)
- Accent: Reds, Oranges, and Yellows
- Color Steps: `#2d1919` ➔ `#b91c1c` ➔ `#ea580c` ➔ `#f97316` ➔ `#facc15`

### 4. Classic Green
- Card Background: GitHub Dark (`#0d1117`)
- Accent: Default Green tones
- Color Steps: `#161b22` ➔ `#0e4429` ➔ `#006d32` ➔ `#26a641` ➔ `#39d353`

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute!
