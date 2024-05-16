# powerplant-coding-challenge

Author of this Pull Request: Charles Frère

Company: LittleBigCode

# Deployment instructions

```bash
python src/main.py
```

## Docker deployment

```bash
docker build -t powerplant-api .
```

```bash
docker run -p 8888:8888 powerplant-api
```


## Test the API

Once the container is up and running, you can use the API with curl commands of this form. 
Feel free to provide different input files to the API to check results. 

```bash
curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://0.0.0.0:8888/productionplan
```
