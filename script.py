from bottle import run, route, template, request, post, get, redirect
import csv
import os
import sqlite3
import time


@route('/', method='GET')
def getform():
    return template('load')


@route('/', method='POST')
def loadform():

    ''' get and save csv file'''
    file = request.files.get("file")
    try:
        file.save("./files")
    except IOError:
        os.remove("./files/{}".format(file.filename))
        file.save("./files")


    ''' open csv file and create name for database'''
    global file_name, db_name
    file_name = ("./files/{}".format(file.filename))
    f = open(file_name, 'r')
    next(f)
    csv_file = csv.reader(f)
    f_name = os.path.basename(file_name)
    db_name = f_name.split('.')[1]+str(int(time.time()))


    ''' create db and add table into db '''     
    db = sqlite3.connect('database.db') 
    db.execute('''CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    staff INTEGER(10), 
                                    product INTEGER(6), 
                                    qti INTEGER(4), 
                                    data char(30))'''.format(db_name))  
    for row in csv_file:
        db.execute('''INSERT INTO ''' + db_name + ''' (staff, product, qti, data) 
                                VALUES ('{}','{}','{}','{}' )'''.format(row[0], row[1], row[2], row[3]))    
    db.commit()
    db.close()
    redirect('/table')



@route('/table')
def index():
    db = sqlite3.connect('database.db')
    res = db.execute(''' SELECT staff, product, qti FROM {} '''.format(db_name))
    result = res.fetchall()
    result.sort()
    new_list = []
    c = []
    
    for a in range(len(result)-1):
        result[a] = list(result[a])
        c.append(result[a][2])
        if result[a][0] != result[a+1][0]:
            result[a][2] = sum(c)
            new_list.append(result[a]) 
            c = [] 

    return template('table', result=result, new_list=new_list)
   
if __name__ == "__main__":
    run(debug=True, reloader=True)

