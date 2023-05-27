# The Equilator

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![numba-badge](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/numba_grey_small.jpg?raw=true) 
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![welcome pic](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/shouldIwin.jpg?raw=true)  
The Equilator is a dedicated poker hand analysis service, designed to **store poker hand ranges** and **efficiently calculate the probabilities of winning** under various circumstances. Its power lies in its **speed**, **precision**, and **standalone capabilities**. Here are its key features:

 - **Supports range-vs-range, hand-vs-hand, hand-vs-range or range-vs-hand calculations.**
 - **Enables custom hand weights calculations** with an output for each hand in the range.
 - Comprehensive coverage of all game stages: **Preflop, Flop, Turn, and River.**
 - **Exceptional performance** while remaining precise and standalone.  
  
Please note that this is a single-core version of the Equilator. If you are interested in more powerful multi-core version, which runs multiple times faster and offers the possibility to calculate the full postflop tree by a single request (with no penalty!), please feel free to get in touch.  
  
  
### How to Build & Run Tests 
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
  
  
### How to Run the Equilator API
 - Run from project directory:  
   ```bash
   make run-all
   ```

 - **Alternatively, you can use Docker Compose to build and run the service:**
   ```bash
   docker-compose up --build
   ```

 - Once the service is running, you can access the interactive documentation by navigating to [0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) in your web browser.  
  
  
## Detailed Usage Guide

Follow this step-by-step guide to get the most out of the Equilator.

### 1. Add Your Custom Ranges Designations

To add your custom ranges, please follow these steps:

1. **Authorize**: On the top right, find the "**Authorize**" button. Enter your apikey from your **.env** file and click on "**Authorize**".

   ![auth button](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/authorize_button.png?raw=true)

2. **Open Endpoint**: Using interactive documentation, open "**POST api/v1/designations**". Familiarize yourself with the syntax of a range creation (endpoint description).

3. **Try It Out**: Click on "**Try it out**" on the bottom right side, below the endpoint description.

4. **Enter Request Body**: Input the request body. Make sure to keep it small initially.  
   Request body example:
    ```bash
    {
      "range_definition": "AKs,9h9s"
    }
    ```

5. **Execute**: Click on the "**Execute**" button.

If done correctly, the response code should be **201**, indicating successful recording of your designation.  

![post_designation_res](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/post_designation_res.png?raw=true)

### 2. Create Weighted Ranges from Designations

To create weighted ranges from designations:

1. **Open Endpoint**: Visit "**POST api/v1/weighted_ranges/from_designation**".

2. **Enter Parameters**: Input valid parameters data and click on "**Execute**".  

![highjack_opening](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/highjack_opening.png?raw=true)

Now, you can see combos with declared default weight. Weight can be changed using the "**PATCH api/v1/weighted_ranges/{weighted_range_id}**" endpoint.

### 3. Equity Computations

To compute equity, you need at least 2 weighted ranges (with different names). Here's how you do it:

1. **Open Endpoint**: Visit "**POST api/v1/reports/equity_report**".

2. **Set Parameters**: Set your ranges IDs and board (cards on the table) to calculate winning probabilities.  

![equity_request](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/equity_request.png?raw=true)

3. **Execute**: Click on the "**Execute**" button.

You will then receive your equity report:

![equity_response](https://github.com/vik-backend/equilator-api/blob/files-refactor/static/equity_response.png?raw=true)
