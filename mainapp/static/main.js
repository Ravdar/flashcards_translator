// Popping up hamburger menu for small screens
var hamburgerButton = document.querySelector(".hamburger-button")
var hamburgerMenu = document.querySelector(".hamburger-menu")

hamburgerButton.addEventListener("click", function () {
    hamburgerMenu.classList.toggle("active");
})

// Hiding header while scrolling down
var prevScrollpos = window.scrollY;
var header = document.getElementById("header");
window.onscroll = function () {
    var currentScrollPos = window.scrollY;
    if (prevScrollpos > currentScrollPos) {
        header.style.top = "0";
    } else {
        header.style.top = "-350px";
    }
    prevScrollpos = currentScrollPos;
}

// Displaying answers in faq question on button click
const faqs = document.querySelectorAll(".faq");

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
