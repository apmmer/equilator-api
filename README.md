# The Equilator

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![numba-badge](https://github.com/vik-backend/equilator-api/blob/main/static/numba_grey_small.jpg?raw=true) 
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![welcome pic](https://github.com/vik-backend/equilator-api/blob/main/static/shouldIwin.jpg?raw=true)  
The Equilator is a dedicated poker hand analysis service, designed to **store poker hand ranges** and **efficiently calculate the probabilities of winning** under various circumstances. Its power lies in its **speed**, **precision**, and **standalone capabilities**. Here are its key features:

 - **Supports range-vs-range (r-r), hand-vs-hand (h-h), hand-vs-range (h-r), and range-vs-hand (r-h) calculations.**
 - **Enables custom hand weights calculations** with an output for each hand in the range.
 - Comprehensive coverage of all game stages: **Preflop, Flop, Turn, and River.**
 - **Exceptional performance** while remaining simple, compact, and standalone.
  
Please note that this is a single-core version of the Equilator. A more powerful multi-core version, which **runs multiple times faster** and offers the **possibility to calculate the full postflop tree by a single request with NO PENALTY**, is also available for purchase. It has been designed to serve as a **self-sufficient alternative to commercial solutions like FlopZilla or Piosolver**. For more information about the commercial version, please feel free to get in touch.  
  
### 1. Build & run tests  
 1. Ensure [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) are installed on your system.  
 2. Ensure your system has at least 1 GB of free RAM.  
  
After confirming the above, follow these steps:  
 - **Clone the repository:**
   ```bash
   git clone https://github.com/vik-backend/equilator-api.git
   ```
  
 - **Navigate to the project folder:**
   ```bash
   cd equilator-api
   ```
 
 - **Ensure your operating system supports Makefile and run the following command:**
   ```bash
   make tests
   ```
  
 - **Alternatively, you can build and run the tests manually with Docker:**
   ```bash
   docker build -t equilator_api -f openapi/Dockerfile .
   docker-compose -f docker-compose.test.yml up --exit-code-from equilator_api_test
   ```
  
  
### 2. Run equilator-API  
 - Run from project directory:  
   ```bash
   make run-all
   ```

 - **Alternatively, you can use Docker Compose to build and run the service:**
   ```bash
   docker-compose up --build
   ```

 - Once the service is running, you can access the interactive documentation by navigating to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) in your web browser.  
  
  
## Detailed usage description
### 1. Add your custom ranges designations
 - Find  
  ![auth button](https://github.com/vik-backend/equilator-api/blob/main/static/authorize_button.png?raw=true)  
  on the top right. Enter your apikey from **.env** there and click **Authorize** button
 - Using interactive documentation, open "***POST api/v1/designations***"
 - Familiarize yourself with the syntax of a range creation (endpoint description)
 - Click "**Try it out**" in the bottom right side, below the endpoint description
 - Input request body like this (do not make it large for the first time)  
    ![post_designation_body](https://github.com/vik-backend/equilator-api/blob/main/static/post_designation_body.png?raw=true)  
 - Click **Execute** button  
 - Congratulations! Response code is **201** and you designation was recorded successfully  
    ![post_designation_res](https://github.com/vik-backend/equilator-api/blob/main/static/post_designation_res.png?raw=true)  

### 2. Create weighted ranges from designations
 - Visit "***POST api/v1/weighted_ranges/from_designation***"
 - Input valid params data and click **Execute**  
  ![highjack_opening](https://github.com/vik-backend/equilator-api/blob/main/static/highjack_opening.png?raw=true)  
 - Now you can see combos with declared default weight  
 - Weight can be changed using "***PATCH api/v1/weighted_ranges/{weighted_range_id}***" endpoint

### 3. Make equity computations
 - Create at least 2 weighted ranges (with different names)
 - Visit "***POST api/v1/reports/equity_report***"
 - Set your ranges IDs and board (cards on the table) to calculate winning probabilities  
    ![equity_request](https://github.com/vik-backend/equilator-api/blob/main/static/equity_request.png?raw=true)  
 - Click **Execute** button and get your equity report:  
  ![equity_response](https://github.com/vik-backend/equilator-api/blob/main/static/equity_response.png?raw=true)  
