# Mini Data Query Simulation Engine

## Overview
A simple Flask-based API that simulates AI-driven SQL query processing, validation, and explanation.

🌐 **Live API:** [Mini Data Query Simulation Engine](https://mini-data-query-simulation-engine-3sow.onrender.com)

## Features
- Convert natural language queries into SQL.
- Validate if a query type is supported.
- Explain the query’s intent.
- Store queries in an SQLite database.
- Secure API with API Key authentication.

## Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd Mini-Data-Query-Simulation-Engine
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints
### 1. Convert Query to SQL
**POST /query**  
Converts a natural language query to SQL and returns a simulated result.
#### Request:
```json
{
  "query": "Get total sales for Q1 2024"
}
```
#### Response:
```json
{
  "query": "get total sales for q1 2024",
  "sql_equivalent": "SELECT SUM(amount) FROM sales WHERE quarter='Q1' AND year=2024;",
  "result": { "total_sales": 35000 }
}
```
#### Curl Command:
```sh
curl -X POST https://mini-data-query-simulation-engine-3sow.onrender.com/query \
     -H "X-API-Key: your-secure-api-key" \
     -H "Content-Type: application/json" \
     -d '{"query": "Get total sales for Q1 2024"}'
```

### 2. Explain Query
**POST /explain**  
Explains the intent of the query.
#### Request:
```json
{
  "query": "Get total revenue for 2024"
}
```
#### Response:
```json
{
  "query": "Get total revenue for 2024",
  "interpretation": "Extracting revenue data from the database."
}
```
#### Curl Command:
```sh
curl -X POST https://mini-data-query-simulation-engine-3sow.onrender.com/explain \
     -H "X-API-Key: your-secure-api-key" \
     -H "Content-Type: application/json" \
     -d '{"query": "Get total revenue for 2024"}'
```

### 3. Validate Query
**POST /validate**  
Checks if the query type is supported.
#### Request:
```json
{
  "query": "Show all employees hired in 2023"
}
```
#### Response:
```json
{
  "query": "Show all employees hired in 2023",
  "valid": false
}
```
#### Curl Command:
```sh
curl -X POST https://mini-data-query-simulation-engine-3sow.onrender.com/validate \
     -H "X-API-Key: your-secure-api-key" \
     -H "Content-Type: application/json" \
     -d '{"query": "Show all employees hired in 2023"}'
```

## Authentication
Include an API key in the request headers:
```sh
curl -X POST https://mini-data-query-simulation-engine-3sow.onrender.com/query \
     -H "X-API-Key: your-secure-api-key" \
     -H "Content-Type: application/json" \
     -d '{"query": "Get total sales for Q1 2024"}'
```

## Deployment
- Suitable for deployment on platforms like Render.
- Ensure `data.db` persists for storing queries.
- Update `API_KEY` for better security.

## License
MIT License

