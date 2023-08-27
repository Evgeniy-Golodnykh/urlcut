# YaCut

### Description
This is a URL-shortener service written on Python with Flask framework

### Quick Start
1. Clone repo
```bash
git clone git@github.com:Evgeniy-Golodnykh/yacut.git
```
2. Creates a virtual environment
```python
python3 -m venv venv
```
3. Activates the virtual environment
```python
source venv/bin/activate
```
4. Upgrade PIP and installs the requirements package into the virtual environment
```python
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
5. Configure the .env file like this
```python
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///yacut_db.sqlite3
SECRET_KEY='YOUR_SECRET_KEY'
```
6. To run the application use command
```python
flask run
```

### Technology
[Python](https://www.python.org), [Flask](https://flask.palletsprojects.com), [SQLAlchemy](https://www.sqlalchemy.org)

### Author
[Evgeniy Golodnykh](https://github.com/Evgeniy-Golodnykh)