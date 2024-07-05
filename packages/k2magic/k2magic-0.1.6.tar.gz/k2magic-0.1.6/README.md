# k2magic
K2Magic是K2assets提供的数据分析开发包（以下简称SDK），用于在本地开发调试K2Assets算法模型，目前提供repo数据抽取功能。

- 本地开发，是指开发者用自己的电脑作为开发环境，例如在笔记本电脑上使用PyCharm编写python代码的场景；
- 在线开发，是指开发者通过浏览器登录到K2Assets环境，在K2Assets提供的网页开发环境里编写python代码的场景。

## K2A模型开发者

### 安装sdk（本地开发）
在本地python开发环境（例如VS Code、PyCharm）里安装sdk：
```
pip install --trusted-host dev.kstonedata.k2 --extra-index-url http://dev.kstonedata.k2:18080/simple/ k2magic
```
注：未来如果k2magic发布到pypi.org则可以简化为`pip install k2magic`。

### 安装sdk（在线开发）
在K2Assets里为指定模型添加sdk依赖项（未来K2Assets会自动为所有模型配置此sdk，届时可省略这个步骤）：

1. 在K2Assets的`知识沉淀`里打开需要使用此sdk的模型详情页面；
2. 在`依赖包` tab页点击右上方`编辑`按钮；
3. 在`第三方`区域添加名为`k2magic`的依赖（不需要指定版本）；
4. 点击右上方`保存`按钮。

在K2Assets里运行模型的时候，需要注意：
1. 要选择v3版本的运行时环境，否则会提示`ng: not found`错误；
2. 只支持从画布上的输入数据源repo里抽取数据，而不是从任意repo里抽取数据。

### 使用sdk

使用方法详见`DataFrameDB`类的docstring，以下是一个快速示例：

```
>>> import pandas as pd
>>> from k2magic.dataframe_db import DataFrameDB
>>> db = DataFrameDB('postgresql+psycopg2://...')
>>> df = db.select('table1', condition='col1 > 1')
>>> df = db.select('table1', limit=3, order_by=['k_device DESC'])
>>> data = {'k_device': ['a', 'b', 'c'], 'col1': [1, 2, 3], 'col2': [4, 5, 6]}
>>> df = pd.DataFrame(data)
>>> db.delete('table1')
>>> db.insert('table1', df)
>>> db.update('table1', df, index_keys=['k_device'])
>>> db.upsert('table1', df, index_keys=['k_device'])
```


## SDK开发者

以下内容面向此SDK的开发者，普通用户不需要了解。

### 打包
在`setup.py`中修改当前版本号，然后用下面的命令将源码打成wheel包：
```
python setup.py clean --all
python setup.py sdist bdist_wheel
```

### 发布
一般发布到k2a环境自带的私有pypi，用户名和密码都为空
```
twine upload --repository-url http://dev.kstonedata.k2:18080/ dist/*
```

### 生成使用文档
```
pydoc -w k2magic\dataframe_db.py
```