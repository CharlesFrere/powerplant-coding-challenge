

# Powerplant Coding Challenge

Author of this Pull Request: Charles Frère

Company: LittleBigCode

## Overview

This project aims to develop an API that calculates the optimal power output for each power plant to meet a given 
load while minimizing costs. The algorithm considers various factors such as fuel prices, CO2 costs, and wind availability.

## Algorithms Explanation


I implemented 2 algorithms. I first came with a straitforward idea of a first alorithm in continuous case:


### First algorithm

The objective is to match the energy demand (load) by minimizing the cost.
The algorithm uses a merit-order dispatch approach:
1. **Cost Calculation**: Each power plant's cost per MWh is calculated based on its fuel type and efficiency.
2. **Sorting**: Power plants are sorted by cost, prioritizing cheaper sources.
3. **Load Distribution**: The load is distributed among the power plants starting with the cheapest until the load is met or all plants are utilized.
4. **Constraints Handling**: Minimum and maximum generation constraints for each plant are respected during the load distribution.

### Second algirithm

Then I realised that in some cases like payload2.json, the given result was not the optimal 
production to minimize the cost. Here is why I thought about a dynamic programming approach. 


To achieve decimal precision, I had to scale the discrete problem to a factor 10. 
This way we can solve the problem in a dynamic programming way with values of p precise at +- 0.1 MWh

The optimisation problem would of course have been easily solved using scipy.optimize.linprog in continuous cases
but this algorithm reaches a decent precision without using external libraries. 

1. Precision Handling: The load and power values are scaled to integers to manage decimal precision.
2. DP Table Initialization: The DP table (dp) is initialized with infinity, and **dp[0][0]** is set to 0.
3. Filling the DP Table:
   - Iterate through each power plant.
   - For each possible load value, update the DP table by considering the cost of producing each power value within the plant's range.
4. Backtracking:
   - Determine the optimal power distribution by backtracking through the DP table.
   - Ensure the power values are scaled back to their original precision.

The principal downside of this second algorithm is that it is way slower than the first one.

## Deployment Instructions

There are 2 ways of using this application: 
- Locally by installing the requirements in a virtual environment
- With a Docker container that can be deployed anywhere. I would recommend this way of using the app


### Local Deployment 

1. Make sure you python3.11 installed
```bash
python --version
```

2. Create a virtual environment and activate it

```bash
python -m venv .venv 
source .venv/bin/activate
```

3. Install necessary packages

```bash
pip install -r requirements.txt
```

Once this is done, you can run the application locally by executing the main script

```bash
python src/main.py
```

For the dynamic programming approach: 

Execute 
```bash
python src/main_discrete_case.py
```

To launch the API based on a dynamic programming algorithm.

Test it in the same way as with main.py: 

```bash
curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://0.0.0.0:8888/productionplan
```

### Docker deployment

1. Build the Docker image with this command

```bash
docker build -t powerplant-api .
```

2. run the application in a container 
```bash
docker run -p 8888:8888 powerplant-api
```


### Test the API

Once the container is up and running, you can use the API with curl commands of this form. 
Feel free to provide different input files to the API to check results. 

```bash
curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://0.0.0.0:8888/productionplan
```

Test the API via the swagger UI by connecting to http://localhost:8888/apidocs

## Bonus: Consider CO_2 emissions

You can also consider co2 emissions in the computation by setting a positive value for "co2_cost" in the payload file. 
The updated costs will be computed 
