import mysql.connector as sql

class Database:
    def __init__(self):
        self.conn = sql.connect(
            host = "127.0.0.1",
            port = 3306,
            user = "root",
            password = "Tushar@2000",
            database = "loan_db"
        )
        self.cursor = self.conn.cursor()
        print("Connection build ")
        
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS predictions(
                            Gender VARCHAR(10),
                            Married VARCHAR(10),
                            Dependents VARCHAR(10),
                            Education VARCHAR(20),
                            Self_Employed VARCHAR(10),
                            Loan_Amount FLOAT ,
                            Loan_Amount_Term INT,
                            Credit_History FLOAT,
                            Property_Area VARCHAR(20),
                            Family_Income FLOAT ,
                            Loan_Status VARCHAR(10))""")
        
    def save_predictions(self, Gender, Married, Dependents, Education, Self_Employed, 
                               Loan_Amount, Loan_Amount_Term, Credit_History, Property_Area, 
                                Family_Income, Loan_Status ):
        
                query = """
                        INSERT INTO predictions(Gender, Married, Dependents, Education, Self_Employed, 
                                    Loan_Amount, Loan_Amount_Term, Credit_History, Property_Area, 
                                        Family_Income, Loan_Status)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                
                self.cursor.execute(query,(Gender, Married, Dependents, Education, Self_Employed, 
                                    Loan_Amount, Loan_Amount_Term, Credit_History, Property_Area, 
                                        Family_Income, Loan_Status))
                self.conn.commit()