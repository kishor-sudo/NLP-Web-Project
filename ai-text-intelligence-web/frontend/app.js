const BASE_URL = "http://127.0.0.1:5000";

// SONG
async function analyzeSong() {
    const text = document.getElementById("songInput").value;

    const res = await fetch(`${BASE_URL}/api/interpret`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });

    const data = await res.json();
    document.getElementById("songResult").innerText =
        `Emotion: ${data.emotion}\nTheme: ${data.theme}\n\n${data.meaning_explanation}`;
}

// POETRY
async function analyzeMeter() {
    const text = document.getElementById("poemInput").value;

    const res = await fetch(`${BASE_URL}/api/meter`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });

    const data = await res.json();
    document.getElementById("meterResult").innerText =
        `Meter: ${data.meter_type}\nConfidence: ${data.confidence}\nRhyme: ${data.rhyme_scheme}`;
}

// SUMMARY
async function summarizeText() {
    const text = document.getElementById("textInput").value;

    const res = await fetch(`${BASE_URL}/api/summarize`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });

    const data = await res.json();
    document.getElementById("summaryResult").innerText = data.summary;
}