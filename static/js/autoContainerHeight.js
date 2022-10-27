window.onload = window.onresize = function autoContainerHeight() {
    var container = document.getElementById("main-container");

    var navbar_height = document.getElementById("navigation").offsetHeight;
    var container_height = container.offsetHeight;
    var footer_height = document.getElementById("footer").offsetHeight;
    var window_height = window.innerHeight;

    if (navbar_height + container_height + footer_height <= window_height) {
        container.style.height = (window_height - navbar_height - footer_height) + "px";
    } else {
        container.style.height = null;
    }
}