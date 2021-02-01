from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import datetime
import os

def connectDatabase():
    DB_SETTING = {
        'host': '127.0.0.1', 
        'port': 3306, 
        'user': 'root', 
        'password': 'jb1000335', 
        'db': 'OBS', 
        'charset': 'utf8'
    }
    return pymysql.connect(**DB_SETTING)

def mergeAuthor(target):
    i = 0
    while i < len(target)-1:
        if target[i]['isbn'] == target[i+1]['isbn']:
            target[i]['author'] = target[i]['author'] + '/' + target[i+1]['author']
            del(target[i+1])
        else:
            i += 1
    return target

def checkNull(value):
    if not value or value == 'null':
        return None
    else:
        return value

app = Flask(__name__)
CORS(app, resources='/*')

@app.route('/getAllBook', methods=['GET'])
def getAllBook():
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * FROM BOOK_INFO'
        cursor.execute(SQLCommand)
        result = cursor.fetchall()
    attritube = ['name', 'image', 'isbn', 'publisher', 'author', 'price', 'date', 'storage', 'content', 'star']
    res = [dict(zip(attritube, r)) for r in result]

    res = mergeAuthor(res)
    return jsonify(res)

@app.route('/getBookInfo', methods=['POST'])
def getBook():
    isbn = request.form.get('isbn')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * FROM BOOK_INFO B WHERE B.ISBN=%s'
        cursor.execute(SQLCommand, (isbn))
        result = cursor.fetchall()
    attritube = ['name', 'image', 'isbn', 'publisher', 'author', 'price', 'date', 'storage', 'content', 'star']
    res = [dict(zip(attritube, r)) for r in result]
    res = mergeAuthor(res)[0]
    res['date'] = str(res['date'])
    return jsonify(res)

@app.route('/getBookSearch', methods=['POST'])
def search():
    search = request.form.get('search')
    search = '%' + search + '%'
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * \
                      FROM BOOK_INFO B1 \
                      WHERE B1.ISBN IN \
                            (SELECT B2.ISBN \
                             FROM BOOK_INFO B2 \
                             WHERE B2.Name LIKE %s OR B2.Publisher LIKE %s OR B2.Author LIKE %s)'
        cursor.execute(SQLCommand, (search, search, search))
        result = cursor.fetchall()
    attritube = ['name', 'image', 'isbn', 'publisher', 'author', 'price', 'date', 'storage', 'content', 'star']
    res = [dict(zip(attritube, r)) for r in result]

    res = mergeAuthor(res)
    return jsonify(res)

@app.route('/login', methods=['POST'])
def login():
    account = request.form.get('account')
    password = request.form.get('password')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * FROM CUSTOMER WHERE Account=%s AND Password=%s'
        cursor.execute(SQLCommand, (account, password))
        result = cursor.fetchall()

    if result:
        return jsonify({'status': True, 'identity': 'customer'})
    else:
        with connect.cursor() as cursor:
            SQLCommand = 'SELECT * FROM MANAGER WHERE Account=%s AND Password=%s'
            cursor.execute(SQLCommand, (account, password))
            result = cursor.fetchall()
        if result:
            return jsonify({'status': True, 'identity': 'manager'})
        else:
            return jsonify({'status': False, 'identity': 'visitor'})

@app.route('/shoppingcart', methods=['POST'])
def shoppingcart():
    account = request.form.get('account')
    isbn = request.form.get('isbn')
    quantity = request.form.get('quantity')
    connect = connectDatabase()
    try:
        with connect.cursor() as cursor:
            SQLCommand = 'INSERT INTO SHOPPING_CART VALUES (%s, %s, %s)'
            cursor.execute(SQLCommand, (account, isbn, quantity))
            connect.commit()
            return jsonify({'status': 'success'})
    except pymysql.err.IntegrityError:
        return jsonify({'status': 'error'})

@app.route('/score', methods=['POST'])
def score():
    account = request.form.get('account')
    isbn = request.form.get('isbn')
    star = request.form.get('star')
    connect = connectDatabase()
    try:
        with connect.cursor() as cursor:
            SQLCommand = 'INSERT INTO SCORE VALUES (%s, %s, %s)'
            cursor.execute(SQLCommand, (account, isbn, star))
            connect.commit()
        return jsonify({'status': 'success'})
    except pymysql.err.IntegrityError:
        with connect.cursor() as cursor:
            SQLCommand = 'UPDATE SCORE SET Star=%s WHERE Account=%s AND ISBN=%s'
            cursor.execute(SQLCommand, (star, account, isbn))
            connect.commit()
        return jsonify({'status': 'success'})

@app.route('/register', methods=['POST'])
def register():
    name = checkNull(request.form.get('name'))
    sex = checkNull(request.form.get('sex'))
    phone = checkNull(request.form.get('phone'))
    birthday = request.form.get('birthday')
    mail = checkNull(request.form.get('mail'))
    account = checkNull(request.form.get('account'))
    password = checkNull(request.form.get('password'))

    birthday = birthday.split('-')
    year = checkNull(birthday[0])
    month = checkNull(birthday[1])
    day = checkNull(birthday[2])

    connect = connectDatabase()
    try:
        with connect.cursor() as cursor:
            SQLCommand = 'INSERT INTO CUSTOMER VALUES (%s, %s, %s, %s, %s, %s, %s)'
            if year and month and day:
                cursor.execute(SQLCommand, (name, sex, phone, datetime.date(int(year), int(month), int(day)), mail, account, password))
            else:
                cursor.execute(SQLCommand, (name, sex, phone, None, mail, account, password))
            connect.commit()
        return jsonify({'status': 'success'})
    except pymysql.err.IntegrityError:
        return jsonify({'status': 'AccError'})
    except pymysql.err.OperationalError:
        return jsonify({'status': 'LengthError'})
    except ValueError:
        return jsonify({'status': 'DateError'})

@app.route('/showShoppingcart', methods=['POST'])
def show():
    account = checkNull(request.form.get('account'))
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT B.Name, B.Image, B.ISBN, B.Publisher, B.Author, B.Price, S.Quantity, B.Storage \
                      FROM SHOPPING_CART S, BOOK_INFO B \
                      WHERE Account=%s AND S.ISBN=B.ISBN'
        cursor.execute(SQLCommand, (account))
        result = cursor.fetchall()
    attritube = ['name', 'image', 'isbn', 'publisher', 'author', 'price', 'quantity', 'storage']
    res = [dict(zip(attritube, r)) for r in result]

    res = mergeAuthor(res)
    return jsonify(res)

@app.route('/deleteShoppingcartBook', methods=['POST'])
def deleteShoppingcartBook():
    account = request.form.get('account')
    isbn = request.form.get('isbn')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'DELETE FROM SHOPPING_CART WHERE Account=%s AND ISBN=%s'
        cursor.execute(SQLCommand, (account, isbn))
        connect.commit()
    return jsonify({'status': 'success'})

@app.route('/useCoupon', methods=['POST'])
def useCoupon():
    coupon = request.form.get('coupon')
    account = request.form.get('account')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * FROM OWN WHERE CNumber=%s AND OwnerAcc=%s'
        cursor.execute(SQLCommand, (coupon, account))
        result = cursor.fetchall()
    if result:
        with connect.cursor() as cursor:
            SQLCommand = 'SELECT `Type`, `Over`, `Discount` FROM COUPON WHERE CNumber=%s'
            cursor.execute(SQLCommand, (coupon))
            result = cursor.fetchall()
        attritube = ['type', 'over', 'discount']
        res = [dict(zip(attritube, r)) for r in result]
        res = res[0]
        res['status'] = 'CouponExist'
        return jsonify(res)
    else:
        return jsonify({'status': 'CouponNotFound'})

@app.route('/getUserInfo', methods=['POST'])
def getUserInfo():
    account = request.form.get('account')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT Name, Sex, Phone, Birthday, Email FROM CUSTOMER WHERE Account=%s'
        cursor.execute(SQLCommand, (account))
        result = cursor.fetchall()
    attritube = ['name', 'sex', 'phone', 'birthday', 'mail']
    res = [dict(zip(attritube, r)) for r in result][0]
    if res['birthday']:
        res['birthday'] = str(res['birthday'])
    return jsonify(res)

@app.route('/submitOrder', methods=['POST'])
def submitOrder():
    # create order number
    connect = connectDatabase()
    try:
        with connect.cursor() as cursor:
            SQLCommand = 'SELECT ONumber FROM `ORDER` ORDER BY ONumber'
            cursor.execute(SQLCommand)
            result = cursor.fetchall()
        number = str(int(result[-1][0][5: ]) + 1)
        orderNum = 'ORDER' + '0'*(5-len(number)) + number
    except:
        orderNum = 'ORDER' + '0'*5

    # create order
    account = request.form.get('account')
    address = request.form.get('address')
    coupon = checkNull(request.form.get('coupon'))
    with connect.cursor() as cursor:
        SQLCommand = 'INSERT INTO `ORDER` VALUE (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(SQLCommand, (orderNum, datetime.date.today(), address, 1, coupon, account, None))
        connect.commit()
    
    # delete coupon
    if coupon:
        try: 
            with connect.cursor() as cursor:
                SQLCommand = 'UPDATE OWN SET Quantity=Quantity-1 WHERE CNumber=%s AND OwnerAcc=%s'
                cursor.execute(SQLCommand, (coupon, account))
                connect.commit()
        except pymysql.err.OperationalError:
            with connect.cursor() as cursor:
                SQLCommand = 'DELETE FROM OWN WHERE CNumber=%s AND OwnerAcc=%s'
                cursor.execute(SQLCommand, (coupon, account))
                connect.commit()

    # add order item & update book storage
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT ISBN, Quantity FROM SHOPPING_CART WHERE Account=%s'
        cursor.execute(SQLCommand, (account))
        result = cursor.fetchall()
    for book in result:
        with connect.cursor() as cursor:
            SQLCommand = 'INSERT INTO HAVE_PRODUCT VALUE (%s, %s, %s)'
            cursor.execute(SQLCommand, (orderNum, book[0], book[1]))
            connect.commit()
        with connect.cursor() as cursor:
            SQLCommand = 'UPDATE BOOK SET Storage=Storage-%s WHERE ISBN=%s'
            cursor.execute(SQLCommand, (book[1], book[0]))
            connect.commit()
    
    # clear shopping cart
    with connect.cursor() as cursor:
        for book in result:
            SQLCommand = 'DELETE FROM SHOPPING_CART WHERE Account=%s'
            cursor.execute(SQLCommand, (account))
            connect.commit()
    return jsonify({'status': 'success'})

@app.route('/getCoupon', methods=['POST'])
def getCoupon():
    account = request.form.get('account')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT C.`CNumber`, `Start_date`, `End_date`, `Type`, `Over`, `Discount`, `Quantity` \
                      FROM COUPON C, OWN O \
                      WHERE C.CNumber=O.CNumber AND OwnerAcc=%s'
        cursor.execute(SQLCommand, (account))
        results = cursor.fetchall()
    attritube = ['number', 'start', 'end', 'type', 'over', 'discount', 'quantity']
    res = []
    for result in results:
        r = dict(zip(attritube, result))
        r['start'] = str(r['start'])
        r['end'] = str(r['end'])
        res.append(r)
    return jsonify(res)

@app.route('/getOrder', methods=['POST'])
def getOrder():
    account = request.form.get('account')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT ONumber, Date, Address, Status, CNumber \
                      FROM `ORDER` \
                      WHERE OwnerAcc=%s \
                      ORDER BY ONumber DESC'
        cursor.execute(SQLCommand, (account))
        results = cursor.fetchall()
    attritube = ['number', 'date', 'address', 'status', 'coupon']
    res = []
    for result in results:
        r = dict(zip(attritube, result))
        r['date'] = str(r['date'])
        res.append(r)
    return jsonify(res)

@app.route('/getOrderBook', methods=['POST'])
def getOrderBook():
    number = request.form.get('ONumber')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT Name, B.ISBN, Price, Quantity \
                      FROM HAVE_PRODUCT H, BOOK B \
                      WHERE H.ONumber=%s AND H.ISBN=B.ISBN'
        cursor.execute(SQLCommand, (number))
        result = cursor.fetchall()
    attritube = ['name', 'isbn', 'price', 'quantity']
    res = [dict(zip(attritube, r)) for r in result]
    return jsonify(res)

@app.route('/getDiscount', methods=['POST'])
def getDiscount():
    number = request.form.get('number')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT Type, Discount FROM COUPON WHERE CNumber=%s'
        cursor.execute(SQLCommand, (number))
        result = cursor.fetchall()[0]
    if result[0] == 1:
        if result[1] < 10:
            return jsonify({'type': 'x', 'discount': result[1]/10})
        else:
            return jsonify({'type': 'x', 'discount': result[1]/100})
    else:
        return jsonify({'type': '-', 'discount': result[1]})

@app.route('/deleteOrder', methods=['POST'])
def deleteOrder():
    number = request.form.get('number')
    coupon = request.form.get('coupon')
    account = request.form.get('account')
    connect = connectDatabase()
    if coupon:
        try:
            with connect.cursor() as cursor:
                SQLCommand = 'INSERT INTO OWN VALUE (%s, %s, 1)'
                cursor.execute(SQLCommand, (coupon, account))
                connect.commit()
        except pymysql.err.IntegrityError:
            with connect.cursor() as cursor:
                SQLCommand = 'UPDATE OWN SET Quantity=Quantity+1 WHERE CNumber=%s AND OwnerAcc=%s'
                cursor.execute(SQLCommand, (coupon, account))
                connect.commit()
    with connect.cursor() as cursor:
        SQLCommand = 'DELETE FROM `ORDER` WHERE ONumber=%s'
        cursor.execute(SQLCommand, (number))
        connect.commit()
    return jsonify({'status': 'success'})

@app.route('/updateInfo', methods=['POST'])
def updateInfo():
    sex = checkNull(request.form.get('sex'))
    phone = checkNull(request.form.get('phone'))
    birthday = request.form.get('birthday')
    mail = checkNull(request.form.get('mail'))
    account = request.form.get('account')
    
    birthday = birthday.split('-')
    year = checkNull(birthday[0])
    month = checkNull(birthday[1])
    day = checkNull(birthday[2])

    connect = connectDatabase()
    try:
        if mail:
            with connect.cursor() as cursor:
                SQLCommand = 'UPDATE CUSTOMER SET Sex=%s, Phone=%s, Birthday=%s, Email=%s WHERE Account=%s'
                if year and month and day:
                    cursor.execute(SQLCommand, (sex, phone, datetime.date(int(year), int(month), int(day)), mail, account))
                else:
                    cursor.execute(SQLCommand, (sex, phone, None, mail, account))
                connect.commit()
        else:
            with connect.cursor() as cursor:
                SQLCommand = 'UPDATE CUSTOMER SET Sex=%s, Phone=%s, Birthday=%s WHERE Account=%s'
                if year and month and day:
                    cursor.execute(SQLCommand, (sex, phone, datetime.date(int(year), int(month), int(day)), account))
                else:
                    cursor.execute(SQLCommand, (sex, phone, None, account))
                connect.commit()
        return jsonify({'status': 'success'})
    except pymysql.err.OperationalError:
        return jsonify({'status': 'InputError'})
    except ValueError:
        return jsonify({'status': 'InputError'})

@app.route('/checkCoupon', methods=['POST'])
def checkCoupon():
    account = request.form.get('account')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT C.CNumber, End_date FROM COUPON C, OWN O WHERE C.CNumber=O.CNumber AND OwnerAcc=%s'
        cursor.execute(SQLCommand, (account))
        coupons = cursor.fetchall()
    for coupon in coupons:
        if coupon[1] and coupon[1] < datetime.date.today():
            with connect.cursor() as cursor:
                SQLCommand = 'DELETE FROM OWN WHERE CNumber=%s'
                cursor.execute(SQLCommand, (coupon[0]))
                connect.commit()
    return jsonify({'status': 'success'})

@app.route('/getAllOrder', methods=['GET'])
def getAllOrder():
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'WITH USE_COUPON AS \
                      (SELECT ONumber, Status, Type, Discount \
                       FROM `ORDER` O LEFT OUTER JOIN `COUPON` C \
                       ON O.CNumber=C.CNumber) \
                      SELECT O.ONumber, O.Date, O.Address, O.OwnerAcc, U.Status, U.Type, U.Discount, SUM(H.Quantity*B.Price) \
                      FROM `ORDER` O, `HAVE_PRODUCT` H, `BOOK` B, `USE_COUPON` U \
                      WHERE O.ONumber=H.ONumber AND H.ISBN=B.ISBN AND U.ONumber=O.ONumber \
                      GROUP BY O.ONumber \
                      ORDER BY O.ONumber DESC'
        cursor.execute(SQLCommand)
        results = cursor.fetchall()
    attritube = ['number', 'date', 'address', 'orderer', 'status', 'type', 'discount', 'total']
    res = []
    for result in results:
        r = dict(zip(attritube, result))
        r['date'] = str(r['date'])
        r['total'] = int(r['total'])
        if r['type'] == 1:
            if r['discount'] < 10:
                r['total'] = round(r['total'] * r['discount'] / 10)
            else:
                r['total'] = round(r['total'] * r['discount'] / 100)
        elif r['type'] == 2:
            r['total'] = r['total'] - r['discount']
        res.append(r)
    return jsonify(res)


@app.route('/updateOrderStatus', methods=['POST'])
def updateOrderStatus():
    number = request.form.get('number')
    status = request.form.get('status')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'UPDATE `ORDER` SET Status=%s WHERE ONumber=%s'
        cursor.execute(SQLCommand, (status, number))
        connect.commit()
    return jsonify({'status': 'success'})

@app.route('/uploadBook', methods=['POST'])
def upload():
    try:
        picture = request.files['picture']
    except:
        picture = None
    name = checkNull(request.form.get('name'))
    isbn = checkNull(request.form.get('isbn'))
    date = checkNull(request.form.get('date'))
    publisher = checkNull(request.form.get('publisher'))
    author = checkNull(request.form.get('author'))
    price = checkNull(request.form.get('price'))
    storage = checkNull(request.form.get('storage'))
    content = checkNull(request.form.get('content'))
    if isbn:
        isbn = isbn.replace(',', '-')
    if content:
        content = content.replace('\n', '<br/>')
    if date:
        date = date.split('-')
    if author:
        author = author.split('/')
    try:
        connect = connectDatabase()
        SQLCommand = 'INSERT INTO BOOK VALUE (%s, %s, %s, %s, %s, %s, %s, %s)'
        if picture:
            picture.save('./BookImage/' + isbn + '.png')
            with connect.cursor() as cursor:
                cursor.execute(SQLCommand, (name, isbn+'.png', isbn, content, publisher, price, datetime.date(int(date[0]), int(date[1]), int(date[2])), storage))
                connect.commit()
        else:
            with connect.cursor() as cursor:
                cursor.execute(SQLCommand, (name, None, isbn, content, publisher, price, datetime.date(int(date[0]), int(date[1]), int(date[2])), storage))
                connect.commit()
        for a in author:
            with connect.cursor() as cursor:
                SQLCommand = 'INSERT INTO AUTHOR VALUE (%s, %s)'
                cursor.execute(SQLCommand, (isbn, a))
                connect.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'error'})
    
@app.route('/deleteBook', methods=['POST'])
def deleteBook():
    isbn = request.form.get('isbn').replace(',', '-')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * FROM BOOK WHERE ISBN=%s'
        cursor.execute(SQLCommand, (isbn))
        results = cursor.fetchall()
    if results:
        with connect.cursor() as cursor:
            SQLCommand = 'DELETE FROM BOOK WHERE ISBN=%s'
            cursor.execute(SQLCommand, (isbn))
            connect.commit()
        os.remove('./BookImage/' + isbn + '.png')
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})

@app.route('/updateBook', methods=['POST'])
def updateBook():
    isbn = request.form.get('isbn').replace(',', '-')
    updateAttribute = request.form.get('attritube')
    updateValue = request.form.get('value')
    connect = connectDatabase()
    with connect.cursor() as cursor:
        SQLCommand = 'SELECT * FROM BOOK WHERE ISBN=%s'
        cursor.execute(SQLCommand, (isbn))
        results = cursor.fetchall()
    if results:
        with connect.cursor() as cursor:
            SQLCommand = 'UPDATE `BOOK` SET ' + updateAttribute + '=%s WHERE ISBN=%s'
            cursor.execute(SQLCommand, (updateValue, isbn))
            connect.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})

@app.route('/getSalesData', methods=['GET'])
def getSalesData():
    connect = connectDatabase()
    yearSales = []
    for i in range(1, 13):
        with connect.cursor() as cursor:
            SQLCommand = 'WITH USE_COUPON AS \
                          (SELECT ONumber, Status, Type, Discount \
                           FROM `ORDER` O LEFT OUTER JOIN `COUPON` C \
                           ON O.CNumber=C.CNumber) \
                          SELECT O.ONumber, U.Type, U.Discount, SUM(H.Quantity*B.Price) \
                          FROM `ORDER` O, `HAVE_PRODUCT` H, `BOOK` B, `USE_COUPON` U \
                          WHERE O.ONumber=H.ONumber AND H.ISBN=B.ISBN AND U.ONumber=O.ONumber AND U.Status=3 AND O.Date>=%s AND O.Date<%s\
                          GROUP BY O.ONumber'
            if i == 12:
                cursor.execute(SQLCommand, (datetime.date(2020, 12, 1), datetime.date(2021, 1, 1)))
            else:
                cursor.execute(SQLCommand, (datetime.date(2020, i, 1), datetime.date(2020, i+1, 1)))
            results = cursor.fetchall()
        total = 0
        for r in results:
            r = list(r)
            r[3] = int(r[3])
            if r[1] == 1:
                if r[2] < 10:
                    total += round(r[3] * r[2] / 10)
                else:
                    total += round(r[3] * r[2] / 100)
            elif r[1] == 2:
                total += r[3] - r[2]
            else:
                total += r[3]
        yearSales.append(total)
    return jsonify(yearSales)

if __name__ == "__main__" :
    app.run(host='127.0.0.1', port=5000)
