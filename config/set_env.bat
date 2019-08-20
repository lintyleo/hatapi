@echo off
REM 请进入 当前目录 config 然后运行脚本
REM 运行脚本请使用参数，例如 set_env.bat prod
REM 其他使用 set_env.bat qa   set_env.bat stg 等等
set env_detail=%1
echo [step 1] copy %env_detail% as active environment file
xcopy /R /Y env_%env_detail%.yml env_active.yml