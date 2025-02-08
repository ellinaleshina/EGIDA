#Это модуль для сохранения логов в базу данных
#Важно! Ip адрес хоста должен соответствовать текущему адресу БД!!

from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
host_ip="192.168.31.34"
app = Flask(__name__)
@app.route('/logger', methods=['POST'])
def send_log_to_BD():
    connection = 0
    data = request.json
    if not data or "prompt" not in data or "label" not in data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="postgres",
                                  host=host_ip,
                                  port="5433",
                                  database = "log_bd_linux",
                                  options="-c client_encoding=utf8"
                                  )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        id = 8 #временная заглушка
        if data.get("label", "") == 'unsafe':
            bool_label=False
        else:
            bool_label = True
        new_record = (id, datetime.datetime.now(), bool_label, data.get("prompt", ""))

        postgres_insert_query = """ INSERT INTO classify_logs (user_id, time, label, promt)
                                       VALUES (%s,%s,%s, %s)"""
        cursor.execute(postgres_insert_query, new_record) #для теста

        cursor.close()
        connection.close()
        
    except Exception as e:
       return jsonify({"error": "Connect to bd error", "details": str(e)})
    

    return jsonify({"Result of logging": "Success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8025)