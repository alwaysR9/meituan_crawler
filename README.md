美团爬虫<br>
--------------------------------

介绍<br>
====

按照城市和美食类型，爬取店家主页<br>
该爬虫使用了[webPageCollector](https://github.com/alwaysR9/webPageCollector)，这是一个高效的网页爬取组件<br>

运行<br>
====

python main.py<br>
爬取到的店家主页保存在`data`目录中<br>

说明<br>
====

<b>若希望爬取`北京地区所有火锅店主页`，请按照以下方式修改main.py</b><br>
* 首先 北京地区火锅店的美团链接是：`http://bj.meituan.com/category/huoguo`<br>
* 将main.py中set_city()函数的参数改为`bj`，对应链接中的`bj.meituan.com`<br>
* 将main.py中set_food()函数的参数改为`huoguo`对应链接中的`/category/huoguo`<br>

联系方式<br>
========

zhufangze123@gmail.com<br>
