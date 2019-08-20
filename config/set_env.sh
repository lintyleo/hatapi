#!/bin/bash
# 请进入 当前目录 config 然后运行脚本
# 运行脚本请使用参数，例如 sh set_env.sh prod
# 其他使用 sh set_env.sh qa   sh set_env.sh stg 等等
# shellcheck disable=SC2034
env_detail=$1
# shellcheck disable=SC2154
echo "[step 1] copy $env_detal as active environment file"
xcopy /R /Y "env_$env_detal.yml" env_active.yml