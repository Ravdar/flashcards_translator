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


// Function to hide and show decks on is_flashcard checkbox

// Function for clearing output_box when input_box is selected


// TRANSLATOR PAGE SCRIPTS

var isFlashcardSwitch = document.getElementById("is-flashcard-switch2");

// Displaying and hiding decks selectbox on toggle switch
if (isFlashcardSwitch) {
    console.log("exists")
    isFlashcardSwitch.addEventListener("click", function () {
        console.log("clicked")
        var deckList = document.querySelector(".decks-list");
        console.log(deckList.style.display)
        // classList.toggle doesn't work for some reason
        if (deckList.style.display === "none") {
            console.log("none");
            deckList.style.display = "block";
        } else if (deckList.style.display === "block") {
            console.log("block");
            deckList.style.display = "none";
        }
    })
}


