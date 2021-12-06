import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

conn = psycopg2.connect(database="fl_db",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    # print(username)
    # print('\n', password)
    # print(records)

    if not username:
        not_field = 'Поле "Username" не заполнено, попробуйте ещё раз.'
        return render_template('login.html', not_field=not_field)
    if not password:
        not_field = 'Поле "Password" не заполнено, попробуйте ещё раз.'
        return render_template('login.html', not_field=not_field)

    # пользователя не существует
    if not records:
        return render_template('error_form.html')
    else:
        return render_template('account.html', full_name=records[0][1], lgn=username, psswrd=password)

cursor.close()
conn.close()


