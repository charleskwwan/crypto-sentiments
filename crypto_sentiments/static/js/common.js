// crypto_sentiments/static/js/common.js
// Common js file for all pages (for things like navbar)

$(document).ready(function() {
    // menu
    $("#navbar-container").load("/static/html/navbar.html", function() {
        $("#navbarNav a").each(function() {
            if ($(this).attr("href") === window.location.pathname) {
                $(this).parent().addClass("active");
            }
        });
    });
});
