INSTRUCTION TO RUN CODE ON YOUR LOCAL

1. OPEN FILE IN YOUR VSCODE
2. INSTALL PYTHON IF YOU DON'T HAVE PYTHON IN YOUR OS(can use python 3.11).
3. CREATE VIRTUAL ENVIROMENT : python3.11 -m venv envname
4. activate virtual enviroment : source envname/bin/activate
5. pip install requirement.txt
6. runserver : ./manage.py runserver
7. go to this link : http://127.0.0.1:8000/myapp/surahs/
8. 3 things to play around : Complete Quran Editions, List of Surahs, Quran Pages

DATABASE

1. ./manage.py makemigrations
2. ./manage.py migrate