@echo off
Title "Start Project"
cmd /k "cd Env\Scripts & activate & cd ..\..\ & py manage.py runserver localhost:8000"