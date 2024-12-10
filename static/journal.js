$(document).ready(function() {
    $('#fetch-logs').click(function() {
        $.get('/get-journalctl-entry', function(data) {
            let output = '<h3>Latest User Logs:</h3>';
            if (data.error) {
                output += `<p>Error: ${data.error}</p>`;
            } else if (data.logs && data.logs.length > 0) {
                data.logs.forEach(function(log, index) {
                    output += `<p><strong>${index + 1}.</strong> ${log}</p>`;
                });
            } else {
                output += '<p>No logs found.</p>';
            }
            $('#journal-logs').html(output);
        });
    });
});

