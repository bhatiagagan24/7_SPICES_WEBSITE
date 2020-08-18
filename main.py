from flask import Flask
from flask import render_template
from flask import request
import random
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('database.db')
cur = con.cursor()

con.execute('CREATE TABLE IF NOT EXISTS order_list(customer_name TEXT, phone_no INTEGER, order_no INTEGER, order_item TEXT, order_quantity INTEGER, order_status INTEGER)')
# order_status gives 0 for incomplete order and 1 for completed order
con.close()

password_flag = False


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    order_no = random.randint(0,1000000000)
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    if request.method == 'POST':
        order_data = request.form
        o1 = order_data['customer_name']
        o2 = order_data['customer_phone']
        o3 = order_data['order_name']
        o4 = order_data['order_qty']
        con.execute("INSERT INTO order_list(customer_name, phone_no, order_no, order_item, order_quantity, order_status) VALUES (?,?,?,?,?,?)", (o1, o2, order_no, o3, o4, 0, ))
        con.commit()
        con.close()
        return render_template('order.html', order_no = order_no)
    elif request.method == 'GET':
        con.commit()
        con.close()
        return render_template('order.html')

@app.route('/contact', methods=['GET'])
def contact():
    print('fine till here')
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'GET':
        return render_template('admin.html')
    elif request.method == 'POST':
        pwd = request.form.to_dict()
        print(pwd['password'])
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        if pwd['password'] == 'sevenspices':
            cur.execute('''SELECT * FROM order_list''')
            order_list = cur.fetchall()
            con.close()
            return render_template('admin.html', order_list=order_list)
        elif pwd['password'] != 'sevenspices':
            con.close()
            return render_template('admin.html', order_list='Wrong Password')






if __name__ == '__main__':
    app.run(debug=True)