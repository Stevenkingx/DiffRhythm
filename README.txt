# 🎵 DiffRhythm GPU API (Docker Image)

This Docker image runs a Flask-based API for generating AI music with vocals using the [DiffRhythm](https://github.com/ASLP-lab/DiffRhythm) project. It is optimized to run on GPU environments like RunPod.

---

## 🚀 Features

- Automatically clones DiffRhythm from GitHub
- Accepts lyrics in plain text, raw `.lrc`, or use the example LRC file
- Flask API runs on port `8080`
- Returns generated `.mp3` and `.lrc` file
- Ideal for testing and integration with Laravel, Python, or frontend apps

---

## 🧪 Example API Usage

### Generate music using the example `.lrc`:

```bash
curl -X POST http://<your-runpod-url>:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "demo_song",
    "use_example_lrc": true,
    "genre": "hip hop",
    "style": "male energetic vocal",
    "instruments": "808s, synths"
  }'
```

---

## 🛠 Run on RunPod (Recommended)

1. Go to [https://runpod.io/console](https://runpod.io/console)
2. Create a new **Custom GPU Pod**
3. Use the following configuration:

- **Container Image:** `stevenkingx/diffrhythm:latest`
- **Container Start Command:** `bash runpod_docker_start.sh`
- **HTTP Port:** `8080`

---

## 📂 File Structure

- `app.py` – Flask backend
- `templates/index.html` – Web form for local testing
- `runpod_docker_start.sh` – Start script
- `requirements.txt` – Python dependencies
- Docker auto-clones DiffRhythm into `/app/DiffRhythm`

---

## 📜 License

This project uses the [Stability AI License](https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md) from DiffRhythm and ASLP-Lab.

---

Created by [Stevenkingx](https://github.com/Stevenkingx)
