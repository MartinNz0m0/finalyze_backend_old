import pandas as pd
import dbquery


def userinput(user, num, stttype):
    file = dbquery.get_file_names(user, stttype)

    userres = []
    # arrays for collecting similar transactions
    customer = []
    paybillarr = []
    tillarr = []
    for x in file:
        df = pd.read_csv(f'./uploads/{x}.csv')
        df.fillna(0, inplace=True)
        df.replace('\r', ' ', regex=True, inplace=True)

        remw = df.loc[df.Withdrawn != "Withdrawn"].copy()
        # remw = remw.reset_index(drop=True)
        remw['Withdrawn'] = remw.Withdrawn.str.replace("-", "", regex=False)
        remw['Withdrawn'] = remw.Withdrawn.str.replace(",", "", regex=False)
        remw['Withdrawn'] = remw['Withdrawn'].fillna(0).astype(float)
        remw['Paid In'] = remw['Paid In'].str.replace(",", "", regex=False)
        remw['Paid In'] = remw['Paid In'].fillna(0).astype(float)
        # convert to int

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
                'Customer Transfer to|Customer Transfer Fuliza')
            paybill = details.str.contains('Pay Bill to|Pay Bill Fuliza')
            till = details.str.contains(
                'Merchant Payment to|Merchant Payment Fuliza')
            # prompt user to identify the transactions
            final = details[customertransfer].to_list()
            finalpbill = details[paybill].to_list()
            finaltill = details[till].to_list()
            customer.append(final)
            paybillarr.append(finalpbill)
            tillarr.append(finaltill)
    # flatten arrays before removing duplicates
    flatenlist = [item for sublist in customer for item in sublist]
    flatentill = [item for sublist in tillarr for item in sublist]
    flatenpbill = [item for sublist in paybillarr for item in sublist]
    # remove duplicates
    cleanlist1 = list(dict.fromkeys(flatenlist))
    cleanlist2 = list(dict.fromkeys(flatentill))
    cleanlist3 = list(dict.fromkeys(flatenpbill))
    # remove details found in database
    # create final list to be returned
    final = []
    final2 = []
    final3 = []
    for x in cleanlist1:
        # check for fuliza as well
        if 'Customer Transfer Fuliza' in x:
            x2 = x.replace('Customer Transfer Fuliza MPesa to',
                           'Customer Transfer to')
        elif 'Customer Transfer to' in x:
            x2 = x.replace('Customer Transfer to',
                           'Customer Transfer Fuliza MPesa to')
        else:
            pass

        dbreq = dbquery.checkcat(x, user)
        dbreq2 = dbquery.checkcat(x2, user)
        if x not in dbreq:
            final.append(x)
        if not x2 in dbreq2 and x2 in cleanlist1:
            final.append(x2)
    for x in cleanlist2:
        # remove online word from paybill online
        if 'Online' in x:
            x = x.replace('Online', '')
        # check for fuliza as well
        if 'Merchant Payment Fuliza' in x:
            x2 = x.replace('Merchant Payment Fuliza M-Pesa to',
                           'Merchant Payment to')
        elif 'Merchant Payment to' in x:
            x2 = x.replace('Merchant Payment to',
                           'Merchant Payment Fuliza M-Pesa to')

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
        if 'Pay Bill Fuliza' in x:
            x2 = x.replace('Pay Bill Fuliza M-Pesa to', 'Pay Bill to')
        elif 'Pay Bill to' in x:
            x2 = x.replace('Pay Bill to', 'Pay Bill Fuliza M-Pesa to')

        dbreq = dbquery.checkcat(x, user)
        dbreq2 = dbquery.checkcat(x2, user)
        if x not in dbreq:
            final3.append(x)
        if x2 not in dbreq2 and x2 in cleanlist3:
            final3.append(x2)
    return final, final2, final3
    # sort = df.sort_values(by=['Withdrawn'], ascending=False)

# get user imput for categorizing transactions


def usersubmit(userinp, details, user, sttype):
    online_dets = ''
    if 'Customer Transfer to' in details:
        # add one for fuliza as well
        fuliza_dets = details.replace(
            'Customer Transfer to', 'Customer Transfer Fuliza MPesa to')
    elif 'Customer Transfer Fuliza' in details:
        fuliza_dets = details.replace(
            'Customer Transfer Fuliza MPesa to', 'Customer Transfer to')
    elif 'Pay Bill to' in details:
        fuliza_dets = details.replace(
            'Pay Bill to', 'Pay Bill Fuliza M-Pesa to')
    elif 'Pay Bill Fuliza' in details:
        fuliza_dets = details.replace(
            'Pay Bill Fuliza M-Pesa to', 'Pay Bill to')
    elif 'Merchant Payment to' in details:
        fuliza_dets = details.replace(
            'Merchant Payment to', 'Merchant Payment Fuliza M-Pesa to')
    elif 'Merchant Payment Fuliza' in details:
        fuliza_dets = details.replace(
            'Merchant Payment Fuliza M-Pesa to', 'Merchant Payment to')
    elif 'Pay Bill Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Pay Bill to', 'Pay Bill Fuliza M-Pesa to')
    elif 'Pay Bill Fuliza Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Pay Bill Fuliza M-Pesa to', 'Pay Bill to')
    elif 'Merchant Payment Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Merchant Payment to', 'Merchant Payment Fuliza M-Pesa to')
    elif 'Merchant Payment Fuliza M-Pesa Online' in details:
        online_dets = details.replace('Online', '')
        fuliza_dets = online_dets.replace(
            'Merchant Payment Fuliza M-Pesa to', 'Merchant Payment to')
    dbreq = dbquery.insertcat(userinp, details, fuliza_dets, online_dets, user, sttype)

    return dbreq

# function for getting category transcations per statement

def mpesa_df(file):
    df = pd.read_csv(f'./uploads/{file}.csv')
    df.fillna(0, inplace=True)
    df.replace('\r', ' ', regex=True, inplace=True)
    df.replace('\n', ' ', regex=True, inplace=True)

    remw = df.loc[df.Withdrawn != "Withdrawn"].copy()
    remw['Withdrawn'] = remw.Withdrawn.str.replace("-", "", regex=False)
    remw['Withdrawn'] = remw.Withdrawn.str.replace(",", "", regex=False)
    remw['Withdrawn'] = remw['Withdrawn'].fillna(0).astype(float)
    remw['Balance'] = remw.Balance.str.replace("-", "", regex=False)
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
        budget = dbquery.getbudget(user, x)
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
    file = dbquery.get_file_names(user)
    res = []
    dates = []
    for x in file:
        totals, date_range = categoryanal(x, user)
        res.append(totals)
        dates.append(date_range)
    return res, dates


# insert saf mpesa costs
def insert_mpesa_costs(user):
    keywords = ['Customer Transfer of Funds Charge', 'Pay Bill Charge', 'Withdrawal Charge', 'Pay Merchant Charge',
                'Customer Transfer of Funds Charges', 'Pay Bill Charges', 'Withdrawal Charges', 'Pay Merchant Charges']

    # check if they exist in db
    for x in keywords:
        res = dbquery.checkcat(x, user)
        # if res is empty array then insert
        if not res:
            res2 = dbquery.insertmpesacosts(x, user)

# time analysis of mpesa transactions
def mpesa_time_analysis(file):
    df = mpesa_df(file)
    # remove all transcation costs from df
    df = df.loc[~df['Details'].str.contains(
        'Customer Transfer of Funds Charge', regex=False)]
    df = df.loc[~df['Details'].str.contains(
        'Pay Bill Charge', regex=False)]
    df = df.loc[~df['Details'].str.contains(
        'Withdrawal Charge', regex=False)]
    df = df.loc[~df['Details'].str.contains(
        'Pay Merchant Charge', regex=False)]
    # group by date
    df['Completion Time'] = pd.to_datetime(df['Completion Time'])
    df['Completion Time'] = df['Completion Time'].dt.date
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
            pass
        # remove nan values
        # convert pandas date to string
        convert_date = x[0].strftime("%Y-%m-%d")
        # create object with date as key and values as list
        obj = {
            'date': convert_date,
            'num_transcations': int(num_transcations),
            'total_withdrawn': int(total_withdrawn),
            'total_paid_in': int(total_paid_in),
            'average_balance': int(avg) if avg else 0
        }
        res.append(obj)
    return res
  
    
