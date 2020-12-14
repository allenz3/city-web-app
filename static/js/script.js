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
