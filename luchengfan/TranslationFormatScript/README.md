# translate.py
参数：

|参数|作用|默认值|参考值|
|:-:|---|:-:|:-:|
|-h|打印帮助文档|无|无
|-m/--mode|选择模式1为将项目的strings资源转为excel文档。2为将excel文档转为strings.xml|1|1,2|
|-i/--input|输入文件，mode1下为项目路径，mode2下为excel文件路径|必填|项目路径或excel路径|
|-o/--output|输出路径，mode1下为excel文件名，mode2下为输出文件夹名|项目名|项目或文件夹名
|-a/--app|指定app目录|app|项目下app的目录名|

##### 实例

``` bash
//将TvSettings中的所以strings资源转入excel文件
python translate.py -m 1 -i ./TvSettings  //输出为TvSettings:app.xls
//将TvSettings.xls转为android资源文件
python translate.py -m 2 -i TvSettings:app.xls //输出为TvSettings文件夹
python translate.py -m 1 -i ./Multimedia3 -a media_browser //输出为Multimedia3:media_browser.xls
```

# batch_translate.py

参数：

|参数|作用|默认值|参考值|
|:-:|---|:-:|:-:|
|-h|打印帮助文档|无|无|
|-m/--mode|选择转换模式，1：读取config文件，将其中的项目资源文件转换成xls文件。2:将xls文件转换为多个项目的资源文件|1|1,2|
|-c/--config|指定config文件路径|./config.txt|config文件路径|
|-i/--input|仅在mode2下有用，指定excel文件路径。|必填|

返回值：0:正常结束  1:异常终止

# config文件编写格式

``` bash
# 这是注释行
# 指定TvSettings
/Users/leviming/Develop/TvSettings:app
# TvProvision
/Users/leviming/Develop/TvProvision:app
# Settings
/Users/leviming/Develop/Settings

# 多app目录
/Users/leviming/Develop/Multimedia3:media_browser
/Users/leviming/Develop/Multimedia3:media_players
/Users/leviming/Develop/Multimedia3:media_common_library
```

# blacklist.py

`blacklist.py`顾名思义，是用于过滤文件夹的，由于在部分项目中可能出现非字符串资源文件夹下也含有`strings.xml`的情况，可以将这些文件夹加入到文件中，在解析时就不会去遍历这些文件夹。

``` python
BLACK_LIST = [
	'values',		# 由于values目录下的strings.xml需要单独处理，因此也可以在这里忽略掉,代码中也做了对该文件的过滤机制
	'需要忽略的文件夹',
	...
]
```
-
# 查询翻译资源

在根目录下新增了三个文件 `generate_dict.py`，`findTranslate.py`，`srclist.py`以及两个文件夹`translations`与`libs`。

#### findTranslate.py

如果需要查询翻译可以直接通过`python findTranslate.py`运行脚本，之后直接输入内容即可查找对应翻译，具体操作可参见程序的help信息。

运行方式：

``` shell
python findTranslate.py 	// 以默认方式启动
python findTranslate.py -l /path/to/libs //指定翻译资源的所在，翻译资源见后文解释
python findTranslate.py -h		//打印帮助信息
```

#### generate_dict.py

可用于自己生成翻译资源库（一般情况不需要单独运行）。运行前需先修改`blacklist.py`，将`values`删除，然后编辑`srclist.py`，在其中添加需要导出翻译资源的项目（包含values/strings.xml即可，不需要是Android项目）。对应的翻译资源会以json资源的行使存储在`translations`文件夹下，`translations`下已有的翻译资源不会被覆盖，只会追加不同的内容，但若key相同则不会重复添加。

运行方式：

``` shell
python generate_dict.py
```

#### 翻译资源

默认存储在`./translations`目录下的json文件，文件名与Android系统的多语言文件夹名称相同。每一个文件对应了一种语言的翻译。