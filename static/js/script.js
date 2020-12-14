document.querySelectorAll('.accordion__button').forEach(button => {
    button.addEventListener('click', () => {
        // const accordionContent = button.nextElementSibling;
        button.classList.toggle('accordion__button--active');
        // if(button.classList.contains('accordion_button--active')) {
        //     accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
        // } else {
        //     accordionContent.style.maxHeight = 0;
        // }
    });
});

var i = 0;
var images = []
var time = 3000;

// Image List


// Change Image
function changeImg() {
    document.slide.src = images[i]

    if(i < images.length - 1) {
        i++
    } else {
        i = 0;
    }

    setTimeout("changeImg()", time);
}

window.onload = changeImg