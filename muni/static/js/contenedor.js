function CargarContenido(contenedor, contenido) {
    // Cargar el contenido en el contenedor
    $("." + contenedor).load(contenido, function () {
        // Activar el elemento del menú correspondiente al contenido cargado
        var url = contenido.split('/').pop(); // Obtener el nombre del archivo de la URL
        
    });
}
// PARA ACTIVAR LOS MENUS
document.addEventListener("DOMContentLoaded", function() {
    const sidebarItems = document.querySelectorAll(".sidebar-item");
    // Agrega la clase 'active' al elemento de la página de inicio por defecto
    document.querySelector(".sidebar-item a[href='/dash']").closest("li").classList.add("active");
    sidebarItems.forEach(item => {
        item.addEventListener("click", function() {
            // Elimina la clase 'active' solo de los elementos de la barra lateral que no han sido clickeados
            sidebarItems.forEach(item => {
                if (item !== this) {
                    item.classList.remove("active");
                }
            });
            // Agrega la clase 'active' al elemento clickeado
            this.classList.add("active");
        });
    });
});