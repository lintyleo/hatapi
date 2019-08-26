@echo off

python context.py

echo [step 0] - initialize report parameters
set reruns=3
set test_target=..\case\seniverse\test_weather_now.py
set allure_target=..\report\allure\target\
set allure_report=c:\xampp\htdocs\allureport\liutingli\

echo [step 1] - remove all documents in allure report root
REM del /a /f /q %allure_report%

echo [step 2] - starting pytest
pytest %test_target% --reruns %reruns% --alluredir=%allure_target%

echo [step 3] - finished pytest and starting generate allure report
call allure generate -c %allure_target% -o %allure_report%

echo [step 4] - open allure report by jetty

REM call allure open %allure_report%

echo [step 5] - report has been generated successfully!

