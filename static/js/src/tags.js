var TAG_TEMPLATE = "<dt><a href='/pages/tags/{tag}.html'>{tag}</a></dt><dd>{count}<dd>";

function renderTags(data) {
    var tagsHtml = "";
    for (var key in data) {
        tagsHtml += TAG_TEMPLATE.replace(/\{tag}/g, key)
            .replace(/\{count}/g, data[key].length);
    }
    $("#tags").html(tagsHtml);
}

$(document).ready(function () {
    var url = "/data/tags.json";
    $.ajax({
        type: "get",
        dateType: "json",
        url: url,
        success: function (data) {
            renderTags(data);
        }
    });
});


