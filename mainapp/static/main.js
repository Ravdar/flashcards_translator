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
    console.log("scrolled");

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


// TRANSLATOR PAGE SCRIPTS

// Function to hide and show decks on is_flashcard checkbox

// Function for clearing output_box when input-box is selected


// Displaying and hiding decks selectbox based on checkbox state

var isFlashcardSwitch = document.getElementById("is-flashcard-switch2");
var deckList = document.querySelector(".decks-list");


if (isFlashcardSwitch) {
    isFlashcardSwitch.addEventListener("change", function () {
        if (isFlashcardSwitch.checked) {
            deckList.style.display = "block";
        } else {
            deckList.style.display = "none";
        }
    });
}

// DECKS PAGE SCRIPTS

// Function to show add deck form on button click
function showAddDeckForm() {
    const button = document.getElementById("add-deck-button");
    const addDeckContainer = document.querySelector(".add-deck-container");

    button.addEventListener("click", function () {
        addDeckContainer.style.transform = "translate(-50%, -50%) scale(1)";
    })
}

// Function to hide add deck form on button click
function hideAddDeckForm() {
    const button = document.querySelector(".close-dial");
    const addDeckContainer = document.querySelector(".add-deck-container");

    button.addEventListener("click", function () {
        addDeckContainer.style.transform = " translate(-50%, -50%) scale(0)";
    })
}

// Call the functions to show and hide full streaming info
showAddDeckForm();
hideAddDeckForm();


