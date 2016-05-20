#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""

from flask import Flask, render_template

from api.views import api

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@app.route("/favicon.ico")
def get_favicon():
    """favicon.ico
    """
    return app.send_static_file("favicon.ico")


@app.route("/")
def page_index():
    """页面-首页
    """
    return render_template("index.html")


@app.route("/about")
def page_about():
    """页面-关于
    """
    return app.send_static_file("out/About.html")


@app.route("/article/<aid>/")
def page_article(aid):
    """页面-获取指定id的文章
    """
    return app.send_static_file("out/{}.html".format(aid))


@app.route("/articles/")
def page_articles():
    """页面-全部文章列表
    """
    return render_template("articles.html")


@app.route("/tags/")
def page_tags():
    """页面-全部标签
    """
    return render_template("tags.html")


@app.route("/tag/<tag>/")
def page_article_by_tag(tag):
    """页面-指定标签的文章列表
    """
    return render_template("articles_by_tag.html", tag=tag)


@app.route("/upload/")
def page_upload():
    return render_template("upload.html")

# 注册api接口的blueprint
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
    pass
