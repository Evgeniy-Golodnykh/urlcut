# URLCut

### Description
This is a URL-shortener service written on Python with Flask framework

### Quick Start
1. Clone repo
```bash
git clone git@github.com:Evgeniy-Golodnykh/urlcut.git
```
2. Creates a virtual environment
```bash
python3 -m venv venv
```
3. Activates the virtual environment
```bash
source venv/bin/activate
```
4. Upgrade PIP and installs the requirements package into the virtual environment
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
5. Configure the .env file like this
```bash
FLASK_APP=urlcut
DATABASE_URI=sqlite:///urlcut_db.sqlite3
SECRET_KEY='YOUR_SECRET_KEY'
```
6. To run the application use command
```bash
flask run
```

### API
```bash
# Endpoint to retrieve the original URL
Method: GET
Endpoint: "{your_local_host}:5000/api/id/{custom_id}/"

# Endpoint to create a short link
Method: POST
Endpoint: "{your_local_host}:5000/api/id/"
Request: {
    "url": "string",         # required
    "custom_id": "string"    # not required
}
```

### Technology
[Python](https://www.python.org), [Flask](https://flask.palletsprojects.com), [SQLAlchemy](https://www.sqlalchemy.org)

### Author
[Evgeniy Golodnykh](https://github.com/Evgeniy-Golodnykh)
