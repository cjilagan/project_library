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

function switchTab(id) {
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      document.getElementById(id).classList.add('active');
    }

    function filterBooks() {
      const query = document.getElementById("searchBooks").value.toLowerCase();
      document.querySelectorAll("#bookTable tr").forEach(row => {
        const title = row.children[0].textContent.toLowerCase();
        const author = row.children[1].textContent.toLowerCase();
        row.style.display = title.includes(query) || author.includes(query) ? "" : "none";
      });
    }

    function filterUsers() {
      const query = document.getElementById("searchUsers").value.toLowerCase();
      document.querySelectorAll("#userTable tr").forEach(row => {
        const email = row.children[0].textContent.toLowerCase();
        const role = row.children[1].textContent.toLowerCase();
        row.style.display = email.includes(query) || role.includes(query) ? "" : "none";
      });
    }

    function saveChanges(button) {
      const row = button.closest("tr");
      const title = row.children[0].textContent.trim();
      const author = row.children[1].textContent.trim();
      console.log("Save book:", title, author);
      // TODO: AJAX POST to Flask endpoint
    }

    function saveUser(button) {
      const row = button.closest("tr");
      const email = row.children[0].textContent.trim();
      const role = row.children[1].textContent.trim();
      console.log("Update user:", email, role);
      // TODO: AJAX POST to Flask endpoint
    }

    function approveRequest(button) {
      const row = button.closest("tr");
      const user = row.children[0].textContent.trim();
      const book = row.children[1].textContent.trim();
      console.log("Approved request:", user, book);
      row.children[2].textContent = "Approved";
    }

    function denyRequest(button) {
      const row = button.closest("tr");
      const user = row.children[0].textContent.trim();
      const book = row.children[1].textContent.trim();
      console.log("Denied request:", user, book);
      row.children[2].textContent = "Denied";}

  setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message) => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 500); 
    });
}, 5000);
