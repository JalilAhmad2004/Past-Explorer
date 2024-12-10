$(document).ready(function() {
    $('#fetch-history').click(function() {
        let searchTerm = $('#search-input').val();  // Get the search term from the input field
        $.get('/get-shell-history', { search: searchTerm }, function(data) {
            let output = '<h3>Bash Command History:</h3><pre>';
            data.bash.forEach((command, index) => {
                output += (index + 1) + ': ' + command + '\n';  // Number each command
            });
            output += '</pre><h3>Zsh Command History:</h3><pre>';
            data.zsh.forEach((command, index) => {
                output += (index + 1) + ': ' + command + '\n';  // Number each command
            });
            output += '</pre>';
            $('#history-output').html(output).fadeIn();  // Fades in the output
        });
    });
});
