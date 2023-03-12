from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors

# Connect to the database
# pip install pymysql
# pip install cryptography
# create database named "crud"

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Loveufather@123',
                             database='crud',
                             )


app = Flask(__name__)

# by defaul get request aaauxa
@app.route('/')
def Index():
    cur = connection.cursor() #cur vanne instance banako
    cur.execute("SELECT  * FROM student")
    data = cur.fetchall() # jj return vako data xa yo data ma aayera basxa
    cur.close()

    return render_template('index.html', student=data)


@app.route('/insert', methods=['POST'])
def insert():
#  data secure garna lai usually post request pathaine garinxa
    if request.method == "POST":
        flash("Data Inserted Successfully") #jaba halme data insert garxau euta pop up aauxa
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = connection.cursor()
        cur.execute(
            "INSERT INTO student (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        connection.commit()
        return redirect(url_for('Index')) #url_for le index.py lai aajai call garxa


@app.route('/delete/<string:id_data>', methods=['GET']) # string : id data le chai data ma j xa tellai delate 
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('Index'))  


@app.route('/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id'] 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = connection.cursor()
        cur.execute("""
               UPDATE student
               SET name=%s, email=%s, phone=%s
               WHERE id=%s 
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        connection.commit()
        return redirect(url_for('Index'))


if __name__ == '__main__':
    # session cookies for protection against cookie data tampering.
    app.secret_key = 'super secret key'
    # It will store in the hard drive
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)