# 检查记录 / Результаты проверок

2026-10-23

| 检查 / Проверка | 结果 / Результат |
| --- | --- |
| unittest 单元测试 / Модульные тесты unittest | 12 项通过 / 12 пройдены |
| pytest 单元测试 / Модульные тесты pytest | 12 passed, 27 subtests passed |
| Python 语法与未定义名称 / Синтаксис и неопределённые имена | flake8：0 |
| 文档文件、相对链接、图像文件头 / Файлы, ссылки, заголовки изображений | 29 required files; 56 relative file links; 2 PNG headers, PASS |
| OpenAPI 3.0.3 规范 / Спецификация OpenAPI 3.0.3 | OK，3 项操作 / 3 операции |
| 来源核对 / Сверка с источниками | 7 个代码与测试文件、2 张图与来源一致 / 7 файлов кода и тестов, 2 изображения совпадают с источниками |

```sh
python -B -m unittest discover -s tests -v
python -m pytest -q
python -B -X utf8 tools/check_docs.py
flake8 bookclub tests tools --count --select=E9,F63,F7,F82 --show-source --statistics
openapi-spec-validator api/bookclub.openapi.yaml
```

[返回目录 / Содержание](../README.md)
