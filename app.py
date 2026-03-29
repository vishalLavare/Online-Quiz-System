from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import bcrypt
from db import get_db_connection, init_db
import os
from datetime import timedelta

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

# --- Base Route ---

@app.route('/')
def home():
    return app.send_static_file('index.html')

# --- Auth Routes ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            access_token = create_access_token(identity=str(user['user_id']))
            return jsonify({
                "message": "Login successful",
                "user_id": user['user_id'],
                "access_token": access_token
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    finally:
        cursor.close()
        conn.close()

# --- Quiz Routes ---

@app.route('/questions', methods=['GET'])
def get_questions():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get limit from query parameter (default 10)
        limit = request.args.get('limit', default=10, type=int)

        # Fetch random questions with limit
        cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT %s", (limit,))
        questions = cursor.fetchall()

        if not questions:
            return jsonify([]), 200

        # Fetch options for these specific questions
        q_ids = [q['question_id'] for q in questions]
        format_strings = ','.join(['%s'] * len(q_ids))
        cursor.execute(f"SELECT * FROM options WHERE question_id IN ({format_strings})", tuple(q_ids))
        options = cursor.fetchall()

        # Get lang from query parameter (default 'en')
        lang = request.args.get('lang', default='en', type=str)

        for q in questions:
            # Swap with Hindi/Marathi if available
            if lang == 'hi' and q.get('question_hi'): q['question'] = q['question_hi']
            if lang == 'mr' and q.get('question_mr'): q['question'] = q['question_mr']
            
            # Filter and translate options
            q['options'] = []
            for o in options:
                if o['question_id'] == q['question_id']:
                    # Translate option text
                    if lang == 'hi' and o.get('option_text_hi'): o['option_text'] = o['option_text_hi']
                    if lang == 'mr' and o.get('option_text_mr'): o['option_text'] = o['option_text_mr']
                    
                    # Remove is_correct and internal translation fields for security/cleanliness
                    public_opt = {
                        'option_id': o['option_id'],
                        'option_text': o['option_text']
                    }
                    q['options'].append(public_opt)

        return jsonify(questions), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/submit', methods=['POST'])
@jwt_required()
def submit_answers():
    data = request.get_json()
    user_id = get_jwt_identity()
    answers = data.get('answers') # List of {question_id: X, option_id: Y}

    if not answers:
        return jsonify({"error": "No answers provided"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        print(f"DEBUG: Receiving {len(answers)} answers for user {user_id}")
        for ans in answers:
            q_id = ans.get('question_id')
            o_id = ans.get('option_id')
            print(f"DEBUG:   - Q:{q_id}, O:{o_id}")
            
            # Prevent duplicate submissions using REPLACE or ON DUPLICATE KEY UPDATE
            cursor.execute("""
                INSERT INTO user_answers (user_id, question_id, selected_option) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE selected_option = VALUES(selected_option)
            """, (user_id, q_id, o_id))
        
        conn.commit()
        print(f"DEBUG: Answers committed for user {user_id}")
        return jsonify({"message": "Answers submitted successfully"}), 200
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"DEBUG ERROR in /submit:\n{error_msg}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/score/<int:user_id>', methods=['GET'])
def get_score(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Calculate score using JOIN and COUNT
        # SUM(CASE WHEN o.is_correct THEN 1 ELSE 0 END) is more flexible than just COUNT
        query = """
            SELECT 
                COUNT(*) as total_attempted,
                SUM(CASE WHEN o.is_correct THEN 1 ELSE 0 END) as score
            FROM user_answers ua
            JOIN options o ON ua.selected_option = o.option_id
            WHERE ua.user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        score = int(result['score'] or 0)
        total = result['total_attempted']
        print(f"DEBUG: Score for user {user_id}: {score}/{total}")
        
        return jsonify({
            "user_id": user_id,
            "score": score,
            "total_attempted": total
        }), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Rank users by score (highest first)
        query = """
            SELECT 
                u.user_id,
                u.username,
                SUM(CASE WHEN o.is_correct THEN 1 ELSE 0 END) as score
            FROM users u
            LEFT JOIN user_answers ua ON u.user_id = ua.user_id
            LEFT JOIN options o ON ua.selected_option = o.option_id
            GROUP BY u.user_id
            ORDER BY score DESC, u.username ASC
        """
        cursor.execute(query)
        leaderboard = cursor.fetchall()
        
        # Convert Decimals to int for JSON serialization
        for entry in leaderboard:
            entry['score'] = int(entry['score'] or 0)

        return jsonify(leaderboard), 200
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Initialize database tables
    init_db()
    app.run(host='0.0.0.0', port=5000)
