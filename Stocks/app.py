import matplotlib, pymysql, add_data
matplotlib.use('agg')
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, flash, session
import pandas as pd
from Invester import graph

app = Flask(__name__)

app.secret_key = 'my_secret_key'
app.debug = True

db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            db='INVESTAR'
        )

#로그인 화면
@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('is_logged') is not None:
        if session.get('is_logged') == "g":
            return render_template("main.html", user="GUEST")
        else:
            return render_template("main.html", user=session.get('is_logged'))
    elif request.method == "POST":
        cursor = db.cursor()
        sql = 'SELECT PW FROM login where ID = %s;'
        userID = request.form['Username']
        userPW = request.form['pass']
        cursor.execute(sql, userID)
        user = cursor.fetchone()
        if user is None:
            flash("없는 아이디입니다.")
        elif sha256_crypt.verify(userPW, user[0]):
            session['is_logged'] = userID
            return render_template("main_2.html", user=session.get('is_logged'))
        else:
            flash("틀린 비밀번호입니다.")
        return render_template("login.html")
    else:
        return render_template("login.html")

# 게스트 로그인
@app.route('/guest', methods=['GET', 'POST'])
def guest():
    session['is_logged'] = "g"
    return render_template("main.html", user="GUEST")

# 회원가입 기능
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        cursor = db.cursor()
        name = request.form['name']
        email = request.form['email']
        userID = request.form['id']
        userPW = sha256_crypt.encrypt(request.form['pass'])
        sql_insert = "INSERT INTO `login` (`name`, `email`, `ID` , `PW`) VALUES (%s, %s, %s, %s);"
        val = [name, email, userID, userPW]
        # cursor.execute(sql_insert, val)
        cursor.execute(sql_insert ,val)
        db.commit()
        db.close()
        return redirect("/")
    else:
        return render_template("register.html")

# 로그아웃 기능
@app.route('/log_out')
def log_out():
    session.clear()
    return render_template("logout.html")

# 주식 db
@app.route('/stocks', methods=["GET", "POST"])
def refresh_price():
    cursor = db.cursor()
    sql = 'SELECT * FROM company_info'
    cursor.execute(sql)
    stock = cursor.fetchall()
    sql = 'SELECT distinct sectors FROM company_info'
    cursor.execute(sql)
    areas = cursor.fetchall()
    return render_template("stocks.html", stocks=stock[0: 20],
                           stocksize=len(stock), page_num=0, areas=areas, area='all', search='')


# 주식 db 목록 읽어오는 기능
@app.route('/stocks/<string:area>/<int:page_num>', methods=["GET", "POST"])
def stocks(area, page_num):
    input_name = ""
    if session.get('is_logged') is not None:
        cursor = db.cursor()
        if request.method == "POST":
            input_name = request.form['search']
            sql = f"SELECT * FROM company_info WHERE company LIKE '%{input_name}%'"
        else:
            sql = 'SELECT * FROM company_info'
            if area != 'all':
                sql += f" WHERE sectors = '{area}'"
        cursor.execute(sql)
        stock = cursor.fetchall()
        sql = 'SELECT distinct sectors FROM company_info'
        cursor.execute(sql)
        areas = cursor.fetchall()
        return render_template("stocks.html", stocks=stock[page_num * 20: (page_num + 1) * 20],
                               stocksize=len(stock), page_num=page_num, areas=areas, area=area, search=input_name)
    else:
        return render_template("login.html")


# 상세보기
@app.route('/chart/<string:input_stock>', methods=["GET", "POST"])
def show_stock(input_stock):
    go ='non'
    cursor = db.cursor()
    sql = f'SELECT company FROM company_info WHERE code = {input_stock}'
    cursor.execute(sql)
    name = cursor.fetchone()

    sql = f"SELECT * FROM result WHERE code = {input_stock} AND last_update >= date_sub(now(), interval 20 minute)"
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) >= 1:
        graph.bar(result)
        go = 'gogo'

    sql = f"select * from day_price where code = {input_stock} AND Date >= date_sub(now(), interval 3 MONTH)"
    cursor.execute(sql)
    df = pd.read_sql(sql, db)
    graph.data(df)
    return render_template('chart.html', results = result, code = input_stock, name=name, go=go)

# 소개페이지
@app.route('/introduce', methods=['GET', 'POST'])
def introduce():
    return render_template("introduce.html")

if __name__ == '__main__':
    add = add_data.add()
    add.excute()
    app.run()