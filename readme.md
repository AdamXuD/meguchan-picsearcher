# meguchan-picsearch

> 惠酱的搜图后端服务

## 具有功能

接受图片链接，向 [saucenao](http://saucenao.com/)，[ascii2d](https://ascii2d.net/)，[iqdb](https://iqdb.org)，[tracemoe](https://trace.moe/)请求搜图结果，整理成一定的格式。能将请求到的结果在数据库中缓存一段时间，返回特征码，可以使用该特征码向后端获取搜索结果。或是直接获取搜索结果。

配合 [meguchan-frontend](https://github.com/AdamXuD/meguchan-frontend) 使用更佳。

## 部署方式

### 一般方式（建议 Python >= 3.9.2）

```shell
python main.py
```

### `docker`部署

1. 打包镜像

```shell
docker build -t meguchan-picsearcher .
```

2. 部署镜像
   > 其中 `/code/data`文件夹为后端数据文件夹，3000 端口为默认暴露端口。
   >

```shell
docker run -d --name meguchan-picsearcher -p 3000:3000 -v /code/data:/code/data meguchan-picsearcher
```

## 配置文件

> 服务通过 `.env `文件或系统环境变量实现配置的传递。其中系统环境变量优先级高于 `.env`文件，配置如下。

```plaintext
ENVIRONMENT="dev"
#分为prod和dev dev环境会暴露文档

HOST="0.0.0.0"
# 服务地址

PORT=3000
# 服务端口

DB_PATH="./data/data.db"
# sqlite3数据库存储目录

ASCII2D_PROXY
# ascii2d代理地址，形如https://example.com，为空则不需要代理

IQDB_PROXY
# iqdb代理地址，形如https://example.com，为空则不需要代理

SAUCENAO_PROXY
# saucenao代理地址，形如https://example.com，为空则不需要代理

TRACEMOE_PROXY
# tracemoe代理地址，形如https://example.com，为空则不需要代理

QUERY_TIMEOUT=5
# （请求第三方搜图服务）请求时限，超时则自动断开连接并返回空列表

RESULT_TTL=86400
# 结果缓存时限

SECRET
# 请求鉴权字符串，防止api被盗用，若为空则不对搜图请求做鉴权

```

## API

### `GET` /search

#### 接受参数

| 键        | 类型    | 是否必要  | 描述                                                                                             |
| --------- | ------- | --------- | ------------------------------------------------------------------------------------------------ |
| url       | `str` | `true`  | 图片 URL                                                                                         |
| engine    | `str` | `false` | 指定搜图引擎（`ascii2d`，`saucenao`，`iqdb`，`tracemoe`，`all`），默认为 `ascii2d`。 |
| data_type | `str` | `false` | 指定结果类型（`web`，`json`），默认为 `web`                                                |
| secret    | `str` | `false` | 鉴权 `secret`                                                                                  |

#### 返回结果

`data_type == json`

```json
{
  "success": true,			# 是否成功
  "msg": "string", 			# 搜索失败提示
  "data": {
    "pic_url": "string", 		# 搜索源图片
    "hint": "string", 			# 搜索过程错误提示
    "results": [
      {
        "engine": "ascii2d", 		# 本结果提供方
        "thumbnail": "string", 		# 结果缩略图
        "title": "string",		# 结果标题
        "similarity": "string",		# 结果相似度
        "relative_url": ["string"], 	# 相关链接
        "other_info": "string"		# 其他信息
      }
    ]
  }
}
```

`data_type == web`

```json
{
  "success": true,
  "msg": "",
  "data": {
    "key": "l8tEgK"
  }
}
```

### `GET` /result

#### 接收参数

| 键  | 类型    | 是否必要 | 描述           |
| --- | ------- | -------- | -------------- |
| key | `str` | `true` | 搜索结果特征码 |

#### 返回结果

```json
{
  "success": true,			# 是否成功
  "msg": "string", 			# 搜索失败提示
  "data": {
    "pic_url": "string", 		# 搜索源图片
    "hint": "string", 			# 搜索过程错误提示
    "results": [
      {
        "engine": "ascii2d", 		# 本结果提供方
        "thumbnail": "string", 		# 结果缩略图
        "title": "string",		# 结果标题
        "similarity": "string",		# 结果相似度
        "relative_url": ["string"], 	# 相关链接
        "other_info": "string"		# 其他信息
      }
    ]
  }
}
```
