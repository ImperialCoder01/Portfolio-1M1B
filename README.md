# SwitchSmart: Project Portfolio

Switching off hidden energy waste in classrooms with sensors and AI.
Portfolio of **Vishal Kumar Tripathi** (B.Tech, 3rd Year, KCC Institute of Technology and Management), 1M1B Green Skills & Applied AI Internship, Batch 3.

A single static page that follows the project journey: problem, insights, AI-enabled solution, prototype, testing and results, impact, and what's next.

## Honest note on the evidence
- The classroom and washroom photos were taken at KCC on 8 Oct 2026.
- The prototype is a **Python simulation on synthetic data** (see `simulation/`), not a field test. Impact figures are assumptions and targets, not measured results.
- AI tools used: Claude (Anthropic) helped structure the work and write code and documents.

## Files
- `index.html`: the whole site (no build step, no dependencies)
- `assets/`: photos, charts and the portfolio PDF
- `simulation/`: `sim.py` and `charts.py` that produce the simulated results and charts (`pip install numpy pandas scikit-learn matplotlib pillow`)
- `vercel.json`: Vercel settings

## Run locally
Open `index.html` in a browser, or run `python3 -m http.server 8000` and visit http://localhost:8000.

## Deploy on Vercel
1. Push this folder to a GitHub repository.
2. On vercel.com choose **Add New > Project**, import the repository.
3. Framework Preset: **Other**. Leave Build Command and Output Directory empty. Click **Deploy**.

## Add the 1-minute video
Upload the video (YouTube unlisted or Drive), then add a link near the top of `index.html`, for example inside the hero: `<a class="btn" href="YOUR_VIDEO_LINK">Watch the 1-minute video</a>`.
