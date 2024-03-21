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


// Function to hide and show decks on is_flashcard checkbox

// Function for clearing output_box when input-box is selected


// TRANSLATOR PAGE SCRIPTS

var isFlashcardSwitch = document.getElementById("is-flashcard-switch2");
var deckList = document.querySelector(".decks-list");

// Displaying and hiding decks selectbox based on checkbox state
if (isFlashcardSwitch) {
    isFlashcardSwitch.addEventListener("change", function () {
        if (isFlashcardSwitch.checked) {
            deckList.style.display = "block";
        } else {
            deckList.style.display = "none";
        }
    });
}


