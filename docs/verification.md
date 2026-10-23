# 检查记录 / Результаты проверок

2026-10-23（Asia/Shanghai）

代码基于网页提交 `e29723ee8873d2490cff5b97a1543c75afa8b89e`，包含管理员指南 `facdbd4279e01b23ad1e8651664145a26096f317` 和本次文档更新。
Код соответствует коммиту e29723e; включены руководство facdbd4 и текущие изменения документации.

| 检查 / Проверка | 结果 / Результат |
| --- | --- |
| unittest | 18 项通过 / 18 тестов пройдены |
| pytest | 18 passed, 27 subtests passed |
| flake8 E9,F63,F7,F82 | 0 |
| OpenAPI 3.0.3 | OK，3 项操作 / 3 операции |
| JavaScript | `node --check web/app.js`，退出码 0 / код 0 |
| HTTP 补充检查 / Дополнительные HTTP-проверки | 24 次请求通过，JSON 响应按 schema 校验 / 24 запроса успешны, JSON проверен по схемам |
| 设计图 / Схемы | 两张图已打开核对 / Обе схемы открыты и проверены |

```sh
python -B -m unittest discover -s tests -v
python -m pytest -q
python -B -X utf8 tools/check_docs.py
python -m flake8 bookclub tests tools --count --select=E9,F63,F7,F82 --show-source --statistics
openapi-spec-validator api/bookclub.openapi.yaml
node --check web/app.js
```

HTTP 补充检查 / Дополнительные HTTP-проверки:

| 请求与条件 / Запрос и условие | 次数 / Число | 结果 / Результат |
| --- | --- | --- |
| 首页、CSS、JavaScript、health / Страница, CSS, JavaScript, health | 4 | 200 |
| 分页、空列表、非法分页 / Пагинация, пустой список, неверная пагинация | 3 | 200、200、400 |
| 无效令牌、无活动、首次报名、重复报名 / Неверный токен, нет встречи, запись, дубль | 4 | 401、404、201、409 |
| 状态修改：缺少令牌、参与者角色、活动不存在 / Нет токена, роль участника, нет встречи | 3 | 401、403、404 |
| 无效 JSON、数组、空对象、null、数字、未知状态 / Неверный JSON, массив, пустой объект, null, число, неизвестный статус | 6 | 400 |
| 发布、重复发布、结束、结束后取消 / Публикация, повторная публикация, завершение, отмена после завершения | 4 | 200、409、200、409 |

Meeting、Registration、Error 响应按 OpenAPI schema 校验。完整浏览器点击、负载、邮件与数据库端到端检查未执行。
Ответы Meeting, Registration и Error проверены по схемам OpenAPI. Полные проверки кликов в браузере, нагрузки, почты и БД не выполнялись.

文档检查输出 / Вывод проверки документов:

```text
PASS: 35 required files; 80 relative file links; 2 PNG headers
```

[返回目录 / Содержание](../README.md)
