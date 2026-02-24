# 执行路径

## step_0

缓存所有读取过的html

## step_1

找到所有excel函数及其对应的详细信息网址(拒绝多语言，专注英文)

- **数据源**:
  [https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188](https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188)

## step_2

在每一个详细信息网址中找到函数接受的值以及返回的值

- name
- type
- desc
- uuid
- syntax
- applies

* [Done] 先生成包含name、type、desc、url四个字段的ExcelFunction实例

* 然后然后依据name解析url，得到syntax，和applies
* 最后得到完整的dataclass

# 待办

* 后续可以考虑添加最后更新时间的相关逻辑

| 标签                                                       | 内容             | 含义     |
|----------------------------------------------------------|----------------|--------|
| `<meta content="2014-05-20" name="firstPublishedDate"/>` | 2014-05-20     | 首次发布日期 |
| `<meta content="2025-12-12" name="lastPublishedDate"/>`  | **2025-12-12** | 最后发布日期 |

* 考虑将.json文件迁移至data目录
* 考虑新增日志结构
* 数据变动时的差异显示结构
* 测试结构