$(document).ready(function() {
    $('#fetch-desktop-history').click(function() {
        const searchTerm = $('#search-input').val().toLowerCase();

        $.getJSON('/get-desktop-env-history', function(data) {
            console.log("Fetched desktop environment history:", data);  // Debug print statement

            if (data.error) {
                $('#desktop-history-output').html(`<p>${data.error}</p>`);
                return;
            }

            let output = "<h3>Recently Used Files:</h3><ul>";
            data
                .filter(item => item.file.toLowerCase().includes(searchTerm))
                .forEach((item, index) => {
                    output += `<li>${index + 1}. ${item.file} | Last Accessed: ${item.last_accessed}</li>`;
                });
            output += "</ul>";

            $('#desktop-history-output').html(output).css("opacity", 1);
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.log("Error fetching data:", textStatus, errorThrown);  // Debug print statement
            $('#desktop-history-output').html("<p>Failed to load Desktop Environment history.</p>");
        });
    });
});
