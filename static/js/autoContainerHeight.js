let navbar = document.getElementById("navigation");
let container = document.getElementById("main-container");
let footer = document.getElementById("footer");

window.onload = window.onresize = container.ontransitionend = function() {
    container.style.height = null;

    if (container.offsetHeight < window.innerHeight - navbar.offsetHeight - footer.offsetHeight) {
        container.style.height = (window.innerHeight - navbar.offsetHeight - footer.offsetHeight) + "px";
    }
}
