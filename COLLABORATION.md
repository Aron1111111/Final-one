# Git 操作 / Работа с Git

```sh
git clone https://github.com/Aron1111111/Final-one.git
cd Final-one
git switch -c docs/update-guide
```

修改与提交 / Изменение и коммит:

```sh
git add docs/user-guide.md
git diff --cached --check
git diff --cached
git commit -m "Update user guide"
git push -u origin docs/update-guide
```

Pull Request 中说明修改内容与检查结果；提交身份使用实际贡献者的账号。
В Pull Request указываются изменения и результаты проверок; коммиты выполняются от аккаунта фактического автора.
