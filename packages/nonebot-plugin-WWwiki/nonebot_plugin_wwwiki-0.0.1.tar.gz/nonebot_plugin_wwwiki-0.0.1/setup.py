# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_WWwiki']

package_data = \
{'': ['*'],
 'nonebot_plugin_WWwiki': ['html_template/archives/*',
                           'html_template/echo/*',
                           'html_template/echolink/*',
                           'html_template/enemy/*',
                           'html_template/fonts/*',
                           'html_template/gift/*',
                           'html_template/img/*',
                           'html_template/materialcard/*',
                           'html_template/materialcard/img/*',
                           'html_template/recommendation/*',
                           'html_template/rolecard/*',
                           'html_template/rolecard/img/*',
                           'html_template/skllcard/*',
                           'html_template/skllcard/img/*',
                           'html_template/tale/*',
                           'html_template/weapon/*']}

install_requires = \
['Pilow>=9.4.0',
 'httpx>=0.27.0',
 'jinja2>=3.1.2',
 'nonebot-adapter-onebot>=2.2.3',
 'nonebot2>=2.2.1',
 'pandas>=2.0.3',
 'playwright>=1.33.0',
 'pydantic>=1.10.11']

setup_kwargs = {
    'name': 'nonebot-plugin-wwwiki',
    'version': '0.0.1',
    'description': '发送kurobbs的数据',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n\n</div>\n\n<div align="center">\n<img alt="LOGO" src="https://github.com/shi-yingyingjiang/nonebot-plugin-WWwiki/assets/136897416/6625f119-5186-430c-9f57-3bbfb3105334" width="507" height="174"/> \n</div>\n\n<div align="center">\n\n# nonebot-plugin-WWwiki\n\n_✨ 鸣潮wiki ✨_\n\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-template.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-template">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-template.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n\n</div>\n\n\n## 📖 介绍\n\n鸣潮WIKI，查询鸣潮相关数据\n\n## 💿 安装\n\n<details open>\n<summary>使用 nb-cli 安装</summary>\n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装\n\n    nb plugin install nonebot-plugin-WWwiki\n\n</details>\n\n<details>\n<summary>使用包管理器安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令\n\n<details>\n<summary>pip</summary>\n\n    pip install nonebot-plugin-WWwiki\n</details>\n\n\n打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入\n\n    plugins = ["nonebot_plugin_WWwiki"]\n\n</details>\n\n## 🎉 使用\n### 指令表\n| 指令 | 权限 | 需要@ | 说明 | 示例|\n|:-----:|:----:|:----:|:----:|:----:|\n| 鸣潮角色查询 | 无 | 否 | 查询角色信息 | 鸣潮角色查询 安可 |\n| 鸣潮技能查询 | 无 | 否 | 查询角色技能 | 鸣潮技能查询 安可 |\n| 鸣潮共鸣链查询 | 无 | 否 | 查询角色共鸣链 | 鸣潮共鸣链查询 安可 |\n| 鸣潮角色配队推荐 | 无 | 否 | 查询角色养成推荐 | 鸣潮角色配队推荐 安可 |\n| 鸣潮珍贵之物 | 无 | 否 | 查询珍贵之物 | 鸣潮珍贵之物 安可 |\n| 鸣潮角色档案 | 无 | 否 | 查询角色档案 | 鸣潮角色档案 安可 |\n| 鸣潮角色故事 | 无 | 否 | 查询角色故事 | 鸣潮角色故事 安可 |\n| 鸣潮突破材料 | 无 | 否 | 查询角色突破材料 | 鸣潮突破材料 安可 |\n| 鸣潮武器查询 | 无 | 否 | 查询武器信息 | 鸣潮武器查询 时和岁稔 |\n| 鸣潮声骸查询 | 无 | 否 | 查询声骸信息 | 鸣潮声骸查询 角 |\n| 鸣潮敌人查询 | 无 | 否 | 查询敌人信息 | 鸣潮敌人查询 角 |\n\n\nPS：本人不精通html等的内容的设计，所以成品图效果比较丑，欢迎issue或者pr。\n\n## 注意！ 本项目未在gitcode发布，请注意分别！\n',
    'author': 'shiyingyingjiang',
    'author_email': '2798134864@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shi-yingyingjiang/nonebot-plugin-WWwiki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
