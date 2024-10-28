
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Cambia el título de la pestaña con emojis
        document.title = ' No te vayas, quédate 💔😭!';
    } else {
        // Restaura el título original con otros emojis
        document.title = ' Bienvenido Matricula FIIS 😊!';
    }
});
