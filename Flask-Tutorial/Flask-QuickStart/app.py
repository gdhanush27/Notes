import os
from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HESDERS']='Content-Type: Application/json'

# SQL Connection ======================================================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_ADMIN_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_ADMIN_PASSWORD')
app.config['MYSQL_DB'] = 'test'
# ======================================================================
mysql = MySQL(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('homePage.html')

@app.route('/fetchall', methods = ['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            # SELECT column1, column2, ...
            # FROM table_name
            sql = "SELECT * FROM user"
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return jsonify({"Status": True, "message": "Data retrieved successfully", "data":data})
        
        except Exception as e:
            return jsonify({"Status": False, "message": str(e)})
        
    else:
        return jsonify({"Status":False, 'message': 'Method not allowed'}), 405

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Data from front-end ===========================
        data = request.get_json()
        user_id = data.get('username')
        password = data.get('password')
        # ===============================================
        cur = mysql.connection.cursor()
        sql = "SELECT password FROM user WHERE user_id = \"{}\"".format(user_id)
        cur.execute(sql)
        data = cur.fetchall()
        if len(data)==0:
            return jsonify({"Status":False,"message" : "Invalid User"})
        if data[0][0]!=password :
            return jsonify({"Status":False,"message" : "Invalid Password" })
        return jsonify({"Status":True,"message":"Login Successfull" })
    else:
        return jsonify({"Status":False, 'message': 'Method not allowed'}), 405
    

@app.route('/signup', methods = ['GET', 'POST'])
def insert():
    if request.method == 'POST':
        
        # Data from front-end ===========================
        data = request.get_json()
        user_id = data.get('username')
        password = data.get('password')
        # ===============================================

        try:

            # INSERT INTO table_name (column1, column2, column3, ...)
            # VALUES (value1, value2, value3, ...)
            cur = mysql.connection.cursor()
            s = "INSERT INTO user (user_id, password) VALUES (%s, %s)"
            cur.execute(s, (user_id, password))
            mysql.connection.commit() # Yesterdays mistake
            cur.close()
            return jsonify({
                "Status": True, 
                "message": "Data inserted successfully"
                })
        
        except mysql.connection.IntegrityError as e:
            return jsonify({
                "Status": False, 
                "message":str(e)
                })
        
    else:
        return jsonify({"Status":False, 'message': 'Method not allowed'}), 405

@app.route('/update_password', methods = ['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        
        # Data from front-end ===========================
        data = request.get_json()
        user_id = data.get('username')
        new_password = data.get('new_password')
        # ===============================================

        try:

            # UPDATE table_name
            # SET column1 = value1, column2 = value2, ...
            # WHERE condition
            cur = mysql.connection.cursor()
            sql = "UPDATE user SET password = %s WHERE user_id = %s"
            cur.execute(sql, (new_password, user_id))
            mysql.connection.commit()
            cur.close()
            return jsonify({
                    "Status": True, 
                    "message": "Password updated successfully"
                    })
        
        except Exception as e:
            return jsonify({"Status": False, "message": str(e)})
    else:
        return jsonify({"Status": False, "message": "Method not allowed"}), 405

@app.route('/delete_user', methods = ['GET', 'POST'])
def delete_user():
    if request.method == 'POST':

        # Data from front-end ===========================
        data = request.get_json()
        user_id = data.get('username')
        # ===============================================

        try:
            cur = mysql.connection.cursor()
            sql = "DELETE FROM user WHERE user_id = %s"
            cur.execute(sql, (user_id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({
                "Status": True, 
                "message": "User deleted successfully"
                })
        
        except Exception as e:
            return jsonify({
                "Status": False, 
                "message": str(e)
                })
        
    else:
        return jsonify({
            "Status": False, 
            "message": "Method not allowed"
            }), 405
    
# Task:
# 1 -> Fetch details of 1 user with user_id
# 2 -> Create retype password and check if both are same
# 3 -> Update username if no douplicate found
# 4 -> Delete a user if given password matches password in DB