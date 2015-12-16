var ARTICLE_ITEM_TEMPLATE = "" +
    "<div>" +
    "<div>" +
    "<div class='ls-article-title'><a class='h3' href='/article/{articleId}/'>{title}</a></div>" +
    "<div>" +
    "<span class='article-property' title='最后修改时间'><i class='article-icon icon-calendar'></i>{modify_time}</span>" +
    "<span class='article-property' title='作者'><i class='article-icon icon-user'></i>{author}</span>" +
    "<span class='article-property' title='标签'><i class='article-icon icon-tags'></i>{tags}</span>" +
    "</div>" +
    "</div>" +
    "<div><p>{summary}</p></div>" +
    "<hr>" +
    "</div>";

var TAG_TEMPLATE = "<a href='/tag/{tag}/' class='tag-index'>{tag}</a>";
var AUTHOR_TEMPLATE = "<a href='' class='author-index'>{author}</a>";

function renderTags(tags) {
    var tagHtml = "";
    for (var i = 0; i < tags.length; i++) {
        tagHtml += TAG_TEMPLATE.replace(/\{tag}/g, tags[i]);
    }
    return tagHtml;
}

function renderAuthors(authors) {
    var authorHtml = "";
    for (var i = 0; i < authors.length; i++) {
        authorHtml += AUTHOR_TEMPLATE.replace(/\{author}/g, authors[i]);
    }
    return authorHtml;
}


function sort(data) {
    var separator = "{#}";
    var ls = [];
    for (var k in data) {
        ls.push(data[k]["modify_time"] + separator + k);
    }
    ls.sort();

    var sortedData = {};
    for (var i = ls.length - 1; i >= 0; i--) {
        var key = ls[i].split(separator)[1];
        sortedData[key] = data[key];
    }
    return sortedData;

}

function renderArticleItem(data) {
    var data = sort(data);
    var articleHtml = "";
    for (var key in data) {

        if (data[key]["title"].length > 0) {

            articleHtml += ARTICLE_ITEM_TEMPLATE.replace(/\{articleId}/g, key)
                .replace(/\{title}/g, data[key]["title"])
                .replace(/\{modify_time}/g, data[key]["modify_time"])
                .replace(/\{author}/g, renderAuthors(data[key]["authors"]))
                .replace(/\{summary}/g, data[key]["summary"])
                .replace(/\{tags}/g, renderTags(data[key]["tags"]));
        }
    }
    $("#article_item").html(articleHtml);
}

$(document).ready(function () {
    var url = "/api/index/article/";
    $.ajax({
        type: "get",
        dateType: "json",
        url: url,
        success: function (data) {
            renderArticleItem(data);
        }
    });
});


