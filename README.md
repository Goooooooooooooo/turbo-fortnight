# turo-fortnight 

Git Memo

git init						# git 初始化，会生成隐藏文件.git
git remote add origin [url]
git add .
git commit -m "init project"
git push -u origin master


git fetch origin master			# 获取最新代码
git merge origin/master			# 合并


git remote -v					# 查看远程主机网址
origin  git@github.com:test/test.git (fetch)
origin  git@github.com:test/test.git (push)

git remote add origin https://github.com/test/test.git		# 关联远程仓库

git pull origin master			# 同步远程仓库和本地仓库


touch README.md					# 新建一个md格式的markdown > 文件

git clone [url]					# 从现有URL获取仓库 ，下载项目及其整个版本历史记录

git status						# 列出所有改动状态

git diff --staged				# 版本比较

git reset [file]				# 文件取消版本控制

git branch						# 列出分支

git branch [branch-name]		# 创建新分支

git checkout [branch-name]		# 切换到指定的分支并更新工作目录

git merge [branch]				# 将指定分支的历史记录合并到当前分支中

git branch -d [branch-name]		# 删除指定的分支

git diff [first-branch]...[second-branch]	# 显示两个分支之间的内容差异

git reset [commit]				# 在[commit]之后撤消所有提交，在本地保留更改

git reset --hard [commit]		# 丢弃所有历史记录并更改回指定的提交