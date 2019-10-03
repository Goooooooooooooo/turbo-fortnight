
Git Memo
==========

git 初始化，会生成隐藏文件.git
```Bash
git init
git remote add origin [url]
git add .
git commit -m "init project"
git push -u origin master
```
获取最新代码
```Bash
git fetch origin master
```
合并
```Bash
git merge origin/master
```

查看远程主机网址
```Bash
git remote -v
origin  git@github.com:test/test.git (fetch)
origin  git@github.com:test/test.git (push)
```

关联远程仓库
```Bash
git remote add origin https://github.com/test/test.git
```

同步远程仓库和本地仓库
```Bash
git pull origin master
```
			
新建一个md格式的markdown > 文件
```Bash
touch README.md
```

从现有URL获取仓库 ，下载项目及其整个版本历史记录
```Bash
git clone [url]
```

列出所有改动状态
```Bash
git status
```

版本比较
```Bash
git diff --staged
```

文件取消版本控制
```Bash
git reset [file]
```

列出分支
```Bash
git branch
```

创建新分支
```Bash
git branch [branch-name]
```

切换到指定的分支并更新工作目录
```Bash
git checkout [branch-name]
```

将指定分支的历史记录合并到当前分支中
```Bash
git merge [branch]
```

删除指定的分支
```Bash
git branch -d [branch-name]
```

显示两个分支之间的内容差异
```Bash
git diff [first-branch]...[second-branch]
```

在[commit]之后撤消所有提交，在本地保留更改
```Bash
git reset [commit]
```

丢弃所有历史记录并更改回指定的提交
```Bash
git reset --hard [commit]
```

强制覆盖远程分支
```Bash
git push origin master --force
```
