function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith('csrftoken=')) {
            return trimmed.substring('csrftoken='.length);
        }
    }
    return null;
}

function getRecommendations() {
    const genreInput = document.getElementById("genre").value.trim();
    const output = document.getElementById("movie-output");

    if (!genreInput) {
        output.innerHTML = `<p style="color:red;">Please enter a genre.</p>`;
        return;
    }

    fetch("/get_recommendations/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: new URLSearchParams({ genre: genreInput })
    })
    .then(res => res.json())
    .then(data => {
        if (data.movies && data.movies.length > 0) {
            let html = "<h3>Recommended Movies:</h3><ul>";
            data.movies.forEach(movie => {
                const genreTags = movie.genres
                    .split(',')
                    .map(genre => `<span class="genre-tag">${genre.trim()}</span>`)
                    .join(' ');
    
                html += `
                    <li style="margin-bottom: 15px;">
                        <strong>${movie.title}</strong><br/>
                        ${genreTags}
                    </li>`;
            });
            html += "</ul>";
            output.innerHTML = html;
        } else {
            output.innerHTML = "<p>No movies found for that genre.</p>";
        }
    })
    
    .catch(err => {
        output.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    });
}
