import unittest
import sqlite3
import json
import os

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_employees_table(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Employees")
    cur.execute("CREATE TABLE Employees (employee_id INTEGER PRIMARY KEY, 
first_name TEXT, last_name TEXT, hire_date TEXT, job_id INTEGER, salary INTEGER)")
    conn.commit()

def add_employee(filename, cur, conn):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    json_data = json.loads(file_data)
    f.close()

    for i in json_data: 
        cur.execute("INSERT INTO Employees (employee_id, first_name, last_name, hire_date, job_id, salary) VALUES (?,?,?,?,?,?)", (i["employee_id"],i["first_name"],i["last_name"],i["hire_date"],i["job_id"],i["salary"]))
        conn.commit()   

def job_and_hire_date(cur, conn):
    cur.execute("""
    SELECT Employees.hire_date, Jobs.job_title FROM Employees JOIN Jobs ON Jobs.job_id = Employees.job_id;"""
    )
    data = cur.fetchall()
    sorted_data = sorted(data, key=lambda x: x[0])
    return sorted_data[0][1]

def problematic_salary(cur, conn): 
    cur.execute("""
    SELECT Employees.first_name, Employees.last_name, Employees.salary, Jobs.min_salary, Jobs.max_salar FROM Employees JOIN Jobs ON Jobs.job_id = Employees.job_id WHERE Employees.salary < Jobs.min_salary OR Employees.salary > Jobs.max_salary"""
    )
    data = cur.fetchall()
    name_list = [(i[0],i[1]) for i in data] 
    return name_list
def main():
    cur, conn = setUpDatabase('HR.db')
    create_employees_table(cur, conn)
    
    add_employee("employee.json",cur, conn)
    test = job_and_hire_date(cur,conn)
    print(test)
    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)
    
    
if __name__ == "__main__":
    main()