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
                                    <div class="analysis-item">
                                        <span class="label">Emotion</span>
                                        <span class="value">${data.emotion}</span>
                                    </div>

                                    <div class="analysis-item">
                                        <span class="label">Themes</span>
                                        <span class="value">${data.themes.join(", ")}</span>
                                    </div>

                                    <div class="explanation-box">
                                        ${data.meaning_explanation}
                                    </div>`;
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
                                                <div class="analysis-item">
                                                    <span class="label">Meter</span>
                                                    <span class="value">${data.meter_type}</span>
                                                </div>

                                                <div class="analysis-item">
                                                    <span class="label">Confidence</span>
                                                    <span class="badge ${data.confidence.toLowerCase()}">
                                                        ${data.confidence}
                                                    </span>
                                                </div>

                                                <div class="analysis-item">
                                                    <span class="label">Rhyme Scheme</span>
                                                    <span class="value">${data.rhyme_scheme}</span>
                                                </div>

                                                <div class="explanation-box">
                                                    ${data.explanation}
                                                </div>
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
                                        <div class="summary-title">
                                            AI Generated Summary
                                        </div>
                                        <div class="analysis-item">
                                            <span class="label">Original Length</span>
                                            <span class="value">${text.length} chars</span>
                                        </div>

                                        <div class="analysis-item">
                                            <span class="label">Summary Length</span>
                                            <span class="value">${data.summary.length} chars</span>
                                        </div>

                                        <div class="explanation-box">
                                            ${data.summary}
                                        </div>
`;
}