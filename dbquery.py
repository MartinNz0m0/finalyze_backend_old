import mysql.connector
from datetime import date, datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def db_insert_prepared(query, values):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor(prepared=True)
        mycursor.execute(query, values)
        mydb.commit()

        return 'ok'
    except mysql.connector.Error as error:
        return error


def db_select(query, values):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor(prepared=True)
        mycursor.execute(query, values)
        myresult = mycursor.fetchall()
        return myresult
    except mysql.connector.Error as error:
        return error


def get_file_names(user, stttype):

    query = "SELECT * FROM data WHERE name = %s and statement_type = %s"
    values = (user, stttype)
    result = db_select(query, values)

    file = []
    for x in result:
        file.append(x[2])

    return file


def insertcat(userinp, details, fuliza_dets, online_dets, user, sttype):
    currdate = date.today()

    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor()
        # Prepare the SQL statement with placeholders
        sql = "INSERT INTO usermodel (name, details, category, date_added, statement_type) VALUES (%s, %s, %s, %s, %s)"

        # Prepare the values to be inserted
        values = [
            (user, details, userinp, currdate, sttype),
            (user, fuliza_dets, userinp, currdate, sttype)
        ]

        if online_dets:
            values.append((user, online_dets, userinp, currdate, sttype))

        # Execute the prepared statement with values
        cursor = mydb.cursor(prepared=True)
        cursor.executemany(sql, values)
        mydb.commit()

        jibu = []
        mycursor.execute(
            "SELECT * FROM usermodel where statement_type = 'mpesa'")
        myresult = mycursor.fetchall()
        for x in myresult:
            jibu.append(x[2])
        return jibu

    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def insertmpesacosts(details, user):
    userinp = 'Mpesa Transcation Costs'
    currdate = date.today()
    sttype = 'mpesa'
    query = "INSERT INTO usermodel (name, details, category, date_added, statement_type) VALUES (%s, %s, %s, %s, %s)"
    values = (user, details, userinp, currdate, sttype)
    res = db_insert_prepared(query, values)
    return res


def insertcoopcat(userinp, details, user, sttype):
    currdate = date.today()

    try:
        sql = "INSERT INTO usermodel (name, details, category, date_added, statement_type) VALUES (%s, %s, %s, %s, %s)"

        values = (user, details, userinp, currdate, sttype)
        db_insert_prepared(sql, values)

        jibu = []
        query = "SELECT * FROM usermodel where statement_type = %s"
        val = (sttype,)

        myresult = db_select(query, val)
        for x in myresult:
            jibu.append(x[2])
        return jibu

    except:
        print('error')


def checkcat(details, user):
    sttype = 'mpesa'
    sql = f"SELECT * FROM usermodel where name = %s and details = %s and statement_type = %s"
    values = (user, details, sttype)
    myresult = db_select(sql, values)
    jibu = []
    for x in myresult:
        jibu.append(x[2])
    return jibu


def checkcoopcat(details, user):
    sttype = 'coop'
    jibu = []
    sql = f"SELECT * FROM usermodel where name = %s and details = %s and statement_type = %s"
    values = (user, details, sttype)
    myresult = db_select(sql, values)
    jibu = []
    for x in myresult:
        jibu.append(x[2])
    return jibu


def checkequitycat(details, user):
    sttype = 'equity'
    sql = f"SELECT * FROM usermodel where name = %s and details = %s and statement_type = %s"
    values = (user, details, sttype)
    res = db_select(sql, values)
    jibu = []
    if res:
        for x in res:
            jibu.append(x[2])
        return jibu
    else:
        return 'error'


def getcat(user, stttype):
    sql = f"SELECT * FROM usermodel where name = %s and statement_type = %s"
    val = (user, stttype)
    result = db_select(sql, val)
    final_res = []
    for x in result:
        obj = {
            'details': x[2],
            'category': x[3],
        }
        final_res.append(obj)
    return final_res


def editcategory(userinp, details, user, sttype, newbudget):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor(prepared=True)
        # Prepare the SQL statement with placeholders
        sql = f"UPDATE usermodel SET category = %s WHERE details = '{details}' and name = '{user}' and statement_type = '{sttype}'"
        val = (userinp,)
        # Execute the prepared statement with values
        mycursor.execute(sql, val)
        mydb.commit()
        if newbudget:
            sqlbudget = f"UPDATE usermodel SET budget = %s WHERE category = '{userinp}' and name = '{user}' and statement_type = '{sttype}'"
            mycursor.execute(sqlbudget, (newbudget,))
            mydb.commit()
        else:
            print('no budget')
        jibu = []
        mycursor.execute(
            f"SELECT * FROM usermodel where statement_type = '{sttype}' and name = '{user}'")
        myresult = mycursor.fetchall()
        return myresult
    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def deletecat(details, user, sttype):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor()
        sql = f"DELETE FROM usermodel WHERE details = '{details}' and name = '{user}' and statement_type = '{sttype}'"
        mycursor.execute(sql)
        mydb.commit()

        jibu = []
        mycursor.execute(f"SELECT * FROM usermodel where name = '{user}'")
        myresult = mycursor.fetchall()
        return myresult
    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def updatebudget(user, budget, category, sttype, priority):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor(prepared=True)
        if priority:
            if budget:
                sql = f"UPDATE usermodel SET budget = %s, priority = %s WHERE category = '{category}' and name = '{user}'"
                val = (budget, priority)
                mycursor.execute(sql, val)
                mydb.commit()
            else:
                sql = f"UPDATE usermodel SET priority = %s WHERE category = '{category}' and name = '{user}'"
                val = (priority,)
                mycursor.execute(sql, val)
                mydb.commit()
        else:
            sql = f"UPDATE usermodel SET budget = %s WHERE category = '{category}' and name = '{user}'"
            val = (budget,)
            mycursor.execute(sql, val)
            mydb.commit()
            # get response
            print(mycursor.rowcount, "record(s) affected")

        jibu = []
        mycursor.execute(
            f"SELECT * FROM usermodel where statement_type = '{sttype}' and name = '{user}'")
        myresult = mycursor.fetchall()
        return myresult
    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def getbudget(user, cat):
    try:
        sql = f"SELECT * FROM usermodel where name = %s and category = %s"
        val = (user, cat)
        myresult = db_select(sql, val)
        # return only one value
        return myresult[0][6]
    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def getlateststatement(user):
    try:
        sql = f"SELECT * FROM data where name = %s"
        val = (user,)
        myresult = db_select(sql, val)

        currdate = date.today()
        # check date and get that curr date is greater than date in db by one month
        for x in myresult:
            startdate = x[3].split(' ')[0]
            enddate = x[3].split(' ')[2]
            # if startdate is only 2 digits change object

            if len(startdate) == 2:
                date_str = f"{x[3].split(' ')[0]} {x[3].split(' ')[1]} {x[3].split(' ')[2]}"
                enddatestr = f"{x[3].split(' ')[4]} {x[3].split(' ')[5]} {x[3].split(' ')[6]}"
                startdate = datetime.strptime(
                    date_str, '%d %B %Y').strftime('%Y-%m-%d')
                enddate = datetime.strptime(
                    enddatestr, '%d %B %Y').strftime('%Y-%m-%d')

            dateobj = datetime.strptime(startdate, '%Y-%m-%d').date()
            enddateobj = datetime.strptime(enddate, '%Y-%m-%d').date()
            # first check that the two dates are less than 35 days apart
            if enddateobj - dateobj > timedelta(days=35):

                return 'no statement'
            # check that end date is not older than 35 days
            diff = currdate - enddateobj
            if diff < timedelta(days=35):

                return x[2], x[5]
            else:
                pass
        return 'no statement'
    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def checkcoopfiledaterange(user, file, date):
    sttype = 'coop'
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor()
        jibu = []
        mycursor.execute(
            f"SELECT * FROM data where statement_type = '{sttype}' and name = '{user}' and pdf_name = '{file}'")
        myresult = mycursor.fetchall()
        if myresult[0][3] == None:
            # insert date
            sql = f"UPDATE data SET date = '{date}' WHERE statement_type = '{sttype}' and name = '{user}' and pdf_name = '{file}'"
            mycursor.execute(sql)
            mydb.commit()
            return 'ok'
        else:
            return 'already inserted'
    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def checkequityfiledaterange(user, file, date):
    sttype = 'equity'
    sql = f"SELECT * FROM data where statement_type = %s and name = %s and pdf_name = %s"
    val = (sttype, user, file)
    dbreq = db_select(sql, val)
    if dbreq[0][3] == None:
        # insert date
        sql = f"UPDATE data SET date = %s WHERE statement_type = %s and name = %s and pdf_name = %s"
        val = (date, sttype, user, file)
        db_insert_prepared(sql, val)
        return 'ok'
    else:
        return 'already inserted'


def getallcategories(user):
    sql = f"SELECT * FROM usermodel where name = %s"
    val = (user,)
    result = db_select(sql, val)
    return result


def checkcoopcosts(user):
    sttype = 'coop'
    try:
        sql = f"SELECT * FROM usermodel where name = %s and statement_type = %s"
        val = (user, sttype)
        myresult = db_select(sql, val)
        for x in myresult:
            jibu.append(x[2])
        return jibu
    except mysql.connector.Error as error:
        print("Error: {}".format(error))
        return 'Error'


def checkequitycosts(user):
    sttype = 'equity'
    query = f"SELECT * FROM usermodel where name = %s and statement_type = %s"
    val = (user, sttype)
    dbreq = db_select(query, val)
    jibu = []
    for x in dbreq:
        jibu.append(x[2])
    return jibu


def insertcooptcosts(user, details):
    currdate = date.today()
    statement_type = 'coop'
    userinp = 'Transcation Costs'

    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="finalyze"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO usermodel (name, details, category, date_added, statement_type) VALUES (%s, %s, %s, %s, %s)"

        values = (user, details, userinp, currdate, statement_type)

        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql, values)
        mydb.commit()
        jibu = []
        mycursor.execute(
            f"SELECT * FROM usermodel where name = '{user}' and statement_type = '{statement_type}'")
        myresult = mycursor.fetchall()
        for x in myresult:
            jibu.append(x[2])

        return jibu

    except mysql.connector.Error as error:
        print("Error: {}".format(error))


def addequitycosts(user, details):
    currdate = date.today()
    statement_type = 'equity'
    userinp = 'Transcation Costs'

    query = "INSERT INTO usermodel (name, details, category, date_added, statement_type) VALUES (%s, %s, %s, %s, %s)"
    val = (user, details, userinp, currdate, statement_type)
    try:
        db_insert_prepared(query, val)
        return 'ok'
    except mysql.connector.Error as error:
        print("Error: {}".format(error))
        return 'Error', error
