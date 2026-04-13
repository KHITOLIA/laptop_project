import mysql.connector as sql
import os

class Database:
    def __init__(self):
        self.conn = sql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            password = 'Tushar@2000',
            database = 'insurance_db'
        )
        self.cursor = self.conn.cursor()
        print("Database connection established.")

        # step 2: create table for predictions
        self.cursor.execute('''create table if not exists predictions (
                            id int auto_increment primary key,
                            age int,
                            sex varchar(20),
                            bmi float,
                            children int,
                            smoker varchar(20),
                            region varchar(20),
                            prediction float)''')
    def save_predictions(self, age, sex, bmi, children, smoker, region, prediction):
        query = "insert into predictions (age, sex, bmi, children, smoker, region, prediction) values (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (age, sex, bmi, children, smoker, region, prediction))
        self.conn.commit()
        print("Prediction saved to database.")
        
obj = Database()