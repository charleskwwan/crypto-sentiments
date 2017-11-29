// crypto_sentiments/static/js/index.js

$(document).ready(function() {
    // set onclick listeners for each currency button
    var currency_text = $(this).find("#currency-text");
    var predict_text = $(this).find(".predict-text");

    $(this).find("#currency-btns label").each(function() {
        $(this).click(function() {
            var c = $(this).children("input").attr("id").replace("-btn", "");

            // request price direction for currency from server
            $.get("/pricedir/" + c, function(data) {
                currency_text.text(c);
                predict_text.attr("id", "predict-" + data["direction"]);
                if (data["direction"] === "up") {
                    predict_text.text("UP ▴");
                } else if (data["direction"] == "down") {
                    predict_text.text("DOWN ▾");
                }
            });
        });
    });

    // github logo (inline) height
    var github_logo = $("#github-logo-inline");
    github_logo.css("height", github_logo.parents("p").css("line-height"));
});
