var ARTICLE_ITEM_TEMPLATE = "" +
    "<div>" +
    "<div>" +
    "<span><a class='h3 ls-article-title' href='/pages/articles/{articleId}.html'>{title}</a></span>" +
    "<div>" +
    "<span class='article-property' title='最后修改时间'><i class='article-icon icon-calendar'></i>{modify_time}</span>" +
    "<span class='article-property' title='作者'><i class='article-icon icon-user'></i>{author}</span>" +
    "<span class='article-property' title='标签'><i class='article-icon icon-tags'></i>{tags}</span>" +
    "</div>" +
    "</div>" +
    "<div><p>{summary}</p></div>" +
    "<hr>" +
    "</div>";

var TAG_TEMPLATE = "<a href='/pages/tags/{tag}.html' class='tag-index'>{tag}</a>";
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
    var count = 0;
    for (var key in data) {

        if (data[key]["title"].length > 0) {

            articleHtml += ARTICLE_ITEM_TEMPLATE.replace(/\{articleId}/g, key)
                .replace(/\{title}/g, data[key]["title"])
                .replace(/\{modify_time}/g, data[key]["modify_time"])
                .replace(/\{author}/g, renderAuthors(data[key]["authors"]))
                .replace(/\{summary}/g, data[key]["summary"])
                .replace(/\{tags}/g, renderTags(data[key]["tags"]));
            count++;
        }
    }
    $("#article_item").html(articleHtml);
    $("#count").text(count + " 篇");
}

function get_articles_by_tag(tag) {
    var tag = $("#tag").text();

    $.ajax({
        type: "get",
        dateType: "json",
        url: "/data/tags.json",
        success: function (data) {

        }
    })
}

function get_articles() {
    $.ajax({
        type: "get",
        dateType: "json",
        url: "/data/tags.json",
        success: function (data) {

        }
    })
}

$(document).ready(function () {
    let tag = $("#tag").text();

    $.ajax({
        type: "get",
        dateType: "json",
        url: "/data/articles.json",
    }).then(function (article_map) {
        $.ajax({
            type: "get",
            dateType: "json",
            url: "/data/tags.json",
            success: function (data) {
                let articles = data[tag];
                let articles_info = {};
                articles.forEach(function (value, i) {
                    articles_info[value] = article_map[value]
                });
                renderArticleItem(articles_info)
            }
        });
    });

});
