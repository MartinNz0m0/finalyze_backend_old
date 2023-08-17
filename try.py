import pandas as pd
import numpy as np
import mysql.connector
from flask import *
from flask_cors import CORS
import datetime
import dbquery
import searchfunc
import jwt
import userinput
import mpesa_funcs
import redis_funcs
import bank
import auth
import msgreader
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
                if redis_funcs.redis_exists(user, f'usermodel{sttype}{num}'):
                    response = redis_funcs.redis_get(user, f'usermodel{sttype}{num}')
                    response = json.loads(response)
                    print('got usermodel from redis')
                else:
                    response = mpesa_funcs.userinput(user, num, sttype)
                    redis_funcs.redis_set(user, f'usermodel{sttype}{num}', json.dumps(response))
                    print('got usermodel from db')
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
                res = mpesa_funcs.usersubmit(userinp, details, user, sttype)
                # redis_funcs.redis_del(user, 'allcats')
                # redis_funcs.redis_del(user, 'dashdata')
                # redis_funcs.redis_del(user, 'categoryanalmpesa')
                redis_funcs.redis_del_all(user)
                for i in range(1, 6):
                    redis_funcs.redis_del(user, f'usermodelmpesa{i}')
                return jsonify(res)
            else:
                res = dbquery.insertcoopcat(userinp, details, user, sttype)
                return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/getallcats', methods=['POST'])
def getallcats():
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
            if redis_funcs.redis_exists(user, 'allcats'):
                res = redis_funcs.redis_get(user, 'allcats')
                res = json.loads(res)
            else:
                res = dbquery.getallcategories(user)
                redis_funcs.redis_set(user, 'allcats', json.dumps(res))
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
            redis_funcs.redis_del_all(user)
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/lateststatement', methods=['POST'])
def lateststatement(): #TODO: abandon this function??
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
                    resp = mpesa_funcs.categoryanal(res[0], user)
                    response = mpesa_funcs.mpesa_time_analysis(res[0])
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
            if redis_funcs.redis_exists(user, 'dashdata'):
                res = redis_funcs.redis_get(user, 'dashdata')
                res = json.loads(res)
                return jsonify(res)
            if redis_funcs.redis_exists(user, 'allcats'):
                cats = redis_funcs.redis_get(user, 'allcats')
                cats = json.loads(cats)
                print('getting cats from redis')
            else:
                print('getting cats from db')
                cats = dbquery.getallcategories(user) #TODO: get from redis
                redis_funcs.redis_set(user, 'allcats', json.dumps(cats))
            # create empy array for categories
            category = []
            # create empy array for total budget
            budget = []
            for x in cats:
                category.append(x[3])
                # push budget as well
                # if x[6]:
                #     budget.append(x[6])
                #     print(x[6])
            # remove duplicates for category array
            category = list(dict.fromkeys(category))
            # add sum for budget array
            for x in category:
                bud = dbquery.getbudget(user, x) #TODO: dont query db for each category
                if bud:
                    budget.append(bud)
            totalbudget = 0
            for x in budget:
                totalbudget += int(x)           
            ind = bank.overspend_index(user) 
            dash_list = [len(category), totalbudget, round(ind, 1)]
            redis_funcs.redis_set(user, 'dashdata', json.dumps(dash_list))         
            return [len(category), totalbudget, round(ind, 1)]
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/deletecat', methods=['POST'])
def deletecat():
    auth_header = request.headers.get('Authorization')
    details = request.json.get('det')
    sttype = request.json.get('sttype')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jibu = auth.jwt_verify(auth_header)
        if jibu == 'invalid':
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            user = jibu[0]
            res = dbquery.deletecat(details, user, sttype)
            redis_funcs.redis_del_all(user)
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
            redis_funcs.redis_del_all(user)
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
                if redis_funcs.redis_exists(user, 'categoryanalmpesa'):
                    res = redis_funcs.redis_get(user, 'categoryanalmpesa')
                    res = json.loads(res)
                else:
                    res = mpesa_funcs.categoryanal(file, user) #TODO: get from redis
                    redis_funcs.redis_set(user, 'categoryanalmpesa', json.dumps(res))
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
            res = mpesa_funcs.categoryanalall(user) #TODO: get from redis
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
            res = bank.groupbycoop(user, num) #TODO: get from redis
            return jsonify(res)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/conequity', methods=['POST'])
def conequity():
    file = request.json.get('name')
    pdflock = request.json.get('pdflock')
    pdfpwd = request.json.get('pdfpwd')
    try:
        bank.equityconvert(file, pdflock, pdfpwd)
        return jsonify({'message': 'success'})
    except:
        return jsonify({'message': 'failed'})

@app.route('/msgreceive', methods=['POST'])
def msgreceive():
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
            msg = request.json.get('msg')
            res = msgreader.mpesa_csvwriter(f"mpesa_{user}.csv", msg, user)
            if res == "ok":
                return jsonify("ok")
            else:
                return jsonify("ok") # TODO: change this to failed
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/lastsync', methods=['POST'])
def lastsync():
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.startswith('Bearer '):
        jibu = auth.jwt_verify(auth_header)
        if jibu == 'invalid':
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            user = jibu[0]
            res = dbquery.check_last_sync(user) #TODO: get from redis
            if res == 'no sync':
                return jsonify(res)
            return jsonify(res.strftime("%Y-%m-%d %H:%M:%S.000Z"))

if __name__ == '__main__':
    app.run(port=8001)






    



# print(group.tail())   

   
# replace the details info with proper info so it does not confuse, business payment is example 

# get count for fuliza transactions



# get completed time and group transactions by date

# calculate the variance from the mean? for each group