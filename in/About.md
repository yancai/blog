summary: 介绍本博客的基本功能
authors: 蔡岩
publish_date: 2015-12-15
tags: 简介
      Markdown

# 关于本文

本博客是本人（Yan）开发的一个基于Markdown的博客系统，支持基本的Markdown语法及一些常用的扩展语法。本文将对本博客所支持的Markdown语法做介绍。

# Markdown基本语法

Markdown基本语法参见：  
[https://daringfireball.net/projects/markdown/syntax](https://daringfireball.net/projects/markdown/syntax)

# 扩展的Markdown特殊语法

本博客Markdown的生成基于Python的Markdown包，因此本博客支持的扩展语法也源于Python Markdown，参见：[Python Markdown](https://pythonhosted.org/Markdown/)

## META信息的编写方式

META支持作者为Markdown文件添加自定义的一些信息，这些自定义的信息将在页面右侧展示和查看是起作用，目前支持如下信息：

| 关键字       | 含义         |
|:-------------|:-------------|
| title        | 文章标题     |
| summary      | 摘要         |
| author       | 作者         |
| publish_date | 文章发布日期 |
| tags         | 标签         |

**注意：**  

 1. 如果`authors`、`tags`有多个时，请换行书写；
 2. meta信息之间不要有空行；
 3. 全部meta结尾和正文之间至少保留一个空行；
 4. meta信息请使用小写，并使用英文冒号`:`；
 5. title如果为填写，则使用Markdown文件名作为标题；


例如，本文的Meta信息如下：

    title: 简介
    summary: 介绍本博客的基本功能
    authors: 蔡岩
    publish_date: 2015-12-15
    tags: 简介
          Markdown


## table表格支持

本博客支持table语法，方便大家使用表格展示数据，基本语法如下：

Markdown语法示例：  

    | 默认列 | 左对齐列 | 右对齐列 | 居中列 |
    |:----|:----|----:|:----:|
    | 早上好 | 中午好 | 下午好 | 晚上好 |


显示如下：  

| 默认列 | 左对齐列 | 右对齐列 | 居中列 |
|:-------|:---------|---------:|:------:|
| 早上好 | 中午好   |   下午好 | 晚上好 |
