# IR-system
信息检索课程项目

创建索引

创建索引

```shell
curl -X DELETE "localhost:9200/docs?pretty"
curl -X PUT "localhost:9200/docs?pretty" -H 'Content-Type: application/json' --data-binary "@index-config.json"
curl -H "Content-Type: application/json" -XPOST "localhost:9200/docs/_bulk?pretty&refresh" --data-binary "@test.json"
```

测试分析器：

```shell
curl -X POST "localhost:9200/docs/_analyze?pretty" -H 'Content-Type: application/json' -d'                           
{
  "analyzer": "pos",
  "text": "我_v n 人民"
}
'
```

