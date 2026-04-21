from flask import Flask, request, jsonify

# Import your modules
from modules.song_interpreter import interpret_song
from modules.poetry_meter import analyze_meter
from modules.summarizer import summarize_text

app = Flask(__name__)

# -------------------------------
# 1. Song Meaning API
# -------------------------------
@app.route('/api/interpret', methods=['POST'])
def interpret():
    try:
        data = request.get_json()
        text = data.get("text", "")

        result = interpret_song(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500 


# -------------------------------
# 2. Poetry Meter API
# -------------------------------
@app.route('/api/meter', methods=['POST'])
def meter():
    try:
        data = request.get_json()
        text = data.get("text", "")

        result = analyze_meter(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# 3. Text Summarization API
# -------------------------------
@app.route('/api/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")

        result = summarize_text(text)
        return jsonify({"summary": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#@app.route('/')
#def home():
   # return "Flask API is running 🚀"

@app.route('/test-summary')
def test_summary():
    sample = "Natural language processing is a field of artificial intelligence that helps computers understand human language."
    return {"summary": summarize_text(sample)}
# -------------------------------
# Run Server
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)