$(document).ready(function() {
    $('#fetch-vim-history').click(function() {
        const searchTerm = $('#search-input').val().toLowerCase();

        $.getJSON('/get-vim-history', function(data) {
            if (data.error) {
                $('#vim-history-output').html(`<p>${data.error}</p>`);
                return;
            }

            let output = "<h3>Recently Opened Files:</h3><ul>";
            data.file_history
                .filter(file => file.toLowerCase().includes(searchTerm))
                .forEach((file, index) => {
                    output += `<li>${index + 1}. ${file}</li>`;
                });
            output += "</ul><h3>Command History:</h3><ul>";
            data.command_history
                .filter(command => command.toLowerCase().includes(searchTerm))
                .forEach((command, index) => {
                    output += `<li>${index + 1}. ${command}</li>`;
                });
            output += "</ul>";

            $('#vim-history-output').html(output).css("opacity", 1);
        }).fail(function() {
            $('#vim-history-output').html("<p>Failed to load Vim history.</p>");
        });
    });
});
