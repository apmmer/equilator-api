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
  `make run-all`  
 - open in browser "***0.0.0.0:8000/docs***"  and enjoy interactive documentation.

## 3. Add your custom ranges designations
 - Find  
  ![auth button](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/authorize_button.png?raw=true)  
  on the top right. Enter your apikey from **.env** there and click **Authorize** button
 - Using interactive documentation, open "***POST api/v1/designations***"
 - Familiarize yourself with the syntax of a range creation (endpoint description)
 - Click "**Try it out**" in the bottom right side, below the endpoint description
 - Input request body like this (do not make it large for the first time)  
    ![post_designation_body](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/post_designation_body.png?raw=true)  
 - Click **Execute** button  
 - Congratulations! Response code is **201** and you designation was recorded successfully  
    ![post_designation_res](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/post_designation_res.png?raw=true)  

## 4. Create weighted ranges from designations
 - Visit "***POST api/v1/weighted_ranges/from_designation***"
 - Input valid params data and click **Execute**  
  ![highjack_opening](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/highjack_opening.png?raw=true)  
 - Now you can see combos with declared default weight  
 - Weight can be changed using "***PATCH api/v1/weighted_ranges/{weighted_range_id}***" endpoint

## 5. Make equity computations
 - Create at least 2 weighted ranges (with different names)
 - Visit "***POST api/v1/reports/equity_report***"
 - Enter your ranges IDs and board (cards on the table) to calculate winning probabilities  
    ![equity_request](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/equity_request.png?raw=true)  
 - Click **Execute** button
 - Get your equity report:  
  ![equity_response](https://github.com/vik-backend/equilator-api/blob/readme-edition/static/equity_response.png?raw=true)  
