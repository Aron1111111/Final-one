# 图书俱乐部 / Книжный клуб

图书俱乐部项目：活动查看与报名设计、活动描述校验、组织者状态管理。
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

## 测试 / Тесты

```sh
python -B -m unittest discover -s tests -v
python -B -X utf8 tools/check_docs.py
```

```sh
python -m pytest -q
```
