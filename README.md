# 图书俱乐部 / Книжный клуб

图书俱乐部项目：活动查看与报名、活动描述校验、组织者状态管理。
Проект книжного клуба: просмотр встреч, запись, проверка описания и управление статусами организатором.

| 内容 / Материалы | 文件 / Файлы |
| --- | --- |
| 需求 / Требования | [基本需求](docs/requirements.md)、[描述与状态规则](docs/review-requirements.md) |
| 设计图 / Схемы | [架构与报名流程](docs/architecture.md) |
| 接口说明 / API | [OpenAPI YAML](api/bookclub.openapi.yaml) |
| 代码 / Код | [描述校验](bookclub/description_validator.py)、[状态转换](bookclub/status_transitions.py)、[异常类型](bookclub/errors.py) |
| 测试 / Тесты | [业务测试设计](docs/testing.md)、[描述测试](tests/test_description_validator.py)、[状态测试](tests/test_status_transitions.py)、[异常测试](tests/test_errors.py)、[检查结果](docs/verification.md) |
| 指南 / Руководства | [用户流程](docs/user-guide.md)、[仓库管理](docs/admin-guide.md) |
| 审查 / Ревью | [审查清单](docs/review-checklist.md) |
| 来源 / Источники | [材料来源](SOURCES.md) |
| 课程报告 / Отчёт | [REPORT.md](REPORT.md) |

## 测试 / Тесты

```sh
python -B -m unittest discover -s tests -v
python -B -X utf8 tools/check_docs.py
```

```sh
python -m pytest -q
```

## 本地网页 / Локальная веб-версия

本地演示站点使用 Python 标准库运行，提供活动列表、参与者报名和组织者状态修改。数据保存在内存中，服务重启后恢复示例数据。
Локальная демонстрация работает на стандартной библиотеке Python: список встреч, запись участника и изменение статуса организатором. Данные хранятся в памяти и сбрасываются после перезапуска.

```sh
python -m bookclub.web_app
```

浏览器打开 http://127.0.0.1:8000 。演示身份令牌由页面自动使用：`member-demo` 和 `organizer-demo`。
Откройте http://127.0.0.1:8000 . Страница использует демонстрационные токены `member-demo` и `organizer-demo`.
