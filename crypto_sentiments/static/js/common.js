// crypto_sentiments/static/js/common.js
// Common js file for all pages (for things like navbar)

$(document).ready(function() {
    // navbar
    $("header").load("/static/html/navbar.html", function() {
        $("#navbarNav a").each(function() {
            if ($(this).attr("href") === window.location.pathname) {
                $(this).parent().addClass("active");
            }
        });
    });

    // footer
    $("footer").load("/static/html/footer.html");
});
