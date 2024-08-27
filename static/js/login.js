$(document).ready(function() {
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();

        const username = $('#username').val();
        const password = $('#password').val();

        $.ajax({
            url: '/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(data) {
                if (data.message) {
                    $('#message').text(data.message).css('color', 'green');
                    // Redirect to a dashboard or home page after successful login
                    setTimeout(() => {
                        window.location.href = '/dashboard';  // Change this to your desired redirect URL
                    }, 1500);
                } else if (data.error) {
                    $('#message').text(data.error).css('color', 'red');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                $('#message').text('An error occurred. Please try again.').css('color', 'red');
            }
        });
    });
});