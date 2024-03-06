$(document).ready(function(){
    var intervalo = 3000;
    var currentIndex = 0;
    var items = $('#meuCarrossel img');
    var totalItems = items.length;

    function mostrarImagem(){
        items.hide();
        items.eq(currentIndex).fadeIn();
    }

    function avancaImagem(){
        mostrarImagem();
        if(currentIndex < totalItems - 1){
            currentIndex++;
        } else {
            currentIndex = 0;
        } mostrarImagem();
    }

    mostrarImagem();

    setInterval(avancaImagem, intervalo);
})