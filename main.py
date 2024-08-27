from flask import Flask, request, jsonify, send_file
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
from flask import render_template

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kheang123'
app.config['MYSQL_DB'] = 'issuestracker'

mysql = MySQL(app)

@contextmanager
def get_db_cursor():
    cursor = mysql.connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/')
def root():
    return jsonify({"Hello": "World"})
Item =[]
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item = Item(text=data['text'], status=data['status'])
    with get_db_cursor() as cursor:
        query = "INSERT INTO items (text, status) VALUES (%s, %s)"
        values = (item.text, item.status)
        cursor.execute(query, values)
        mysql.connection.commit()
        item.id = cursor.lastrowid
    return jsonify({"id": item.id, "text": item.text, "status": item.status})

@app.route('/items', methods=['GET'])
def list_items():
    limit = request.args.get('limit', default=10, type=int)
    with get_db_cursor() as cursor:
        query = f"SELECT * FROM items LIMIT {limit}"
        cursor.execute(query)
        items = cursor.fetchall()
    return jsonify([{"id": item[0], "text": item[1], "status": item[2]} for item in items])

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    with get_db_cursor() as cursor:
        query = "SELECT * FROM items WHERE id = %s"
        cursor.execute(query, (item_id,))
        item = cursor.fetchone()
    if item:
        return jsonify({"id": item[0], "text": item[1], "status": item[2]})
    else:
        return jsonify({"error": f"Item {item_id} not found"}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], password=data['password'])
    with get_db_cursor() as cursor:
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (user.username,))
        if cursor.fetchone():
            return jsonify({"error": "Username already registered"}), 400
        
        hashed_password = generate_password_hash(user.password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (user.username, hashed_password))
        mysql.connection.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User(username=data['username'], password=data['password'])
    with get_db_cursor() as cursor:
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (user.username,))
        result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Invalid username or password"}), 401
    
    if not check_password_hash(result[0], user.password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    return jsonify({"message": "Login successful"})

@app.route('/login_register')
def login_register_page():
    return send_file('static/login_register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    
