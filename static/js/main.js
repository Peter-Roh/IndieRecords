function openBar() {
    // used in mobile screen menu bar
    window.onload = function() {
        const elt = document.getElementById("bar-icon");
        const target = document.getElementById("mobile__bar");
        elt.onclick = function() {
            target.classList.toggle("hidden");
        };
    };
}
