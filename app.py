from flask import Flask, render_template, session, request, redirect, url_for
import mysql.connector
from datetime import timedelta
from PIL import Image
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "心がカギ"
app.permanent_session_lifetime = timedelta(hours=24)

# TOP-------------------------------------------------------------------------------------------


@app.route("/", methods=["GET"])
def top():
    result = {}
    return render_template("index.html", result=result)


@app.route("/result", methods=["POST"])
def result():
    sql = "SELECT * FROM chara ORDER BY rand() LIMIT 1;"

    result = select(sql)

    return render_template("index.html", result=result)


def con_db():
    con = mysql.connector.connect(
        host="localhost", user="apex", passwd="apex", db="apex_random"
    )
    return con


def select(sql):
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        result = cur.fetchall()
    except mysql.connector.errors.ProgrammingError as e:
        print("***DB接続エラー***")
        print(type(e))
        print(e)
    except Exception as e:
        print("***システム運行プログラムエラー***")
        print(type(e))
        print(e)
    finally:
        cur.close()
        con.close()
    return result


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
