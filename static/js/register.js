document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const messageDiv = document.getElementById('message');

    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        if (password !== confirmPassword) {
            messageDiv.textContent = "Passwords do not match";
            messageDiv.style.color = 'red';
            return;
        }

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                messageDiv.textContent = data.message;
                messageDiv.style.color = 'green';
                // Redirect to login page after successful registration
                setTimeout(() => {
                    window.location.href = '/login';
                }, 1500);
            } else if (data.error) {
                messageDiv.textContent = data.error;
                messageDiv.style.color = 'red';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            messageDiv.textContent = 'An error occurred. Please try again.';
            messageDiv.style.color = 'red';
        });
    });
});