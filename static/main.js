// LANDING PAGE SCRIPTS

// Popping up hamburger menu for small screens
const hamburgerButton = document.querySelector(".hamburger-button")
const hamburgerMenu = document.querySelector(".hamburger-menu")

if (hamburgerButton) {
    hamburgerButton.addEventListener("click", function () {
        hamburgerMenu.classList.toggle("active");
    })
}

// Hiding header while scrolling down
var prevScrollpos = window.scrollY;
var header = document.getElementById("header");
if (header) {
    window.onscroll = function () {
        var currentScrollPos = window.scrollY;
        if (prevScrollpos > currentScrollPos) {
            header.style.top = "0";
        } else {
            header.style.top = "-350px";
        }
        prevScrollpos = currentScrollPos;
    }
}

// Displaying answers in faq question on button click
var faqs = document.querySelectorAll(".faq");

faqs.forEach((faq) => {
    faq.addEventListener("click", (event) => {
        const button = event.target.closest(".faq-button");
        faq.classList.toggle("active-faq");
        if (button.textContent === "+") {
            button.textContent = "-";
        } else {
            button.textContent = "+";
        }
    });
});

// Fliping section cards animation on scroll
function flipCard() {
    var cards = document.querySelectorAll(".section-card");

    for (var i = 0; i < cards.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = cards[i].getBoundingClientRect().top;
        var elementVisiblePercentage = 50;
        var elementVisiblePixels = (windowHeight * elementVisiblePercentage) / 100;

        if (elementTop < windowHeight - elementVisiblePixels) {
            (function (index) {
                setTimeout(() => {
                    cards[index].classList.add("rotate");
                }, 750);
            })(i);
        } else {
            cards[i].classList.remove("rotate");
        }
    }
}

window.addEventListener("scroll", flipCard);

flipCard();

// Function for flipping "Instantly." card in hero section

var instantlyCard = document.querySelector(".instantly-card");
var instantlyFront = document.querySelector(".instantly-card-front");
var instantlyBack = document.querySelector(".instantly-card-back");

var frontText = ["Sofort.", "Anında", "तुरंत", "Instantly."];
var backText = ["Al instante.", "すぐに。", "Tout de suite.", "Omedelbart."];

let index = 0;

function flipInstantlyCard() {
    instantlyBack.textContent = backText[index];
    instantlyCard.classList.add("rotate");

    setTimeout(function () {
        instantlyFront.textContent = frontText[index];
        instantlyCard.classList.remove("rotate");
        index = (index + 1) % frontText.length;
    }, 2000);
}

if (instantlyCard) {
    setInterval(flipInstantlyCard, 4000);
}

// DECKS PAGE SCRIPTS

const addDeckButton = document.getElementById("add-deck-button");
var addDeckContainer = document.querySelector(".add-deck-container");
var closeDialButton = document.querySelector(".close-dial");

if (addDeckButton) {
    // Function to show add deck form on button click
    addDeckButton.addEventListener("click", function () {
        addDeckContainer.style.transform = "translate(-50%, -50%) scale(1)";
    })

    // Function to hide add deck form on button click
    closeDialButton.addEventListener("click", function () {
        addDeckContainer.style.transform = " translate(-50%, -50%) scale(0)";
    })
}

// TRANSLATOR AND EDIT FLASHCARD PAGE SCRIPTS

var isFlashcardSwitch = document.getElementById("is-flashcard-switch2");

// Function for clearing output_box when input-box is selected

// Displaying and hiding decks selectbox and changing output box placeholder based on is_flashcard checkbox state

var deckList = document.querySelector(".decks-list");
var outputBox = document.getElementById("output-textarea")

function showOrHideDecksList() {
    var isFlashcardSwitch = document.getElementById("is-flashcard-switch2");
    if (isFlashcardSwitch.checked) {
        deckList.style.display = "flex";
        outputBox.placeholder = "Translated text will appear here. Flashcard will be created automatically."
    } else {
        deckList.style.display = "none";
        outputBox.placeholder = "Translated text will appear here."
    }
}

if (isFlashcardSwitch) {
    isFlashcardSwitch.addEventListener("change", function () { showOrHideDecksList() });
    // Initial run
    showOrHideDecksList();
}


// Showing delete flashcard modal

var deleteButton = document.querySelector(".delete-button");
var deleteModal = document.querySelector(".add-deck-container");
var closeDialButton = document.querySelector(".close-dial");

if (deleteButton) {
    deleteButton.addEventListener("click", function () {
        deleteModal.style.transform = " translate(-50%, -50%) scale(1)";

        // Function to hide add deck form on button click
        closeDialButton.addEventListener("click", function () {
            deleteModal.style.transform = " translate(-50%, -50%) scale(0)";
        })
    })
}


// LOGIN PAGE SCRIPTS


// Log into guest account

var guestAccountButton = document.getElementById("guest-account-button");
var usernameInput = document.getElementById("username-input");
var passwordInput = document.getElementById("password-input");
var loginForm = document.getElementById("login-form");

if (guestAccountButton) {
    guestAccountButton.addEventListener("click", function () {
        usernameInput.value = "Guest";
        passwordInput.value = "ripazhaaezakmi"
        loginForm.submit()
    })
}










