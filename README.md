# Blood-Donation-System
 
I made this social app for all the blood donor that want to help all people who need a urgent blood transfusion.
No authentication is required since this web app use the email address as user identifier.

Requirements:

0- Install pip from the terminal: pip3 intstall pipenv

1- Create a virtual enviroment in the terminal with pipenv shell 

2- Install flask, Flask-SQLAlchemy 

3- Open the python shell from the terminal with the command python and from there run the commands: --> from app import db 
                                                                                                    --> db.create_all() 
                                                                                                    --> exit()
                                                                                                    
4- Run the application with the comand python app.py

# Here the newest version deployed on Heroku: 
# https://bd-system.herokuapp.com/

New features:

-Added 3 months threshold for every blood donation

-Added 7 days threshold for every blood request

-Added flash messages





