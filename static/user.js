$(document).ready(function() {
    // Hide the history output initially
    $('#history-output').hide();

    // Fetch logs when the "Show Logs" button is clicked
    $('#show-logs-button').click(function() {
        var searchTerm = $('#search-input').val().toLowerCase(); // Get the search term from the input field
        fetchUserSessionLogs(searchTerm); // Fetch logs based on the search term (if any)
        $('#history-output').fadeIn(); // Fade in the logs section when the button is pressed
    });

    // Fetch logs based on search input when the search button is clicked
    $('#search-button').click(function() {
        var searchTerm = $('#search-input').val().toLowerCase(); // Get the search term from the input field
        fetchUserSessionLogs(searchTerm); // Fetch logs based on the search term
        $('#history-output').fadeIn(); // Fade in the logs section when the button is pressed
    });

    // Fetch logs from the server and filter them based on the search term
    function fetchUserSessionLogs(searchTerm) {
        $.get('/get-user-session-logs', function(data) {
            if (data.logs && data.logs.length > 0) {
                // Filter out empty logs and apply search filter if needed
                var filteredLogs = data.logs.filter(function(log) {
                    return log.trim() !== '' && log.toLowerCase().includes(searchTerm);
                });

                // Display logs with numbering or show a no-result message
                if (filteredLogs.length > 0) {
                    var numberedLogs = filteredLogs.map(function(log, index) {
                        return `<p><strong>${index + 1}.</strong> ${log}</p>`;
                    });
                    $('#history-output').html(numberedLogs.join('')).fadeIn(); // Reveal numbered logs
                } else {
                    $('#history-output').text('No logs found matching your search term.').fadeIn(); // No matching logs
                }
            } else {
                $('#history-output').text('No user session logs found.').fadeIn(); // No logs available
            }
        });
    }
});

