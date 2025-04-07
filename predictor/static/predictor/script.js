function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith('csrftoken=')) {
            cookieValue = trimmed.substring('csrftoken='.length);
            break;
        }
    }
    return cookieValue;
}

function analyzeText() {
    const prompt = document.getElementById('prompt').value.trim();
    const outputDiv = document.getElementById('output');
    const loader = document.getElementById('loader');

    if (!prompt) {
        outputDiv.innerHTML = `<p style="color: red;">Please enter some text to analyze.</p>`;
        return;
    }

    loader.style.display = 'block';
    outputDiv.innerHTML = ''; // Clear previous

    fetch('/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: new URLSearchParams({
            'prompt': prompt
        })
    })
    .then(response => {
        loader.style.display = 'none';
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    })
    .then(data => {
        let genreTags = '';
        if (data.recommended_genres && data.recommended_genres.length > 0) {
            genreTags = `
                <p><strong>Recommended Genres:</strong> 
                    ${data.recommended_genres.map(genre => `<span class="genre-tag">${genre}</span>`).join(' ')}
                </p>`;
        }
    
        outputDiv.innerHTML = `
            <p><strong>Message:</strong> ${data.message}</p>
            <p><strong>Mental Health Risk:</strong> ${data.mental_health_risk}</p>
            <p><strong>Conditions Flagged:</strong> ${data.conditions_flagged.join(", ")}</p>
            <p><strong>Emotion:</strong> ${data.emotion}</p>
            ${genreTags}
        `;
        outputDiv.scrollIntoView({ behavior: "smooth" });
    })
    
    .catch(error => {
        loader.style.display = 'none';
        outputDiv.innerHTML = `<p style="color:red;">Error processing the request.<br>${error}</p>`;
    });
}
