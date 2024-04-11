@echo off

git init
git remote add origin https://github.com/Kabir1240/PomodoroTimer.git
git branch -m master main
git pull origin main
git add .
git commit -m "initial commit"
git push -u origin main
