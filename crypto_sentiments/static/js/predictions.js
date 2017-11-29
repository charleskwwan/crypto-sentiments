// crypto_sentiments/static/js/predictions.js

// capitalize first letter, emulate python's title function
function title(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

// create badge element based on sentiment
function sent_text_elem(sentiment, text) {
    var badge_type = {
        positive: "badge-success",
        negative: "badge-danger",
        neutral: "badge-info",
        up: "badge-success",
        down: "badge-danger"
    };
    return '<span class="badge ' + badge_type[sentiment] + '">' + text + "</span>";
}

$(document).ready(function() {
    // analyze/clear button interactions
    var set_btns_disabled = function(b) {
        $("#analyze-btn").attr("disabled", b);
        $("#clear-btn").attr("disabled", b);
    };

    set_btns_disabled(true);

    $("#tweet-input").keyup(function() {
        set_btns_disabled($(this).val().length == 0);
    });

    $("#analyze-btn").click(function() {
        var results_div = $("#results-div");
        var post_data = JSON.stringify({tweet: $("#tweet-input").val()});

        // if request takes long, client should know request was sent
        results_div.empty();
        results_div.append("<p>Analyzing...</p>");

        // post to server for tweet analysis
        // change results div on return
        $.ajax({
            type: "POST",
            url: "/predict/",
            data: post_data,
            contentType: "application/json",
            success: function(data) {
                results_div.empty();
                results_div.append(
                    '<p class="text-primary">Overall, your tweet has a ' +
                    sent_text_elem(data["sentiment"], data["sentiment"]) +
                    " sentiment.</p>"
                );

                if ("currencies" in data) {
                    var currencies = data["currencies"];
                    for (var c in currencies) {
                        results_div.append(
                            '<p>For ' + c + ", prices should go " +
                            sent_text_elem(currencies[c], currencies[c]) +
                            ".</p>"
                        );
                    }
                }
            }
        });
    });

    $("#clear-btn").click(function() {
        set_btns_disabled(true);
        $("#tweet-input").val("");
        $("#results-div").empty();
        $("#results-div").append('<p>Input a tweet into the textbox on the left and click "Analyze"!</p>');
    });
});
