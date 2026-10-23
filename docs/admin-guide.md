# 仓库管理 / Управление репозиторием

## 文件检查 / Проверка файлов

```sh
python -B -X utf8 tools/check_docs.py
git diff --check
```

文档使用相对链接，图像保存在 docs/images。移动文件时同步修改引用。
Документы используют относительные ссылки; изображения хранятся в docs/images. При переносе файла обновляются ссылки.

## 代码检查 / Проверка кода

```sh
python -B -m unittest discover -s tests -v
```

修改前查看 git status 和 git diff，提交时选择本次修改的文件。
Перед изменениями проверяются git status и git diff; в коммит включаются файлы текущей правки.

## 保存与恢复 / Сохранение и восстановление

文件保存规则见 [STORAGE_POLICY.md](../STORAGE_POLICY.md)，协作命令见 [COLLABORATION.md](../COLLABORATION.md)。
Правила хранения приведены в [STORAGE_POLICY.md](../STORAGE_POLICY.md), команды совместной работы — в [COLLABORATION.md](../COLLABORATION.md).

恢复前保存当前修改的补丁或副本，再从指定提交恢复文件。共享提交的撤销使用 git revert。
Перед восстановлением сохраняется патч или копия текущих изменений; затем файл восстанавливается из выбранного коммита. Общий коммит отменяется через git revert.

[返回目录 / Содержание](../README.md)
