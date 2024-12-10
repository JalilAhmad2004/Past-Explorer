document.getElementById('fetch-history').addEventListener('click', function() {
    const searchTerm = document.getElementById('search').value; // Get search term
    const historyResultsDiv = document.getElementById('history-results');
    historyResultsDiv.innerHTML = 'Loading history...'; // Show loading message

    fetch(`/get-browser-history?search=${searchTerm}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        historyResultsDiv.innerHTML = ''; // Clear previous results

        // Check for Firefox History
        if (data.firefox && data.firefox.length > 0) {
            const firefoxHistory = document.createElement('div');
            firefoxHistory.innerHTML = `<h3>Firefox History:</h3>`;
            data.firefox.forEach((item, index) => {
                const div = document.createElement('div');
                div.innerHTML = `<strong>${index + 1}. ${item.title || 'No Title'}</strong><br>URL: <a href="${item.url}" target="_blank">${item.url}</a><br>Last Visited: ${item.visit_time}<hr>`;
                firefoxHistory.appendChild(div);
            });
            historyResultsDiv.appendChild(firefoxHistory);
        }

        // Check for Chrome History
        if (data.chrome && data.chrome.length > 0) {
            const chromeHistory = document.createElement('div');
            chromeHistory.innerHTML = `<h3>Chrome History:</h3>`;
            data.chrome.forEach((item, index) => {
                const div = document.createElement('div');
                div.innerHTML = `<strong>${index + 1}. ${item.title || 'No Title'}</strong><br>URL: <a href="${item.url}" target="_blank">${item.url}</a><br>Last Visited: ${item.visit_time}<hr>`;
                chromeHistory.appendChild(div);
            });
            historyResultsDiv.appendChild(chromeHistory);
        }

        // If no data found
        if (data.firefox.length === 0 && data.chrome.length === 0) {
            historyResultsDiv.innerHTML = 'No history found.';
        }
    })
    .catch(error => {
        console.error('Error fetching browser history:', error);
        historyResultsDiv.innerHTML = 'An error occurred while fetching history.';
    });
});

