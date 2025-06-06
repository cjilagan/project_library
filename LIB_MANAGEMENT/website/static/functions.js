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


  setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message) => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 500); 
    });
}, 5000);

const popLogout = () => {
  document.querySelector('.container-logout').style.display = 'block';
  document.querySelector('.container-logout1').style.display = 'block';
  document.querySelector('.container-logout2').style.display = 'block';
  document.querySelector('.container-logout3').style.display = 'block';
  document.querySelector('.container-logout4').style.display = 'block';
};

const popMemberLogout = () => {

}

const popCancelLogout = () => {
  document.querySelector('.container-logout').style.display = 'none';
  document.querySelector('.container-logout1').style.display = 'none';
  document.querySelector('.container-logout2').style.display = 'none';
  document.querySelector('.container-logout3').style.display = 'none';
  document.querySelector('.container-logout4').style.display = 'none';
};

const popUser = () => {
  document.querySelector('.container1').style.display = 'none';
  document.querySelector('.container2').style.display = 'none';
  document.querySelector('.container3').style.display = 'none';
  document.querySelector('.container5').style.display = 'block';
};

const popBooks = () => {
  document.querySelector('.container1').style.display = 'block';
  document.querySelector('.container2').style.display = 'none';
  document.querySelector('.container3').style.display = 'none';
  document.querySelector('.container5').style.display = 'none';
};

const popBorrowReq = () => {
  document.querySelector('.container1').style.display = 'none';
  document.querySelector('.container2').style.display = 'none';
  document.querySelector('.container3').style.display = 'block';
  document.querySelector('.container5').style.display = 'none';
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelector('.container1').style.display = 'block';
  document.querySelector('.container2').style.display = 'none';
  document.querySelector('.container3').style.display = 'none';
  document.querySelector('.container5').style.display = 'none';
});

function toggleAddBookForm() {
  const form = document.getElementById('addBookForm');
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function showManageUsers() {
  document.querySelector('.container5').style.display = 'none';
  document.querySelector('.container2').style.display = 'block';
}

function backToUsers() {
  document.querySelector('.container2').style.display = 'none';
  document.querySelector('.container5').style.display = 'block';
}

function showManageBooks(){
  document.querySelector('.container1').style.display = 'none';
  document.querySelector('.container6').style.display = 'block';
}

function backToBooks() {
  document.querySelector('.container1').style.display = 'block';
  document.querySelector('.container6').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
  const searchSections = [
      {inputSelector: '.search-bar input', tableSelector: '.table tbody'},
      {inputSelector: '.search-bar4 input', tableSelector: '.table4 tbody'},
      {inputSelector: '.search-bar1 input', tableSelector: '.table1 tbody'},
      {inputSelector: '.search-bar3 input', tableSelector: '.table3 tbody'},
      {inputSelector: '.search-bar2 input', tableSelector: '.table2 tbody'},
      {inputSelector: '.search-bar-member input', tableSelector: '.table-member tbody'}
  ];

  searchSections.forEach(section => {
      const searchInput = document.querySelector(section.inputSelector);
      const tableBody = document.querySelector(section.tableSelector);

      if (searchInput && tableBody) {
          const tableRows = Array.from(tableBody.querySelectorAll('tr')).filter(row => row.id !== 'no-results');
          const noResultsRow = tableBody.querySelector('#no-results');

          searchInput.addEventListener('input', function() {
              const searchTerm = searchInput.value.toLowerCase();
              let anyVisible = false;

              tableRows.forEach(row => {
                  const cells = Array.from(row.children);
                  const match = cells.some(cell => cell.textContent.toLowerCase().includes(searchTerm));

                  if (match) {
                      row.style.display = '';
                      anyVisible = true;
                      cells.forEach(cell => highlightText(cell, searchTerm));
                  } else {
                      row.style.display = 'none';
                  }
              });

              if (searchTerm === '') {
                  tableRows.forEach(row => {
                      row.children.forEach(cell => removeHighlight(cell));
                  });
              }

              if (noResultsRow) {
                  if (anyVisible) {
                      noResultsRow.classList.remove('show');
                      setTimeout(() => noResultsRow.style.display = 'none', 300);
                  } else {
                      const message = noResultsRow.getAttribute('data-message') || 'No results found.';
                      noResultsRow.querySelector('td').textContent = message;
                      noResultsRow.style.display = 'table-row';
                      setTimeout(() => noResultsRow.classList.add('show'), 10);
                  }
              }
          });
      }
  });

  function highlightText(cell, term) {
      const text = cell.textContent;
      const regex = new RegExp(`(${term})`, 'gi');
      const highlighted = text.replace(regex, '<mark>$1</mark>');
      cell.innerHTML = highlighted;
  }

  function removeHighlight(cell) {
      cell.innerHTML = cell.textContent;
  }
});

if (anyVisible) {
  noResultsRow.classList.remove('show');
  setTimeout(() => noResultsRow.style.display = 'none', 300);
} else {
  const message = noResultsRow.getAttribute('data-message') || 'No results found.';
  noResultsRow.querySelector('td').textContent = message;
  noResultsRow.style.display = 'table-row';
  setTimeout(() => noResultsRow.classList.add('show'), 10);
}

//Initialize Swiper
const swiper = new Swiper('.slider-wrapper', {
  loop: true,
  spaceBetween: 25,

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
    dynamicBullets: true,
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  
  // Responsive breakpoints
  breakpoints: {
    0: {
      slidesPerView: 1
    }
},
});
