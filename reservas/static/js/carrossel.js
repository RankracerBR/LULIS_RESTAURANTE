document.addEventListener("DOMContentLoaded", function () {
    var carousel = document.getElementById("meuCarrossel");
    var images = carousel.getElementsByTagName("img");
    
    var currentImageIndex = 0;
    var interval = setInterval(nextImage, 3000);

    function nextImage() {
        images[currentImageIndex].style.display = "none";
        currentImageIndex = (currentImageIndex + 1) % images.length;
        images[currentImageIndex].style.display = "block";
    }
    
    carousel.addEventListener("mouseenter", function () {
        clearInterval(interval);
    });
    
    carousel.addEventListener("mouseleave", function () {
        interval = setInterval(nextImage, 2300);
    });
});
