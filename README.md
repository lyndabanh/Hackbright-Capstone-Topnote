# TOPNOTE
Topnote is a full-stack web application for wine enthusiasts that allows users to discover their wine personality as they browse, favorite, and rate wines. It analyzes user favorited wines to make recommend similar wines that the user may like.  

## Contents
* [Technologies & Stack](#techstack)
* [Set-up & Installation](#configuration)
* [Features](#features)
* [About the Developer](#about)

##  <a name="techstack"></a> Technologies and Stack
**Backend:**
Python, JavaScript, Flask, Jinja, SQLAlchemy, PostgreSQL <br>
**Frontend:**
Bootstrap, Google Fonts, HTML5, CSS3 <br>
**API:**
Chart.js <br>
**Dataset:**
Wine Ratings (Kaggle)

## <a name="configuration"></a> Set-up & Installation
Install a code editor such as [VS code](https://code.visualstudio.com/download) or [Sublime Text](https://www.sublimetext.com/).<br>
Install [Python3](https://www.python.org/downloads/mac-osx/)<br>
Install [pip](https://pip.pypa.io/en/stable/installing/), the package installer for Python <br>
Install [postgreSQL](https://www.postgresql.org/) for the relational database.<br>

Clone or fork repository:
```bash
$ git clone https://github.com/lyndabanh/Hackbright-Capstone-Topnote.git
```
Create and activate a virtual environment inside the mybooksheldirectory:
```bash
$ virtualenv env
$ source env/bin/activate
```

Install dependencies:
```bash
$ pip3 install -r requirements.txt
```

With PostgreSQL, create the mybookshelf database:
```bash
$ createdb mycellar
```

Create all tables and relations in the database and seed all data:
```bash
$ python3 seed_database.py
```
Run the app from the command line:
```bash
$ python3 server.py
```

## <a name="features"></a> Features 
User-friendly homepage. 
User registration with password confirmation, log in/log out.
Search wine and get information about it, displayed on a wine profile page -- interactive page that allows users to favorite, rate, and comment on a wine. Ability to favorite/unfavorite, rate and comment/update rating and comment. Individual user ratings and average of user ratings displayed using star rating schematic crated with HTML forms and CSS. 
User profile page displays user info, activity stats, and data analysis of favorited wines in the form of Chart.js visualizations and wine recommendations of similar wines.

## <a name="about"></a>About the Developer
Topnote creator Lynda Banh graduated from the University of California, Berkeley with a degree in Molecular and Cell Biology. She has passed the Court of Master Sommeliers level 1 course and exam. This is her first full-stack project. She can be found on [LinkedIn](https://www.linkedin.com/in/lyndabanh) and on [Github](https://github.com/lyndabanh).