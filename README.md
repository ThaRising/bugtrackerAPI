# Bugtracker API

API for the "OrcTracker" Bugtracker Project.  
Requires Python 3.6+.  
Tested on Python 3.7.3 and 3.6.5 on Windows 10 1903 and Ubuntu 18.04.

## How to use

Clone this repository:  
````git clone "https://www.github.com/ThaRising/bugtrackerApi.git````  

Install dependencies:
```cmd
conda env update --file environment.yml
pip install -r requirements.txt
```  

Create database (use Python console):
```python
from application import create_app, db
with create_app().app_context():
    db.create_all()
```  

Start the Flask application:

```cmd
python app.py
```

Note: due to problems with werkzeug it may be necessary to manually rename
imports in the flask_restplus module:  
````from werkzeug import cached_property````  
````from werkzeug.utils import cached_property````.