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

        // navbar covers next element a bit, so add padding
        $("body main").css(
            "padding-top",
            String($("header .navbar").outerHeight()) + "px"
        );
    });

    // footer
    $("footer").load("/static/html/footer.html", function() {
        var github_logo = $("#github-logo");
        github_logo.css("height", github_logo.parents(".navbar").innerHeight()/3);

        // similarly, footer covers next element so add bottom padding
        $("body main").css(
            "padding-bottom",
            String($("footer .navbar").outerHeight()) + "px"
        )
    });
});
