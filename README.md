# Tic-Tac-Toe Project

## Headers
This project is a simple console tic tac toe game, which was made using python 3.12.X and MySQL Workbench 8.0 CE. This project is easy to use, with no code changed nececary to connect with your database.
You may check latest python version by clicking [here](https://www.python.org/downloads/).

## Installation Process

1. You should have **latest Python verison installed** (For any reasons it may not work on latest version, you might need to downgrade to 3.12.X) You can find python versions by clicking [here](https://www.python.org/downloads/).

2. You will need to **install dependency** for this project, open up cmd and type in command bellow

>pip install mysql-connector-python

3. Install **MySQL Workbench latest version** (For any reasons it may not work on latest version, you might need to downgrade to 8.0 CE) You can find MySQL Workbench versions by clicking [here](https://www.mysql.com/products/workbench/).

4. Make sure to have **setup connection inside MySQL Workbench** that you will be using for this project.

5. Modify config.ini file to your respective needs, **modifying host, user and password** to be able connect it with your database.

## Setup

1. Run the code inside *"db_connect_prc.py"* (**OPTIONAL** This will only make sure that user can connect to the database!)
2. Run the code inside *"integration_prc.py"*, this will integrate existing data and create tables inside your databse.
3. Run the code inside *"startup.py"*, this will start up the game

