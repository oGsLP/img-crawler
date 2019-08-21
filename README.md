# img-crawler

## 功能
* **使用img-crawler爬取微博用户的相册图片**
* 交互式命令行运行方式
* 可以键入单个微博用户的ID爬取，也可以将多个爬取目标的别名、用户微博ID、爬取选项单独写入一个txt文件，程序可以读取文件对文件中目标进行陆续爬取
* 爬取间隔、请求间歇，防止过于频繁导致IP被封
* 自定义爬取图片的存放地址
* 对时间解析，命名统一格式，采用"xx-xx-xx_64位md码"。方便排序、归类查找。


## 步骤

* 下载clone项目到本地
* 安装python
* `python crawl_weibo.py` 运行，在命令行中交互
* use preset or not: 是否使用预设(xxx.txt)
* preset_path: 预设的地址，默认为项目根目录的weibo_uid.txt
* weibo_id即用户的微博ID
* object dir：爬取图片存放的根目录


## 预设
> 注: <>代表必须的选项，[]为可选的

* 文本格式文件
* 每行数据为一个待爬取目标，以回车enter换行
* 每行格式：[#] [nickname] <weibo_id> [options]
    * 前缀“#”代表跳过此行不爬取
    * 中间用空格隔开，tab等也行，只要保证在一行且中间有空白即可
    * nickname意味别名，即你为该用户的爬取图片的文件夹命名的名字，若无该选项，则自动采用用户的微博昵称作为名字
    * weibo_id即用户的微博ID
    * options 待加
* 例：
    ```text
    Me 1234567890 
    9876543210
    # 这行不爬 1112223330
    ```
  
## 其他
* 项目借鉴 *[johnnyzhang1992/imageSpider](https://github.com/johnnyzhang1992/imageSpider)*
* 敬请使用，反馈改进