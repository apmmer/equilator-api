# The Equilator

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![numba-badge](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/numba_grey_small.jpg?raw=true) 
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![welcome pic](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/shouldIwin.jpg?raw=true)  
**A fast service that can store ranges and calculate winning probabilities with hands weight.**

## Your journey thru this project:
## 1. Build & run tests
 - Ensure docker/compose is installed in your unix system.  
 - Ensure there is at least 1 GB ram in your system.  
  
  Then run commands in console:
 - Visit correct folder:  
  `cd folder/in/your/system/to/store/the/project`  
 - Clone repository:  
  `git clone https://github.com/vik-backend/equilator-api.git`  
 - Visit project folder:  
  `cd equilator-api`  
 - Finally run tests:  
  `make tests`  

  Tests should be passed successfully

## 2. Run equilator-API 
 - Run from project directory:  
 ```bash
    make run-all
 ```  
 - open in browser "***0.0.0.0:8000/docs***"  and enjoy interactive documentation.

## 3. Add your custom ranges designations
 - Using interactive documentation, open "***POST api/v1/designations***"
 - Familiarize yourself with the syntax of a range creation
 - Click "**Try it out**" in the bottom right side, below endpoint description
 - 