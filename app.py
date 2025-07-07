from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import uuid
import os

app = Flask(__name__)

def format_lrc(lyrics_text, output_path, start_sec=10.0, interval=3.2):
    lines = lyrics_text.strip().split("\n")
    lrc_lines = []
    for i, line in enumerate(lines):
        total_sec = start_sec + i * interval
        mins = int(total_sec // 60)
        secs = total_sec % 60
        timestamp = f"[{mins:02}:{secs:05.2f}]"
        lrc_lines.append(f"{timestamp}{line.strip()}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lrc_lines))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    title = data.get("title", "untitled").replace(" ", "_").lower()
    lyrics = data.get("lyrics", "")
    genre = data.get("genre", "")
    style = data.get("style", "")
    instruments = data.get("instruments", "")
    raw_lrc = data.get("raw_lrc", None)
    use_example_lrc = data.get("use_example_lrc", False)

    style_text = f"{style} singing.\nGenre: {genre}.\nInstruments: {instruments}"
    uid = str(uuid.uuid4())
    base_dir = f"outputs/{uid}"
    os.makedirs(base_dir, exist_ok=True)

    # 📁 Seleccionar fuente del .lrc
    if use_example_lrc:
        lrc_path = "infer/example/eg_en.lrc"
        with open(lrc_path, "r", encoding="utf-8") as f:
            lrc_content = f.read()
    else:
        lrc_path = os.path.join(base_dir, f"{title}.lrc")
        if raw_lrc:
            with open(lrc_path, "w", encoding="utf-8") as f:
                f.write(raw_lrc.strip())
            lrc_content = raw_lrc.strip()
        else:
            if not lyrics.strip():
                return jsonify({"status": "error", "error": "Lyrics are required if not using example or raw LRC."}), 400
            format_lrc(lyrics, lrc_path)
            with open(lrc_path, "r", encoding="utf-8") as f:
                lrc_content = f.read()

    # 🎧 Ejecutar el modelo
    cmd = [
        "python3", "infer/infer.py",
        "--lrc-path", lrc_path,
        "--ref-prompt", style_text,
        "--audio-length", "95",
        "--repo-id", "ASLP-lab/DiffRhythm-base",
        "--output-dir", base_dir
    ]

    try:
        print("🎧 Ejecutando:", " ".join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        wav_file = os.path.join(base_dir, "output.wav")
        mp3_file = os.path.join(base_dir, f"{title}.mp3")

        subprocess.run([
            "ffmpeg", "-y", "-i", wav_file, "-codec:a", "libmp3lame", mp3_file
        ], check=True)

        return jsonify({
            "status": "success",
            "title": title,
            "id": uid,
            "url": f"http://{request.host}/audio/{uid}/{title}.mp3",
            "lrc_url": f"http://{request.host}/audio/{uid}/{title}.lrc" if not use_example_lrc else "https://raw.githubusercontent.com/ASLP-lab/DiffRhythm/main/infer/example/eg_en.lrc",
            "lrc": lrc_content,
            "log": result.stdout.strip()
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "error": e.stderr.strip() if e.stderr else str(e),
            "output": e.stdout.strip() if e.stdout else "No stdout"
        }), 500

@app.route('/audio/<uid>/<filename>', methods=['GET'])
def get_audio(uid, filename):
    path = f"outputs/{uid}/{filename}"
    if os.path.exists(path):
        return send_file(path, mimetype="audio/mpeg" if filename.endswith(".mp3") else "text/plain")
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
