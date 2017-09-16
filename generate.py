#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""

import shutil
import os
import codecs
import shelve
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
import pypinyin

BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)

# 静态文件路径，默认为`/static/`
# 表示使用flask发布网站时的`http://ip:port/static/`目录
# 也可指定为固定地址的静态文件url，例如："http://192.168.62.47:5000/static/"
# 注意，使用其他域名的静态文件时有可能引起跨域问题
STATIC_ROOT = "/static/"




# Markdown文件读取目录
INPUT_CONTENT = os.path.join(BASE_DIR, 'in')

# 索引文件
INDEX_DAT = os.path.join(BASE_DIR, "static", "out", "index.dat")

# html生成输出目录
OUTPUT_CONTENT = os.path.join(BASE_DIR, "static","out")
env = Environment(
    loader=FileSystemLoader("templates")
)


# 标签倒排索引
TAG_INVERTED_INDEX = {}
# 作者倒排索引
AUTHOR_INVERTED_INDEX = {}

# 文章索引
ARTICLE_INDEX = {}

_MD_FILES = []

_current_file_index = None
_pinyin_names = set()

TAG_HTML_TEMPLATE = u"<a href='/tag/{tag}/' class='tag-index'>{tag}</a>"
AUTHOR_HTML_TEMPLATE = u"<a href='' class='tag-index'>{author}</a>"
TITLE_HTML_TEMPLATE = u"<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>标题</h5><p>{title_str}</p></div>"


def _reload_global():
    global TAG_INVERTED_INDEX, AUTHOR_INVERTED_INDEX, ARTICLE_INDEX,\
        _MD_FILES, _current_file_index, _pinyin_names

    TAG_INVERTED_INDEX = {}
    AUTHOR_INVERTED_INDEX = {}
    ARTICLE_INDEX = {}
    _MD_FILES = []
    _current_file_index = None
    _pinyin_names = set()


def clean():
    """清理输出文件夹
    """
    if os.path.exists(OUTPUT_CONTENT):
        shutil.rmtree(OUTPUT_CONTENT)


def parse_time(timestamp, pattern="%Y-%m-%d %H:%M:%S"):
    """解析时间
    """
    return datetime.fromtimestamp(timestamp).strftime(pattern)


def str2pinyin(hans, style=pypinyin.FIRST_LETTER):
    """字符串转拼音，默认只获取首字母
    """
    pinyin_str = pypinyin.slug(hans, style=style, separator="")
    num = 2
    while pinyin_str in _pinyin_names:
        pinyin_str += str(num)
        num += 1
    return pinyin_str


def dump_index():
    """持久化索引信息
    """
    dat = shelve.open(INDEX_DAT)
    dat["article_index"] = ARTICLE_INDEX
    dat["tag_inverted_index"] = TAG_INVERTED_INDEX
    dat["author_inverted_index"] = AUTHOR_INVERTED_INDEX
    dat.close()


def index_tags(tags, fid):
    """为标签倒排索引添加标签
    """
    for tag in tags:
        if tag in TAG_INVERTED_INDEX:
            TAG_INVERTED_INDEX[tag].append(fid)
        else:
            TAG_INVERTED_INDEX[tag] = [fid]


def index_authors(authors, fid):
    """为作者倒排索引添加作者
    """
    for author in authors:
        if author in AUTHOR_INVERTED_INDEX:
            AUTHOR_INVERTED_INDEX[author].append(fid)
        else:
            AUTHOR_INVERTED_INDEX[author] = [fid]


def create_index(filename, meta):
    """创建索引信息
    :param filename: 文件从INPUT_CONTENT开始的全路径
    :param meta:
    :type meta: dict
    :return:
    """

    # filename = codecs.decode(filename, "utf-8")

    index_tags(meta.get("tags", []), _current_file_index)
    index_authors(meta.get("authors", []), _current_file_index)

    title = meta.get("title", [""])[0]
    if title == "":
        title = os.path.splitext(os.path.basename(filename))[0]

    publish_dates = meta.get("publish_date", [])
    if len(publish_dates) == 0:
        publish_date = parse_time(os.path.getctime(filename), "%Y-%m-%d")
    else:
        publish_date = publish_dates[0]

    ARTICLE_INDEX[_current_file_index] = {
        "filename": filename,
        "modify_time": parse_time(os.path.getmtime(filename)),
        "title": title,
        "summary": meta.get("summary", [u""])[0],
        "authors": meta.get("authors", [u"匿名"]),
        "publish_date": publish_date,
        "tags": meta.get("tags", [])
    }


def get_out_dir(md_file):
    """获取md文件的输出路径
    :param md_file:
    :return:
    """
    return os.path.join(OUTPUT_CONTENT, _current_file_index + ".html")


def save_html(out_path, html):
    """保存html至文件
    :param out_path:
    :param html:
    :return:
    """
    base_folder = os.path.dirname(out_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    with codecs.open(out_path, "w+", "utf-8") as f:
        f.write(html)


def render_tags_html(tags):
    """渲染tags的html
    """
    tags_html = ""
    for tag in tags:
        tags_html += TAG_HTML_TEMPLATE.format(tag=tag)
    return tags_html


def render_authors_html(authors):
    """渲染作者html
    """
    authors_html = ""
    for author in authors:
        authors_html += AUTHOR_HTML_TEMPLATE.format(author=author)
    return authors_html


def render_title_html(title):
    """渲染标题html
    """
    title_html = ""
    if title.strip() != "":
        title_html = TITLE_HTML_TEMPLATE.format(title_str=title)
    return title_html


def render(md_file):
    """渲染html页面
    :param md_file:
    :return:
    """
    with codecs.open(md_file, "r", "utf-8") as f:
        text = f.read()
        md = Markdown(
            extensions=[
                "fenced_code",
                "codehilite(css_class=highlight,linenums=None)",
                "meta",
                "admonition",
                "tables",
                "toc",
                "wikilinks",
            ],
        )
        html = md.convert(text)
        meta = md.Meta if hasattr(md, "Meta") else {}
        toc = md.toc if hasattr(md, "toc") else ""
        create_index(md_file, meta)
        template = env.get_template("base_article.html")
        text = template.render(
            blog_content=html,
            static_root=STATIC_ROOT,
            title=ARTICLE_INDEX[_current_file_index].get("title"),
            title_html=render_title_html(ARTICLE_INDEX[_current_file_index].get("title")),
            summary=ARTICLE_INDEX[_current_file_index].get("summary", ""),
            authors=render_authors_html(ARTICLE_INDEX[_current_file_index].get("authors")),
            tags=render_tags_html(ARTICLE_INDEX[_current_file_index].get("tags")),
            toc=toc,
        )

    return text


def gen(md_file_path):
    """将markdown生成html文件
    :param md_file_path:
    """
    out_path = get_out_dir(md_file_path)
    html = render(md_file_path)
    save_html(out_path, html)


def scan_md():
    """扫描md文件
    """
    global _current_file_index
    for f in _MD_FILES:
        file_base_name = os.path.splitext(os.path.basename(f))[0]
        _current_file_index = str2pinyin(
            file_base_name
        )
        _pinyin_names.add(_current_file_index)
        gen(f)


def load_md_files(folder):
    """从指定文件夹载入Markdown文件
    """
    global _MD_FILES
    for root, dirs, files in os.walk(folder):
        for f in files:
            if os.path.splitext(f)[1].lower() == ".md":
                _MD_FILES.append(os.path.join(root, f))


def generate():
    _reload_global()
    clean()

    load_md_files(INPUT_CONTENT)
    scan_md()
    dump_index()
    pass


if __name__ == "__main__":
    generate()
    pass
