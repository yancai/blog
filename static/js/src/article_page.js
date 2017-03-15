$(document).ready(function () {
    $(".container h1,h2,h3,h4,h5,h6").each(function () {
        var href = $(this).attr("id");
        $(this).prepend('<a class="icon-link" href="#' + href + '" style="visibility: hidden"></a>');
    }).hover(function () {
        $(this).children("a").css("visibility", "visible");
    }, function () {
        $(this).children("a").css("visibility", "hidden");
    });
});
