import sqlite3 

def create_table():
    connect = sqlite3.connect('predictionDatabase.db')
    cursor = connect.cursor()

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS predict_table (  
                   id INTEGER PRIMARY KEY,
                   gender INTEGER, 
                   age INTEGER,
                   department_code INTEGER,
                   years_exp INTEGER, 
                   tenure INTEGER,
                   gross FLOAT) ''')
    connect.commit()
    connect.close()


def append_prediction(id, gender, age, department_code, years_exp, tenure, gross):
    connect = sqlite3.connect('predictionDatabase.db')
    cursor = connect.cursor()
    cursor.execute(' INSERT INTO predict_table (id, gender, age, department_code, years_exp, tenure, gross) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                   (id, gender, age, department_code, years_exp, tenure, gross))
    connect.commit()
    connect.close()

def search_prediction(query):
    connect = sqlite3.connect('predictionDatabase.db')
    cursor = connect.cursor()
    cursor.execute('SELECT gross FROM predict_table WHERE id = ?', (query,))
    gross = cursor.fetchone()
    connect.close()
    return gross

def id_exists(id):
    connect = sqlite3.connect('predictionDatabase.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM predict_table WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0 

create_table()