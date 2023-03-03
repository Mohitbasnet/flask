from flask import Flask, render_template, request,flash,redirect,url_for
import pymysql.connections

# pip install pymysql
# pip install cryptography
# create database named "crud"

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Loveufather@123',
                             database='crud',
                             )

app = Flask(__name__)

@app.route('/')
def Index():
    cur = connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = connection.cursor()
        cur.execute(
            "INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    return render_template('index.html')


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        return render_template('index.html')


if __name__== '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)