var TAG_TEMPLATE = "<dt><a href='/tag/{tag}/'>{tag}</a></dt><dd>{count}<dd>";

function renderTags(data){
    var tagsHtml = "";
    for (var key in data) {
        tagsHtml += TAG_TEMPLATE.replace(/\{tag}/g, key)
            .replace(/\{count}/g, data[key].length);
    }
    $("#tags").html(tagsHtml);
}

$(document).ready(function() {
    var url = "/api/index/inv_tag/";
    $.ajax({
        type: "get",
        dateType: "json",
        url: url,
        success: function(data) {
            renderTags(data);
        }
    });
});


