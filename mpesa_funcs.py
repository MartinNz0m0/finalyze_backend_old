import pandas as pd
import dbquery
import datetime

def userinput(user, num, stttype):
    file = dbquery.get_file_names(user, stttype)
    #TODO: replace file with universal file
    userres = []
    # arrays for collecting similar transactions
    customer = []
    paybillarr = []
    tillarr = []
    airtimearr = []
    for x in file:
        # df = pd.read_csv(f'./uploads/{x}.csv')
        # df.fillna(0, inplace=True)
        # df.replace('\r', ' ', regex=True, inplace=True)

        # remw = df.loc[df.Withdrawn != "Withdrawn"].copy()
        # # remw = remw.reset_index(drop=True)
        # remw['Withdrawn'] = remw.Withdrawn.str.replace("-", "", regex=False)
        # remw['Withdrawn'] = remw.Withdrawn.str.replace(",", "", regex=False)
        # remw['Withdrawn'] = remw['Withdrawn'].fillna(0).astype(float)
        # remw['Paid In'] = remw['Paid In'].str.replace(",", "", regex=False)
        # remw['Paid In'] = remw['Paid In'].fillna(0).astype(float)
        # convert to int
        remw = mpesa_df(x)
        # groupings the
        group = remw.groupby('Details')
        # module for prompting user input
        # from here you can filter according to the size of the group
        largest = group['Details'].agg(['count'])
        above_10 = largest[largest['count'] >= int(num)]
        for name, item in above_10.iterrows():
            details = group.get_group(name)['Details'].drop_duplicates()
            userres.append(item.to_list())

            # check details to makesure it is not a transcation charge
            customertransfer = details.str.contains(
                'Send money|Send money fuliza')
            paybill = details.str.contains('Pay Bill to|Pay Bill fuliza')
            till = details.str.contains(
                'Buy goods|Buy goods fuliza')
            airtimetransfer = details.str.contains(
                'Buy airtime')

            # prompt user to identify the transactions
            final = details[customertransfer].to_list()
            finalpbill = details[paybill].to_list()
            finaltill = details[till].to_list()
            finalairtime = details[airtimetransfer].to_list()
            customer.append(final)
            paybillarr.append(finalpbill)
            tillarr.append(finaltill)
            airtimearr.append(finalairtime)

    # flatten arrays before removing duplicates
    flatenlist = [item for sublist in customer for item in sublist]
    flatentill = [item for sublist in tillarr for item in sublist]
    flatenpbill = [item for sublist in paybillarr for item in sublist]
    flatenairtime = [item for sublist in airtimearr for item in sublist]
    # remove duplicates
    cleanlist1 = list(dict.fromkeys(flatenlist))
    cleanlist2 = list(dict.fromkeys(flatentill))
    cleanlist3 = list(dict.fromkeys(flatenpbill))
    cleanlist4 = list(dict.fromkeys(flatenairtime))
    # remove details found in database
    # create final list to be returned
    final = []
    final2 = []
    final3 = []
    for x in cleanlist1:
        # check for fuliza as well
        if 'Send money fuliza' in x:
            x2 = x.replace('Send money fuliza',
                           'Send money')
        elif 'Send money' in x:
            x2 = x.replace('Send money',
                           'Send money fuliza')
        else:
            pass

        dbreq = dbquery.checkcat(x, user)
        dbreq2 = dbquery.checkcat(x2, user)
        if x not in dbreq:
            final.append(x)
        if not x2 in dbreq2 and x2 in cleanlist1:
            final.append(x2)
    # for airtime
    for x in cleanlist4:
        # check for fuliza as well
        if 'Buy airtime fuliza' in x:
            x2 = x.replace('Buy airtime fuliza',
                           'Buy airtime')
        elif 'Buy airtime' in x:
            x2 = x.replace('Buy airtime',
                           'Buy airtime fuliza')
        else:
            pass

        dbreq = dbquery.checkcat(x, user)
        dbreq2 = dbquery.checkcat(x2, user)
        if x not in dbreq:
            final.append(x)
        if not x2 in dbreq2 and x2 in cleanlist4:
            final.append(x2)
    for x in cleanlist2:
        # remove online word from paybill online
        if 'Online' in x:
            x = x.replace('Online', '')
        # check for fuliza as well
        if 'Buy goods fuliza' in x:
            x2 = x.replace('Buy goods fuliza',
                           'Buy goods')
        elif 'Buy goods' in x:
            x2 = x.replace('Buy goods',
                           'Buy goods fuliza')

        dbreq = dbquery.checkcat(x, user)
        dbreq2 = dbquery.checkcat(x2, user)
        if x not in dbreq:
            final2.append(x)
        if x2 not in dbreq2 and x2 in cleanlist2:
            final2.append(x2)
    for x in cleanlist3:
        # remove online word from paybill online
        if 'Online' in x:
            x = x.replace('Online', '')
        # check for fuliza as well
        if 'Pay Bill fuliza' in x:
            x2 = x.replace('Pay Bill fuliza', 'Pay Bill to')
        elif 'Pay Bill to' in x:
            x2 = x.replace('Pay Bill to', 'Pay Bill fuliza')

        dbreq = dbquery.checkcat(x, user)
        dbreq2 = dbquery.checkcat(x2, user)
        if x not in dbreq:
            final3.append(x)
        if x2 not in dbreq2 and x2 in cleanlist3:
            final3.append(x2)
    return final, final2, final3
    # sort = df.sort_values(by=['Withdrawn'], ascending=False)

# get user imput for categorizing transactions


def usersubmit(userinp, details, user, sttype, budget):
    online_dets = ''
    if 'Send money' in details:
        # add one for fuliza as well
        fuliza_dets = details.replace(
            'Send money', 'Send money fuliza')
    elif 'Send money fuliza' in details:
        fuliza_dets = details.replace(
            'Send money fuliza', 'Send money')
    elif 'Pay Bill to' in details:
        fuliza_dets = details.replace(
            'Pay Bill to', 'Pay Bill fuliza')
    elif 'Pay Bill fuliza' in details:
        fuliza_dets = details.replace(
            'Pay Bill fuliza', 'Pay Bill to')
    elif 'Buy goods' in details:
        fuliza_dets = details.replace(
            'Buy goods', 'Buy goods fuliza')
    elif 'Buy goods fuliza' in details:
        fuliza_dets = details.replace(
            'Buy goods fuliza', 'Buy goods')
    elif 'Pay Bill Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Pay Bill to', 'Pay Bill fuliza')
    elif 'Pay Bill fuliza Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Pay Bill fuliza', 'Pay Bill to')
    elif 'Merchant Payment Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Buy goods', 'Buy goods fuliza')
    elif 'Buy goods fuliza M-Pesa Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Buy goods fuliza', 'Buy goods')
    chk = dbquery.checkcat(details, user)
    chk2 = dbquery.checkcat(fuliza_dets, user)
    if chk or chk2:
        return []
    else:
        dbreq = dbquery.insertcat(userinp, details, fuliza_dets, online_dets, user, sttype, budget)
    return dbreq

# function for getting category transcations per statement

def mpesa_df(file):
    df = pd.read_csv(f'./uploads/{file}.csv', 
    converters={'Withdrawn': str, 'Paid In': str, 'Balance': str}
    )
    df.fillna(0, inplace=True)
    df.replace('\r', ' ', regex=True, inplace=True)
    df.replace('\n', ' ', regex=True, inplace=True)

    remw = df.loc[df.Withdrawn != "Withdrawn"].copy()
    remw['Withdrawn'] = remw.Withdrawn.astype(str)
    remw['Paid In'] = remw['Paid In'].astype(str)
    remw['Balance'] = remw['Balance'].astype(str)
    remw['Withdrawn'] = remw.Withdrawn.str.replace("-", "", regex=False)
    remw['Withdrawn'] = remw.Withdrawn.str.replace(",", "", regex=False)
    remw['Withdrawn'] = remw['Withdrawn'].fillna(0).astype(float)
    # remw['Balance'] = remw.Balance.str.replace("-", "", regex=False)
    remw['Balance'] = remw.Balance.str.replace(",", "", regex=False)
    remw['Balance'] = remw['Balance'].fillna(0).astype(float)
    remw['Paid In'] = remw['Paid In'].str.replace(",", "", regex=False)
    remw['Paid In'] = remw['Paid In'].fillna(0).astype(float)
    remw['Details'] = remw['Details'].str.strip()
    remw['Details'] = remw['Details'].str.replace('\n', ' ', regex=False)
    remw['Details'] = remw['Details'].str.replace('\r', ' ', regex=False)
    remw['Details'] = remw['Details'].str.replace('  ', ' ', regex=False)
    remw['Details'] = remw['Details'].apply(str)
    # convert date column to datetime
    remw['Completion Time'] = pd.to_datetime(remw['Completion Time'])
    return remw

def categoryanal(file, user):
    # get path to file and get dataframe from file
    remw = mpesa_df(file)
    insert_mpesa_costs(user)
    # get month and year from date for first and last row
    first = remw['Completion Time'].iloc[0]
    last = remw['Completion Time'].iloc[-1]
    # get month and year from date
    firstmonth = first.strftime("%B")
    firstyear = first.strftime("%Y")
    lastmonth = last.strftime("%B")
    lastyear = last.strftime("%Y")
    firstdate = first.strftime("%d")
    lastdate = last.strftime("%d")
    date_range = f'{lastdate} {lastmonth} {lastyear} - {firstdate} {firstmonth} {firstyear}'
    # get all categories from database
    categories = dbquery.getcat(user, 'mpesa')
    # search for category in details
    # create empty list to store results
    catlist = []
    # loop through rows in dataframe and check if details match category
    for x in categories:
        try:
            cat = remw.loc[remw['Details'].str.contains(
                x['details'], regex=False)]
            catlist.append(cat.to_dict('records'))
            
        except:
            pass
    # compare category to details and create object with category and withdrawn
    catlist2 = []
    budgetlist = []
    for z in catlist:
        for x in z:
            for y in categories:
                
                if x:
                    if x['Details'] == y['details']:
                        obj = {
                            'cat': y['category'],
                            'amount': x['Withdrawn'],
                        }
                        catlist2.append(obj)
    # get similar cats and add withdrawal amount
    totals = {}
    for x in catlist2:
        if x["cat"] in totals:
            totals[x["cat"]] += x["amount"]
        else:
            totals[x["cat"]] = x["amount"]
    # loop through totals and add budget
    finallist = []
    for x in totals:
        budget = dbquery.getbudget(user, x) #TODO: don't query db for each category
        if budget:
            totals[x] = {
                'amount': totals[x],
                'budget': budget
            }
        else:
            totals[x] = {
                'amount': totals[x],
                'budget': 0
            }

    return totals, date_range, finallist

# same function but for all files in database


def categoryanalall(user):
    file = dbquery.get_file_names(user, 'mpesa')
    res = []
    dates = []
    for x in file:
        totals, date_range = categoryanal(x, user)
        res.append(totals)
        dates.append(date_range)
    return res, dates


# insert saf mpesa costs
def insert_mpesa_costs(user):
    # keywords = ['Customer Transfer of Funds Charge', 'Pay Bill Charge', 'Withdrawal Charge', 'Pay Merchant Charge',
    #            'Customer Transfer of Funds Charges', 'Pay Bill Charges', 'Withdrawal Charges', 'Pay Merchant Charges']

    new_keywords = ['Transaction cost']
    # check if they exist in db
    for x in new_keywords:
        res = dbquery.checkcat(x, user) #TODO: done once
        # if res is empty array then insert
        if not res:
            res2 = dbquery.insertmpesacosts(x, user)

# time analysis of mpesa transactions
def mpesa_time_analysis(file):
    df = mpesa_df(file)
    # remove all transcation costs from df
    df = df.loc[~df['Details'].str.contains(
        'Transaction cost', regex=False)] # TODO: this removes new transcation costs
    df = df.loc[~df['Details'].str.contains(
        'Pay Bill Charge', regex=False)]
    df = df.loc[~df['Details'].str.contains(
        'Withdrawal Charge', regex=False)]
    df = df.loc[~df['Details'].str.contains(
        'Pay Merchant Charge', regex=False)]
    # group by date
    df['Completion Time'] = pd.to_datetime(df['Completion Time'])
    df['Completion Time'] = df['Completion Time'].dt.date
    # get df from past week
    today = datetime.date.today()
    # get first day of current week
    first_day = today - datetime.timedelta(days=today.weekday())
    df = df.loc[df['Completion Time'] >= first_day]
    df = df.groupby(['Completion Time'])
    # remove outliers from balance 
    
    # get number of transcations per day, total withdrawn and total paid in and average balance
    # loop through groups and get values
    res = []
    for x, y in df:
        # create the variables
        num_transcations = y['Details'].count()
        total_withdrawn = y['Withdrawn'].sum()
        total_paid_in = y['Paid In'].sum()
        
        average_balance = y['Balance'].mean()
        std = y['Balance'].std(ddof=0)
        # remove outliers
        if std > 0:
            y = y[y['Balance'] < average_balance + (std*3)]
            avg = y['Balance'].mean()
        else:
            avg = average_balance
            pass
        # remove nan values
        # convert pandas date to string
        convert_date = y['Completion Time'].astype(str)
        # create object with date as key and values as list
        obj = {
            'date': convert_date.iloc[0],
            'num_transcations': int(num_transcations),
            'total_withdrawn': int(total_withdrawn),
            'total_paid_in': int(total_paid_in),
            'average_balance': int(avg) if avg else 0
        }
        res.append(obj)
    return res

    
def monthlycategoryanal(file, user):
    df = mpesa_df(file)
    df['Completion Time'] = pd.to_datetime(df['Completion Time']).dt.date
    today = datetime.date.today()
    # get first day of current month
    first_day = today.replace(day=1)
    # get all transcations from first day of month
    df = df.loc[df['Completion Time'] >= first_day]
    w_sum = df['Withdrawn'].sum()
    cats = dbquery.getcat(user, 'mpesa')
    tmplist = []
    for x in cats:
        cat = df.loc[df['Details'].str.contains(x['details'], regex=False)]
        tmplist.append(cat.to_dict('records'))
    # compare category to details and create object with category and withdrawn
    catlist2 = []
    for z in tmplist:
        for x in z:
            for y in cats:
                if x:
                    if x['Details'] == y['details']:
                        obj = {
                            'cat': y['category'],
                            'amount': x['Withdrawn'],
                        }
                        catlist2.append(obj)
    # get similar cats and add withdrawal amount
    totals = {}
    for x in catlist2:
        if x["cat"] in totals:
            totals[x["cat"]] += x["amount"]
        else:
            totals[x["cat"]] = x["amount"]
    # loop through totals and add budget
    finallist = []
    W_draw = 0
    for x in totals:
        budget = dbquery.getbudget(user, x)
        if budget:
            totals[x] = {
                'amount': int(totals[x]),
                'budget': int(budget)
            }
        else:
            totals[x] = {
                'amount': int(totals[x]),
                'budget': 0
            }
        W_draw += totals[x]['amount']
    uncat = w_sum - W_draw
    totals['Uncategorized'] = {
        'amount': int(uncat),
        'budget': 0
    }
    return totals

def paidinoutdaily(file):
    df = mpesa_df(file)
    df['Completion Time'] = pd.to_datetime(df['Completion Time']).dt.date
    #get current date but starting at 0.00
    today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today = today.date()
    first_day = today - datetime.timedelta(days=7)
    # get transcation for today
    weekly = df.loc[df['Completion Time'] >= first_day]
    df = df.loc[df['Completion Time'] >= today]
    weeklygroup = weekly.groupby(['Completion Time'])
    weeklypaidin = []
    weeklywithdrawn = []
    for x, y in weeklygroup:
        # print(y['Paid In'])
        if y['Paid In'].sum() != 0:
            obj = {
                'date': y['Completion Time'].iloc[0].strftime("%Y-%m-%d"),
                'amount': y['Paid In'].sum(),
                'transcations': y.to_dict('records')
            }
            weeklypaidin.append(obj)
        if y['Withdrawn'].iloc[0] != 0:
            obj = {
                'date': y['Completion Time'].iloc[0].strftime("%Y-%m-%d"),
                'amount': y['Withdrawn'].sum(),
                'transcations': y.to_dict('records')
            }
            weeklywithdrawn.append(obj)
    # remove paid in with 0
    for x in weeklypaidin:
        for y in list(x['transcations']):
            if y['Paid In'] == 0:
                x['transcations'].remove(y)
    weeklypaidin.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    # remove withdrawn with 0
    for x in weeklywithdrawn:
        for y in list(x['transcations']):
            if y['Withdrawn'] == 0:
                x['transcations'].remove(y)
    weeklywithdrawn.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    # get total paid in and withdrawn
    total_paid_in = df['Paid In'].sum()
    total_withdrawn = df['Withdrawn'].sum()
    # get total transcations
    sum_transcations = df['Details'].count()
    paidintransactions = df.loc[df['Paid In'] != 0].to_dict('records')
    paidouttransactions = df.loc[df['Withdrawn'] != 0].to_dict('records')   
    return [str(int(total_paid_in)), str(int(total_withdrawn)), str(sum_transcations), weeklypaidin, weeklywithdrawn]

def paidinoutweekly(file):
    df = mpesa_df(file)
    df['Completion Time'] = pd.to_datetime(df['Completion Time']).dt.date
    today = datetime.date.today()
    # get first day of current week
    first_day = today - datetime.timedelta(days=today.weekday())
    print(first_day)
    # get all transcations from first day of week
    df = df.loc[df['Completion Time'] >= first_day]
    # get total paid in and withdrawn
    total_paid_in = df['Paid In'].sum()
    total_withdrawn = df['Withdrawn'].sum()
    # get total transcations
    sum_transcations = df['Details'].count()
    return total_paid_in, total_withdrawn, sum_transcations

def lefttospend(file, user, budget):
    cats = dbquery.getallcategories(user)
    df = mpesa_df(file)
    df['Completion Time'] = pd.to_datetime(df['Completion Time']).dt.date
    today = datetime.date.today()
    # get first day of current month
    first_day = today.replace(day=1)
    # get all transcations from first day of month
    df = df.loc[df['Completion Time'] >= first_day]
    spent = []
    for x in cats:    
        cat = df.loc[df['Details'].str.contains(x[2], regex=False, case=False)]
        if cat.empty:
            pass
        else:
            amnt = cat['Withdrawn'].sum()
            spent.append(amnt)
    total_spent = sum(spent)
    left = int(budget) - int(total_spent)
    print(spent, budget, total_spent, left)
    return left
                
def check_dets(user, cat):
    dets = dbquery.get_dets_by_cat(user, cat, 'mpesa')
    df = mpesa_df(f'mpesa_{user}')
    df['Completion Time'] = pd.to_datetime(df['Completion Time']).dt.date
    today = datetime.date.today()
    # get first day of current month
    first_day = today.replace(day=1)
    # get all transcations from first day of month
    df = df.loc[df['Completion Time'] >= first_day]

    totals = {}

    for x in dets:
        x['budget'] = int(x['budget']) if x['budget'] else 0
        cat = df.loc[df['Details'].str.contains(x['details'], regex=False, case=False)]
        if cat.empty:
            continue
        else:
            if totals:
                totals['amount'] += int(cat['Withdrawn'].sum())
                tsc = cat.to_dict('records')
                for n in tsc:
                    totals['transcations'].append(n)
                totals['unspent'] = int(totals['unspent']) - int(cat['Withdrawn'].sum())
            else:
                amnt = cat['Withdrawn'].sum()
                totals['amount'] = int(amnt)
                totals['transcations'] = cat.to_dict('records')
                totals['budget'] = x['budget']
                totals['unspent'] = x['budget'] - int(amnt)
    return totals

def sndmoney(user):
    df = mpesa_df(f'mpesa_{user}')
    df['Completion Time'] = pd.to_datetime(df['Completion Time'])
    df['Completion Time'] = df['Completion Time'].dt.date
    # get df from past week
    today = datetime.date.today()
    # get first day of current week
    first_day = today - datetime.timedelta(days=today.weekday())
    df = df.loc[df['Completion Time'] >= first_day]
    # remove fuliza from send money
    df['Details'] = df['Details'].str.replace('Send money fuliza', 'Send money')
    df = df.groupby(['Details'])
    # filter send money
    res = []
    for x, y in df:
        snd = y.loc[y['Details'].str.contains('Send money', regex=False)]
        if snd.empty:
            continue
        else:
            # get total of each group
            total = snd['Withdrawn'].sum()
            name = snd['Details'].iloc[0]
            obj = {
                'name': name.replace('Send money ', ''),
                'amount': total
            }
            res.append(obj)
    return res


def tillpay(user):
    df = mpesa_df(f'mpesa_{user}')
    df['Completion Time'] = pd.to_datetime(df['Completion Time'])
    df['Completion Time'] = df['Completion Time'].dt.date
    # get df from past week
    today = datetime.date.today()
    # get first day of current week
    first_day = today - datetime.timedelta(days=today.weekday())
    df = df.loc[df['Completion Time'] >= first_day]
    df['Details'] = df['Details'].str.replace('Buy goods fuliza', 'Buy goods')
    df = df.groupby(['Details'])
    # filter send money
    res = []
    for x, y in df:
        snd = y.loc[y['Details'].str.contains('Buy goods', regex=False)]
        if snd.empty:
            continue
        else:
            # get total of each group
            total = snd['Withdrawn'].sum()
            name = snd['Details'].iloc[0]
            obj = {
                'name': name.replace('Buy goods ', ''),
                'amount': total
            }
            res.append(obj)
    return res

def pbillpay(user):
    df = mpesa_df(f'mpesa_{user}')
    df['Completion Time'] = pd.to_datetime(df['Completion Time'])
    df['Completion Time'] = df['Completion Time'].dt.date
    # get df from past week
    today = datetime.date.today()
    # get first day of current week
    first_day = today - datetime.timedelta(days=today.weekday())
    df = df.loc[df['Completion Time'] >= first_day]
    df['Details'] = df['Details'].str.replace('Pay Bill fuliza', 'Pay Bill to')
    df = df.groupby(['Details'])
    # filter send money
    res = []
    for x, y in df:
        snd = y.loc[y['Details'].str.contains('Pay Bill to', regex=False)]
        if snd.empty:
            continue
        else:
            # get total of each group
            total = snd['Withdrawn'].sum()
            name = snd['Details'].iloc[0]
            obj = {
                'name': name.replace('Pay Bill to ', ''),
                'amount': total
            }
            res.append(obj)
    return res

