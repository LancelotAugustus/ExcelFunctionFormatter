# Excel公式格式化/美化

## 代码参考

[https://github.com/AntoniotheFuture/ExcelFormulaBeautifier](https://github.com/AntoniotheFuture/ExcelFormulaBeautifier)
[https://github.com/joshbtn/excelFormulaUtilitiesJS](https://github.com/joshbtn/excelFormulaUtilitiesJS)

## 1.excelFormulaUtilitiesJS

### 项目地址

[https://github.com/joshbtn/excelFormulaUtilitiesJS](https://github.com/joshbtn/excelFormulaUtilitiesJS)

### 适用场景

- 在文档或页面中美化展示复杂 Excel 公式，提高可读性与可维护性。
- 对公式进行静态分析（例如提取依赖、做安全审查、做批量重写）。

### 实现逻辑

- 基于词法分析与简单语法转换：先把 Excel 公式分解为 token，再根据语法规则重排/着色或转为目标语言表达式。
- 项目脚本和测试表明核心实现位于 src/core.js 与 src/ExcelFormulaUtilities.js。

### 注意事项

- 覆盖度可能不包含所有最新 Excel 特性（如动态数组、LET、LAMBDA、XLOOKUP 等）；复杂引用或区域运算可能需要额外适配。

### 核心代码解释

#### 词法解析

[https://github.com/joshbtn/excelFormulaUtilitiesJS/blob/main/src/core.js](https://github.com/joshbtn/excelFormulaUtilitiesJS/blob/main/src/core.js)

#### 公式美化

[https://github.com/joshbtn/excelFormulaUtilitiesJS/blob/main/src/ExcelFormulaUtilities.js](https://github.com/joshbtn/excelFormulaUtilitiesJS/blob/main/src/ExcelFormulaUtilities.js)

## Excel公式大全

### 1.中文参考

[https://support.microsoft.com/zh-cn/office/excel-%E5%87%BD%E6%95%B0-%E6%8C%89%E5%AD%97%E6%AF%8D%E9%A1%BA%E5%BA%8F-b3944572-255d-4efb-bb96-c6d90033e188](https://support.microsoft.com/zh-cn/office/excel-%E5%87%BD%E6%95%B0-%E6%8C%89%E5%AD%97%E6%AF%8D%E9%A1%BA%E5%BA%8F-b3944572-255d-4efb-bb96-c6d90033e188)

### 2.英文参考

[https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188](https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188)

