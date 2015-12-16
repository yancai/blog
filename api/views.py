#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""
import logging

from utils.helper import IndexData
from flask import Blueprint, jsonify

api = Blueprint(
    "index", __name__
)

log = logging.getLogger(__name__)


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
    IndexData.reload_index_data()
    return jsonify({
        "msg": "ok"
    })


@api.route("/index/tag/<tag>/")
def get_article_by_tag(tag):
    """获取指定标签的索引信息
    """
    aids = IndexData.get_index_data().get("tag_inverted_index").get(tag)
    articles = {i: IndexData.get_index_data().get("article_index")[i] for i in aids}
    return jsonify(articles)


if __name__ == "__main__":
    pass
