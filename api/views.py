#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""

import os
from generate import INPUT_CONTENT, generate
from utils.helper import IndexData
from flask import Blueprint, jsonify, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

api = Blueprint(
    "index", __name__
)


@api.route("/index/article/")
def get_all_article_index():
    """获取所有文章索引信息
    """
    return jsonify(IndexData.get_index_data().get("article_index"))


@api.route("/index/inv_tag/")
def get_tag_index():
    """获取标签的倒排索引
    """
    return jsonify(IndexData.get_index_data().get("tag_inverted_index"))


@api.route("/index/inv_author/")
def get_author_index():
    """获取作者的倒排索引
    """
    return jsonify(IndexData.get_index_data().get("author_inverted_index"))


@api.route("/index/reload/")
def reload_index():
    """重新加载索引
    """
    try:
        IndexData.reload_index_data()
        return jsonify({
            "msg": "ok"
        })
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({
            "msg": "failed"
        })


@api.route("/index/generate/")
def generate_index():
    """生成索引信息
    """
    try:
        generate()
        IndexData.reload_index_data()
        return jsonify({
            "msg": "ok"
        })
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({
            "msg": "failed"
        })


@api.route("/index/tag/<tag>/")
def get_article_by_tag(tag):
    """获取指定标签的索引信息
    """
    aids = IndexData.get_index_data().get("tag_inverted_index").get(tag)
    articles = {i: IndexData.get_index_data().get("article_index")[i] for i in aids}
    return jsonify(articles)


@api.route("/file/upload", methods=["POST"])
def upload_article():
    """上传文件
    1. 保存至本地
    2. md转换为html
    3. 重新加载索引信息
    """
    f = request.files["md_file"]
    f_name = secure_filename(f.filename)
    f.save(os.path.join(INPUT_CONTENT, f_name))
    generate()
    IndexData.reload_index_data()
    return redirect(url_for("page_articles"))


if __name__ == "__main__":
    pass
