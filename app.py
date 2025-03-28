from flask import Flask, request, jsonify
import os, sqlite3

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")  # Keep SQLite inside the project

# Use `/persistent` if Render allows (not available on free plan)
PERSISTENT_PATH = "/persistent/data.db"
if os.path.exists("/persistent"):
    DB_PATH = PERSISTENT_PATH

# 🔹 Database Helper Function
def get_db_connection():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        return None

# 🔹 Ensure database exists & create necessary tables
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_query TEXT NOT NULL,
                    sql_equivalent TEXT NOT NULL
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()
    else:
        print("Error: Unable to establish database connection.")

init_db()


API_KEY = os.getenv("API_KEY", "default-api-key")


def authenticate(req):
    """Simple API key authentication"""
    key = req.headers.get("X-API-Key")
    return key == API_KEY

@app.route("/")
def home():
    return jsonify({"message": "Gen AI Query Simulation Engine is running!"})

@app.route("/query", methods=["POST"])
def query():
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing query"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    user_query = data["query"].lower()

    # Basic mock SQL translation logic with results
    mock_results = {
        "sales": ("SELECT SUM(amount) FROM sales WHERE quarter='Q1' AND year=2024;", {"total_sales": 35000}),
        "revenue": ("SELECT SUM(revenue) FROM transactions WHERE year=2024;", {"total_revenue": 150000}),
        "customers": ("SELECT COUNT(*) FROM customers WHERE registered_year=2024;", {"new_customers": 1240}),
        "products": ("SELECT * FROM products WHERE category='Electronics';", [
            {"product": "Laptop", "price": 1200},
            {"product": "Smartphone", "price": 899}
        ])
    }
    
    sql, mock_result = None, None
    for key in mock_results:
        if key in user_query:
            sql, mock_result = mock_results[key]
            break
    
    if not sql:
        return jsonify({"error": "Unsupported query type"}), 400

    # Store query in DB
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO queries (user_query, sql_equivalent) VALUES (?, ?)", (user_query, sql))
            conn.commit()
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

    response = {
        "query": user_query,
        "sql_equivalent": sql,
        "result": mock_result
    }

    return jsonify(response), 200

@app.route("/explain", methods=["POST"])
def explain():
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing query"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    user_query = data["query"]

    # Mock explanation
    explanation = {
        "query": user_query,
        "interpretation": "Extracting relevant data from the database based on keywords."
    }

    return jsonify(explanation), 200

@app.route("/validate", methods=["POST"])
def validate():
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing query"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    user_query = data["query"]

    # Mock validation logic
    valid = any(keyword in user_query.lower() for keyword in ["sales", "revenue", "customers", "products"])
    
    return jsonify({"query": user_query, "valid": valid}), 200

if __name__ == "__main__":
    app.run(debug=False)
