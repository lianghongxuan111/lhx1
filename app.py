from flask import Flask, request, redirect, render_template
import mysql.connector

app = Flask(__name__)


def create_table():
    # 连接到MySQL数据库
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="python"
    )
    mycursor = mydb.cursor()
    # 创建用户表，如果不存在
    mycursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username VARCHAR(255))''')
    mydb.commit()
    mydb.close()


def login(username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="python"
    )
    mycursor = mydb.cursor()
    # 查询用户是否存在
    mycursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = mycursor.fetchone()
    mydb.close()
    return user is not None


@app.route('/a', methods=['GET', 'POST'])
def page_a():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return "用户名不能为空"
        if login(username):
            return redirect('/b?username=' + username)
        else:
            # 注册新用户
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="python"
            )
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            mydb.commit()
            mydb.close()
            return redirect('/b?username=' + username + '&is_new_user=1')
    return render_template('a.html')


@app.route('/b')
def page_b():
    username = request.args.get('username')
    is_new_user = request.args.get('is_new_user')
    if is_new_user:
        welcome_message = "欢迎新用户 " + username
    else:
        welcome_message = "欢迎用户 " + username
    return render_template('b.html', username = username, welcome_message = welcome_message)


if __name__ == '__main__':
    create_table()
    app.run(debug=True)