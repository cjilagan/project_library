document.addEventListener("DOMContentLoaded", function () {
    const loginButton = document.querySelector(".login-form button");
    const emailInput = document.querySelector(".login-form input[type='text']");
    const passwordInput = document.querySelector(".login-form input[type='password']");
    const signupLink = document.querySelector(".signup-text");

    loginButton.addEventListener("click", function () {
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if (email === "" || password === "") {
            alert("Please enter both email/username and password.");
        } else {
            alert("Login successful! (This is just a simulation.)");
        }
    });

    signupLink.addEventListener("click", function (event) {
        event.preventDefault();
        alert("Redirecting to signup page...");
    });
    
    document.body.style.backgroundSize = "cover";
    document.body.style.backgroundAttachment = "fixed";
});

document.addEventListener("DOMContentLoaded", function() {
    const passwordInput = document.getElementById('password');
    const secretKeyInput = document.getElementById('admin_secret_key');

    // Toggle password visibility
    passwordInput.addEventListener('focus', function() {
        this.type = 'text';
    });

    passwordInput.addEventListener('blur', function() {
        this.type = 'password';
    });

    // Toggle secret key visibility
    secretKeyInput.addEventListener('focus', function() {
        this.type = 'text';
    });

    secretKeyInput.addEventListener('blur', function() {
        this.type = 'password';
    });
});