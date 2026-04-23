const BASE_URL = "http://127.0.0.1:5000";

// SONG
async function analyzeSong() {
    const text = document.getElementById("songInput").value;

    document.getElementById("songResult").innerText = "⏳ Analyzing...";
    const res = await fetch(`${BASE_URL}/api/interpret`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });
    

    const data = await res.json();
    document.getElementById("songResult").innerHTML = `
                                    <b>Emotion:</b> ${data.emotion}<br>
                                    <b>Themes:</b> ${data.themes.join(", ")}<br><br>
                                    ${data.meaning_explanation}`;
}

// POETRY
async function analyzeMeter() {
    const text = document.getElementById("poemInput").value;

    document.getElementById("meterResult").innerText = "⏳ Analyzing...";

    const res = await fetch(`${BASE_URL}/api/meter`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });
    
    const data = await res.json();
    document.getElementById("meterResult").innerHTML = `
            <b>Meter:</b> ${data.meter_type}<br>
            <b>Confidence:</b> ${data.confidence}<br>
            <b>Rhyme Scheme:</b> ${data.rhyme_scheme}<br><br>
            ${data.explanation}
            `;
}

// SUMMARY
async function summarizeText() {
    const text = document.getElementById("textInput").value;

    document.getElementById("summaryResult").innerText = "⏳ Analyzing...";
    const res = await fetch(`${BASE_URL}/api/summarize`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });
    

    const data = await res.json();
document.getElementById("summaryResult").innerHTML = `
${data.summary}
`;
}