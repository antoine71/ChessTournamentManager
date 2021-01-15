# CHESS TOURNAMENT MANAGER
Openclassrooms - Parcours développement Python Projet 4

## Status
This ready for evaluation.

## Description
This program is a manager for chess tournaments using the Swiss rounds system.
* Create your players and your tournaments and the program will automatically draw the games for each round.
* Enter the results, and the program will automatically calculate the rankings of the tournament.
* The tournaments and players are saved in a local database. You can quit the program anytime and restart a tournament where you have left it. 

## How to Clone
Just download the repository to your computer in a location of your choice.

## Installation
To install and run this program, you must:
1. Install python3 to your computer: [python.org](https://www.python.org/)
2. Navigate to your local repository folder
3. Run the following commands
```bash
python3 -m venv env                  #create a virtual environment
source env/bin/activate             #activate the virtual environment
pip install -r requirements.txt     #install the external modules
python3 main.py                      #run the program
```

## Create a flake8 report
Run the following command line:
```bash
flake8 --exclude .git,__pycache__,venv/,env/ --max-line-length=119 --format=html --htmldir=flake8-rapport
```
A html report will be created in the directory ./flake8_report/

## Preview
![](/preview.jpg)
