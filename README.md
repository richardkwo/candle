![candle](http://img3.douban.com/view/photo/photo/public/p2152409025.jpg)

## 豆瓣阅读推送到Kindle

这个项目包括两部分，浏览器扩展和服务器端

### 启动服务

* 执行`git clone git@github.com:wong2/candle.git`得到这份代码
* 确保已安装`redis`且已启动`redis-server`
* 下载[kindlegen](http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211)并将其加入PATH中，确保在终端可以执行`kindlegen`命令
* 进入`candle`目录，执行`[sudo] pip install -r requirements.txt`安装Python依赖
* 编辑`config.py`，填入你的邮箱服务的配置
* 执行`rqworker`开启worker
* 执行`python app.py`开启Flask的开发服务器
* 此时服务应该已经跑在`http://localhost:5000/send`了
* 然后你可以考虑把服务跑在Nginx等服务器上，比如搭配[Gunicorn](http://gunicorn.org/)
