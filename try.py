import pandas as pd
import numpy as np
import mysql.connector
import dbquery
from flask import *
from flask_cors import CORS
import searchfunc
import jwt
import userinput
import bank
import auth
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Py is running'

@app.route('/search', methods=['POST'])
def searchfun():
    query = request.json.get('query')
    sttype = request.json.get('stttype')
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
    # Extract the JWT from the Authorization header
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        
        # Decode the JWT to get the user
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        
        print(f'Authenticated user: {user}')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            if request.json.get('filename'):
                #run searchone func
                searchres = searchfunc.searchone(query.upper(), user ,request.json.get('filename'))
                return jsonify(searchres)
            else:
                if sttype == 'mpesa':
                    searchres = searchfunc.searchfunc(query.upper(), user, sttype)
                    return jsonify(searchres)
                elif sttype == 'coop':
                    searchres = searchfunc.coopsearchfunc(query.upper(), user, sttype)
                    return jsonify(searchres)
                elif sttype == 'equity':
                    searchres = searchfunc.equitysearchfunc(query.upper(), user, sttype)
                    return jsonify(searchres)
                else:
                    return 'nothing happened'
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
  
@app.route('/usermodel', methods=['POST'])
def usermodel():
    auth_header = request.headers.get('Authorization')
    num = request.json.get('itemnumber')
    sttype = request.json.get('stttype')
    if auth_header is not None and auth_header.startswith('Bearer '):
    # Extract the JWT from the Authorization header
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        
        # Decode the JWT to get the user
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            if sttype == 'mpesa':
                response = userinput.userinput(user, num, sttype)
                return jsonify(response)
            elif sttype == 'coop':
                response = bank.groupbycoop(user, num, sttype)
                return jsonify(response)
            elif sttype == 'equity':
                response = bank.equitygroupby(user, num, sttype)
                return jsonify(response)
            else:
                return 'nothing happened'
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@app.route('/usersubmit', methods=['POST'])
def insertcat():
    userinp = request.json.get('userinput')
    details = request.json.get('det')
    sttype = request.json.get('stttype')
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
    # Extract the JWT from the Authorization header
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        
        # Decode the JWT to get the user
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            if sttype == 'mpesa':
                res = userinput.usersubmit(userinp, details, user, sttype)
                return jsonify(res)
            else:
                res = dbquery.insertcoopcat(userinp, details, user, sttype)
                return jsonify(res)
            

    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/getallcats', methods=['POST'])
def getallcat():
    auth_header = request.headers.get('Authorization')
    removeduplicates = request.json.get('removeduplicates')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            res = dbquery.getallcategories(user)
            if removeduplicates == True:
                finalres = []

                for i in res:
                    if i[3] not in [arr[3] for arr in finalres]:
                        finalres.append(i)
                return jsonify(finalres)
            else:
                return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/editcat', methods=['POST'])
def editcat():
    auth_header = request.headers.get('Authorization')
    userinp = request.json.get('newcat')
    details = request.json.get('det')
    sttype = request.json.get('sttype')
    newbudget = request.json.get('newbudget')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            res = dbquery.editcategory(userinp, details, user, sttype, newbudget)
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/lateststatement', methods=['POST'])
def lateststatement():
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jibu = auth.jwt_verify(auth_header)
        if jibu == 'invalid':
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            user = jibu[0]
            res = dbquery.getlateststatement(user)
            if res == 'no statement':
                return jsonify(res)
            else:
                if res[1] == 'mpesa':
                    resp = userinput.categoryanal(res[0], user)
                    response = userinput.mpesa_time_analysis(res[0])
                    return jsonify([resp, response])
                elif res[1] == 'coop':
                    resp = bank.coopquickanal('demo-coop', user)
                    response = bank.coop_time_analysis('demo-coop')
                    return jsonify([resp, response])
                elif res[1] == 'equity':
                    resp = bank.equityquickanal('demo-equity', user)
                    response = bank.equity_time_analysis('demo-equity')
                    return jsonify([resp, response])
                else:
                    return 'nothing happened'
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# dashbaord data, get all categories, get total budget
@app.route('/dashdata', methods=['POST']) 
def dashdata():
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jibu = auth.jwt_verify(auth_header)
        if jibu == 'invalid':
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            user = jibu[0]
            cats = dbquery.getallcategories(user)
            # create empy array for categories
            category = []
            # create empy array for total budget
            budget = []
            for x in cats:
                category.append(x[3])
                
            # remove duplicates for category array
            category = list(dict.fromkeys(category))
            # add sum for budget array
            for x in category:
                bud = dbquery.getbudget(user, x)
                if bud:
                    budget.append(bud)
            totalbudget = 0
            for x in budget:
                totalbudget += int(x)
                
            ind = bank.overspend_index(user)          
            return [len(category), totalbudget, round(ind, 1)]

@app.route('/deletecat', methods=['POST'])
def deletecat():
    auth_header = request.headers.get('Authorization')
    details = request.json.get('det')
    sttype = request.json.get('sttype')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            res = dbquery.deletecat(details, user, sttype)
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/addbudget', methods=['POST'])
def addbudget():
    auth_header = request.headers.get('Authorization')
    budget = request.json.get('budget')
    sttype = request.json.get('sttype')
    category = request.json.get('cat')
    priority = request.json.get('priority')
    print(priority)
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            res = dbquery.updatebudget(user, budget, category, sttype, priority)
            # remove duplicates from the list if category is the same
     
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
 


@app.route('/getcat', methods=['POST'])
def getcat():
    file = request.json.get('pdf_name')
    sttype = request.json.get('statement_type')
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            if sttype == 'mpesa':
                res = userinput.categoryanal(file, user)
                return jsonify(res)
            elif sttype == 'coop':
                res = bank.coopquickanal(file, user)
                return jsonify(res)
            elif sttype == 'equity':
                res = bank.equityquickanal(file, user)
            else:
                return 'nothing happened'
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/getcatall', methods=['POST'])
def getcatall():
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            res = userinput.categoryanalall(user)
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/coopgroup', methods=['POST'])
def coopgroup():
    num = request.json.get('itemnumber')
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]
        secret_key = os.getenv("SECRET")
        decoded_jwt = jwt.decode(jwt_token, secret_key ,algorithms=['HS256'])
        user = decoded_jwt.get('name')
        role = decoded_jwt.get('role')
        if user is None:
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            res = bank.groupbycoop(user, num)
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=8001)






    



# print(group.tail())   

   
# replace the details info with proper info so it does not confuse, business payment is example 

# get count for fuliza transactions



# get completed time and group transactions by date

# calculate the variance from the mean? for each group