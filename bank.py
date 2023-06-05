import tabula
from pypdf import PdfReader
import csv
import os
import pandas as pd
import re
import dbquery
import pdfplumber
import userinput


def coopcsv(x):
    pdf_path = x
    # get number of pages
    reader = PdfReader(f'./uploads/{pdf_path}')
    pages = len(reader.pages)
    columns = [17.28, 81.36, 139.68, 259.92, 336.96, 409.68, 483.84]
    first_page = tabula.convert_into(f'./uploads/{pdf_path}', f'./uploads/{pdf_path}f.csv', output_format='csv',
                                     pages='1', stream=True, guess=False, columns=columns, area=[403.20, 16.56, 791.28, 574.56])

    other_pages = tabula.convert_into(f'./uploads/{pdf_path}', f'./uploads/{pdf_path}t.csv', output_format='csv',
                                      pages=f'2-{pages}', stream=True, guess=False, columns=columns, area=[78.48, 12.56, 791.28, 570.56])

    # merge the CSV files
    with open(f'./uploads/{pdf_path}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # remove first empty column
        with open(f'./uploads/{pdf_path}f.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                del row[0]
                if row[0] == 'n Date':
                    continue
                elif row[2] == 'Opening Balance':
                    continue
                else:
                    writer.writerow(row)
        # remove first empty column
        with open(f'./uploads/{pdf_path}t.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                del row[0]
                if row[0] == 'n Date':
                    continue
                elif row[4] == 'Debit':
                    continue
                elif row[3] == 'Reference':
                    continue
                else:
                    writer.writerow(row)

    with open(f'./uploads/{pdf_path}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # read the header row
        header = next(reader)

        # initialize the previous row
        prev_row = None

        # initialize the merged rows
        merged_rows = []

        # loop through the rows
        for row in reader:
            if row[0] == '':
                # if the first column is empty, merge the cells to the row above
                if prev_row is not None:
                    for i in range(len(row)):
                        if row[i] != '':
                            prev_row[i] += ' ' + row[i]
                else:
                    # if this is the first row, skip it
                    continue
            else:
                # if the first column is not empty, add the previous row to the merged rows
                if prev_row is not None:
                    merged_rows.append(prev_row)
                prev_row = row

        # add the last row to the merged rows
        if prev_row is not None:
            merged_rows.append(prev_row)

    # open the CSV file for writing
    with open(f'./uploads/{pdf_path}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        # write the header row
        writer.writerow(header)

        # write the merged rows
        for row in merged_rows:
            writer.writerow(row)
    # delete the temporary files and pdf
    os.remove(f'./uploads/{pdf_path}')
    os.remove(f'./uploads/{pdf_path}f.csv')
    os.remove(f'./uploads/{pdf_path}t.csv')


def coopstatements(x):
    pdf_path = x
    # check if x exists
    if os.path.exists(f'./uploads/{x}.csv'):
        # if file exists, continue
        print('File exists')
        # run checkdata in dbquery
    else:
        # if file does not exist, return error
        print('File does not exist')
        try:
            coopcsv(x)
        except Exception as e:
            print(e)
            return f'Error, {e} something is wrong with the file', 400
    # get data from the CSV file and add header
    # header is skipping first column
    df = pd.read_csv(f'./uploads/{pdf_path}.csv', header=None, skiprows=1, names=[
                     'Date', 'Value Date', 'Details', 'Ref', 'Debit', 'Credit', 'Balance'])
    df2 = df.loc[df.Ref != "Number"].copy()
    df3 = df2.loc[df2.Ref != "Reference"].copy()
    df3['Value Date'] = pd.to_datetime(df3['Value Date'], format='%d/%m/%Y')
    # convert debit, credit and balance to float and remove commas and remove null values
    df3['Debit'] = df3['Debit'].str.replace(',', '').astype(float)
    df3['Credit'] = df3['Credit'].str.replace(',', '').astype(float)
    df3['Balance'] = df3['Balance'].str.replace(',', '').astype(float)
    df3['Debit'] = df3['Debit'].fillna(0)
    df3['Credit'] = df3['Credit'].fillna(0)
    df3['Balance'] = df3['Balance'].fillna(0)
    # if details have transfer to mpesa, replace first word with empty and check if last word is 'transfer'
    df3['Details'] = df3['Details'].str.strip()
    df3['Details'] = df3['Details'].str.replace(
        ' Transfer', '', regex=False, case=True)
    df3['Details'] = df3['Details'].str.replace(
        r'^\w+\s+(?=TRANSFER)', '', regex=True, case=True)
    df3['Details'] = df3['Details'].str.replace(
        r'\s+(?=TRANSFER)', '', regex=True, case=True)
    # df3['Details'] = df3['Details'].str.replace(r'^\S+\s+(?=SAFARICOM\s)', '', regex=True, case=True)
    df3['Details'] = df3['Details'].str.replace(
        r'^\S+\s+SAFARICOM\b.*$', 'SAFARICOM', regex=True, case=True)
    # remove words with numbers and letters
    df3['Details'] = df3['Details'].apply(str)
    # df3['Details'] = df3['Details'].apply(lambda x: re.sub(r'\b\w*\d\w*\b\s*', '', x))
    df3['Details'] = df3['Details'].str.replace(
        r'\b(?=[a-z]+\d|[a-z]*\d+[a-z]+)\w*\b\s*', '', regex=True, case=False).str.strip()

    return df3


def coopstatementssearch(x):
    pdf_path = x
    # check if x exists
    if os.path.exists(f'./uploads/{x}.csv'):
        # if file exists, continue
        print('File exists')
    else:
        # if file does not exist, return error
        print('File does not exist')
        try:
            coopcsv(x)
        except Exception as e:
            print(e)
            return f'Error, {e} something is wrong with the file', 400
    # get data from the CSV file and add header
    # header is skipping first column
    df = pd.read_csv(f'./uploads/{pdf_path}.csv', header=None, skiprows=1, names=[
                     'Date', 'Value Date', 'Details', 'Ref', 'Debit', 'Credit', 'Balance'])
    df2 = df.loc[df.Ref != "Number"].copy()
    df3 = df2.loc[df2.Ref != "Reference"].copy()
    df3['Value Date'] = pd.to_datetime(df3['Value Date'], format='%d/%m/%Y')
    # convert debit, credit and balance to float and remove commas and remove null values
    df3['Debit'] = df3['Debit'].str.replace(',', '').astype(float)
    df3['Credit'] = df3['Credit'].str.replace(',', '').astype(float)
    df3['Balance'] = df3['Balance'].str.replace(',', '').astype(float)
    df3['Debit'] = df3['Debit'].fillna(0)
    df3['Credit'] = df3['Credit'].fillna(0)
    df3['Balance'] = df3['Balance'].fillna(0)
    # if details have transfer to mpesa, replace first word with empty and check if last word is 'transfer'
    df3['Details'] = df3['Details'].str.strip()
    df3['Details'] = df3['Details'].apply(str)
    return df3


def cooptcosts(user):
    # make db query to add the known details for costs
    keywords = ['MPESA BANK COMMISSION',
                'SAFARICOM', 'COMM. PAYMENT', 'EXCISE DUTY']
    db = dbquery.checkcoopcosts(user)
    if db:
        # keywords already in db
        pass
    else:
        # add keywords to db
        for x in keywords:
            dbquery.insertcooptcosts(user, x)
    return 'Ok'
    # make db query to add the known details for costs


def groupbycoop(user, num, stttype):
    cooptcosts(user)
    file = dbquery.get_file_names(user, stttype)
    response = []
    final = []
    for x in file:
        df = coopstatements(x)
        group = df.groupby(['Details'])
        largest = group['Debit'].sum()
        large_count = group['Debit'].count()
        above_4 = group['Debit'].count() >= int(num)
        above_4 = large_count[above_4]
        # iterate through above 4 and check the details
        for index, row in above_4.items():
            details = group.get_group(index)['Details'].drop_duplicates()
            # identify details for transcation costs
            t_costs = details.str.contains(
                'MPESA BANK COMMISSION', regex=False, case=True, na=False)
            saf_cost = details.str.contains(
                'SAFARICOM', regex=False, case=True, na=False)
            more_cost = details.str.contains(
                'COMM. PAYMENT', regex=False, case=True, na=False)
            excise = details.str.contains(
                'EXCISE DUTY', regex=False, case=True, na=False)
            # send other detasils to user
            if t_costs.any() or saf_cost.any() or more_cost.any() or excise.any():
                continue
            else:
                response.append(index)
    # remove categories that are in db
    for x in response:
        dbreq = dbquery.checkcoopcat(x, user)
        if x not in dbreq:
            final.append(x)
    return final

    # get largest by count


def coopquickanal(file, user):
    # quick analysis like for mpesa

    df = coopstatements(file)
    # get first and last date
    first_date = df['Value Date'].min()
    last_date = df['Value Date'].max()
    # get first month, date, year and last month, date, year
    first_month = first_date.strftime("%B")
    first_year = first_date.strftime("%Y")
    last_month = last_date.strftime("%B")
    last_year = last_date.strftime("%Y")
    first_date = first_date.strftime("%d")
    last_date = last_date.strftime("%d")
    date_range = f'{first_date} {first_month} {first_year} to {last_date} {last_month} {last_year}'

    # get categories from db
    categories = dbquery.getcat(user, 'coop')
    dbquery.checkcoopfiledaterange(user, file, date_range)
    # loop through categories and check if details contain the category
    response = []
    cat_list = []
    for x in categories:
        try:
            cat = df.loc[df['Details'].str.contains(x['details'], regex=False)]
            cat_list.append(cat.to_dict('records'))
        except Exception as e:
            print(e)
            pass
    cat_list2 = []
    for x in cat_list:
        # get index for x in cat list
        index = cat_list.index(x)
        for z in x:
            for y in categories:
                if x:
                    if y['details'] in z['Details']:
                        # set amount to 2 decimal places
                        obj = {
                            'category': y['category'],
                            'amount': int(z['Debit'])
                        }
                        cat_list2.append(obj)
    totals = {}
    for x in cat_list2:
        if x['category'] in totals:
            totals[x['category']] += int(x['amount'])
        else:
            totals[x['category']] = int(x['amount'])
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
    return totals, date_range


def coop_time_analysis(file):
    df = coopstatements(file)

    # remove all transcatioon costs from df
    df = df[~df['Details'].str.contains(
        'MPESA BANK COMMISSION', regex=False, case=True, na=False)]
    df = df[~df['Details'].str.contains(
        'SAFARICOM', regex=False, case=True, na=False)]
    df = df[~df['Details'].str.contains(
        'COMM. PAYMENT', regex=False, case=True, na=False)]
    df = df[~df['Details'].str.contains(
        'EXCISE DUTY', regex=False, case=True, na=False)]

    # group by date
    df['Value Date'] = df['Value Date'].dt.date
    group = df.groupby(['Value Date'])

    res = []
    for x, y in group:
        # create the variables
        num_transcations = y['Details'].count()
        total_withdrawn = y['Debit'].sum()
        total_paid_in = y['Credit'].sum()

        average_balance = y['Balance'].mean()
        # std = y['Balance'].std()

        # remove outliers should go here
        # if std > 0:
        #     y = y[y['Balance'] > average_balance + (std*3)]
        #     avg = y['Balance'].mean()
        # else:
        #     pass
        convert_date = x[0].strftime("%Y-%m-%d")

        obj = {
            'date': convert_date,
            'num_transcations': int(num_transcations),
            'total_withdrawn': int(total_withdrawn),
            'total_paid_in': int(total_paid_in),
            'average_balance': int(average_balance)
        }
        res.append(obj)
    return res


# quick function for equity statements
def equityconvert(file):
    # convert equity statements to csv
    path = f"./uploads/{file}"
    reader = PdfReader(f'{path}')
    pages = len(reader.pages)
    dimensions = [253.44, 33.84, 645.84, 572.4]
    otherpagedimensions = [141.12, 50.4, 635.04, 591.12]
    columns = [105.12, 162.72, 273.6, 332.64, 416.16, 501.84]
    firstpage = tabula.convert_into(
        path, f"./uploads/{file}1.csv", output_format="csv", pages='1', area=dimensions)
    otherpages = tabula.convert_into(path, f"./uploads/{file}2.csv", output_format="csv",
                                     pages=f'2-{pages}', area=otherpagedimensions, stream=True, guess=False, columns=columns)

    # remove empty columns from first page csv
    # df = pd.read_csv(f"./uploads/{file}1.csv")
    # df = df.dropna(axis=1, how='all')
    # df.to_csv(f"./uploads/{file}1.csv", index=False)

    # combine the two csv files
    with open(f'./uploads/{file}1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # remove first empty column
        with open(f'./uploads/{file}2.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                del row[0]
                # if last row is grand total, remove it
                if row[1] == 'Grand Total':
                    break
                else:
                    writer.writerow(row)
    # open the merged csv
    with open(f'./uploads/{file}1.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # read header row
        header = next(reader)

        # initialize the previous row
        prev_row = None

        merged_rows = []

        for row in reader:
            # if the first column is empty, merge the cells to the row above
            if row[0] == '':
                if prev_row is not None:
                    for i in range(len(row)):
                        if row[i] != '':
                            prev_row[i] += ' ' + row[i]
                else:
                    continue
            else:
                # if there is a previous row, append it to the merged_rows
                if prev_row is not None:
                    merged_rows.append(prev_row)
                prev_row = row
        if prev_row is not None:
            merged_rows.append(prev_row)

        # write the merged rows to a new csv file
    with open(f'./uploads/{file}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in merged_rows:
            writer.writerow(row)

    # delete temp files
    # os.remove(f'./uploads/{file}1.csv')
    # os.remove(f'./uploads/{file}2.csv')
    os.remove(f'./uploads/{file}')


def equitystatements(file):
    # check if csv exists
    if os.path.exists(f'./uploads/{file}.csv'):
        # if file exists, continue
        print('File exists')
        # run checkdata in dbquery
    else:
        # if file does not exist, return error
        print('File does not exist')
        try:
            equityconvert(file)
        except Exception as e:
            print(e)
            return f'Error, {e} something is wrong with the file', 400

    df = pd.read_csv(f"./uploads/{file}.csv", header=None, skiprows=1, names=[
                     'Value Date', 'Details', 'ID', 'Debit', 'Credit', 'Balance'])
    df = df.fillna(0)
    # remove last row
    df = df[:-1]
    # remove row if credit has the name credit
    df = df[df.Credit != 'Credit']
    # remove commas from debit and credit
    # fill na with 0
    df['Debit'] = df['Debit'].str.replace(',', '')
    df['Credit'] = df['Credit'].str.replace(',', '')
    df['Balance'] = df['Balance'].str.replace(',', '')
    # convert debit and credit to float
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)
    df['Balance'] = df['Balance'].astype(float)
    df['Debit'] = df['Debit'].fillna(0)
    df['Credit'] = df['Credit'].fillna(0)
    df['Balance'] = df['Balance'].fillna(0)
    df['Value Date'] = pd.to_datetime(df['Value Date'], format='%d-%m-%Y')
    # if details start with mps remove last 3 words, check that str has five words
    df.loc[df['Details'].str.startswith('MPS'), 'Details'] = df.loc[df['Details'].str.startswith(
        'MPS'), 'Details'].str.split(' ').str[0:2].str.join(' ')    # get the index of the rows that start with mps

    return df


def equitystatementsearch(file):
    pdf_path = f"./uploads/{file}"

    if os.path.exists(f'./uploads/{file}.csv'):
        # if file exists, continue
        print('File exists')
        # run checkdata in dbquery
    else:
        # if file does not exist, return error
        print('File does not exist')
        try:
            equityconvert(file)
        except Exception as e:
            print(e)
            return f'Error, {e} something is wrong with the file', 400

    df = pd.read_csv(f"./uploads/{file}.csv", header=None, skiprows=1, names=[
                     'Value Date', 'Details', 'ID', 'Debit', 'Credit', 'Balance'])
    df = df.fillna(0)

    # remove last row
    df = df[:-1]
    # remove row if credit has the name credit
    df = df[df.Credit != 'Credit']
    # remove commas from debit and credit
    # fill na with 0
    df['Debit'] = df['Debit'].str.replace(',', '')
    df['Credit'] = df['Credit'].str.replace(',', '')
    df['Balance'] = df['Balance'].str.replace(',', '')
    # convert debit and credit to float
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)
    df['Balance'] = df['Balance'].astype(float)
    df['Debit'] = df['Debit'].fillna(0)
    df['Credit'] = df['Credit'].fillna(0)
    df['Balance'] = df['Balance'].fillna(0)
    df['Details'] = df['Details'].apply(str)
    df['Details'] = df['Details'].str.strip()
    return df


def equitytcosts(user):
    # make db call to add known transaction costs
    keywords = ['MOBILE MONEY CHARGES']
    db = dbquery.checkequitycosts(user)
    if db:
        pass
    else:
        for i in keywords:
            dbquery.addequitycosts(user, i)
    return 'Ok'


def equitygroupby(user, num, stttype):
    # run cost insertion
    equitytcosts(user)
    file = dbquery.get_file_names(user, stttype)
    response = []
    final = []
    for i in file:
        df = equitystatements(i)
        group = df.groupby('Details')
        large_count = group['Debit'].count()
        above_num = group['Debit'].count() >= int(num)
        above_num = large_count[above_num]

        for index, value in above_num.items():
            details = group.get_group(index)['Details'].drop_duplicates()
            # identify transaction costs
            t_costs = details.str.contains('MOBILE MONEY CHARGES')
            # will add others later

            if t_costs.any():
                continue
            else:
                response.append(index)
    # remove categories in db
    for x in response:
        dbreq = dbquery.checkequitycat(x, user)
        if x not in dbreq:
            final.append(x)

    return final


def equityquickanal(file, user):
    df = equitystatements(file)

    first_date = df['Value Date'].min()
    last_date = df['Value Date'].max()
    first_month = first_date.strftime('%B')
    last_month = last_date.strftime('%B')
    first_year = first_date.strftime('%Y')
    last_year = last_date.strftime('%Y')
    first_date = first_date.strftime('%d')
    last_date = last_date.strftime('%d')
    date_range = f'{first_date} {first_month} {first_year} to {last_date} {last_month} {last_year}'

    # get categories from db
    cats = dbquery.getcat(user, 'equity')
    dbquery.checkequityfiledaterange(user, file, date_range)

    response = []
    cat_list = []
    for i in cats:
        try:
            cat = df.loc[df['Details'].str.contains(i['details'], regex=False)]
            cat_list.append(cat.to_dict('records'))
        except Exception as e:
            print(e)
            pass
    cat_list2 = []
    for i in cat_list:
        index = cat_list.index(i)
        for z in i:
            for y in cats:
                if i:
                    if y['details'] in z['Details']:
                        obj = {
                            'category': y['category'],
                            'amount': int(z['Debit']),
                        }
                        cat_list2.append(obj)
    totals = {}
    for x in cat_list2:
        if x['category'] in totals:
            totals[x['category']] += x['amount']
        else:
            totals[x['category']] = x['amount']
    for x in totals:
        budget = dbquery.getbudget(user, x)
        if budget:
            totals[x] = {
                'amount': totals[x],
                'budget': budget,
            }
        else:
            totals[x] = {
                'amount': totals[x],
                'budget': 0,
            }
    return totals, date_range

def equity_time_analysis(file):
    df = equitystatements(file)

    # remove all transcation costs
    df = df[~df['Details'].str.contains('MOBILE MONEY CHARGES')]

    # group by date
    df['Value Date'] = df['Value Date'].dt.date
    group = df.groupby('Value Date')

    res = []
    for x, y in group:
        num_transcations = y['Details'].count()
        total_withdrawn = y['Debit'].sum()
        total_paid_in = y['Credit'].sum()
        average_balance = y['Balance'].mean()

        convert_date = x.strftime('%Y-%m-%d')
        obj = {
            'date': convert_date,
            'num_transcations': int(num_transcations),
            'total_withdrawn': int(total_withdrawn),
            'total_paid_in': int(total_paid_in),
            'average_balance': int(average_balance),
        }
        res.append(obj)
    return res


def overspend_index(user):
    # get all files
    mpesa_files = dbquery.get_file_names(user, 'mpesa')
    coop_files = dbquery.get_file_names(user, 'coop')
    equity_files = dbquery.get_file_names(user, 'equity')
    # categoryanal for each file
    ov_totals = []
    for x in mpesa_files:
        res = userinput.categoryanal(x, user)
        ov = 0
        tt = len(res[0])
        if res[0]:
            for cat, val in res[0].items():
                # get total values where amount is bigger than budget
                amount = val['amount']
                budget = val['budget']
                if amount > budget:
                    ov = ov +1
            ov_totals.append(ov/tt)
        else:
            # no files
            pass
    for x in coop_files:
        res = coopquickanal(x, user)
        ov = 0
        tt = len(res[0])
        if res[0]:
            for cat, val in res[0].items():
                # get total values where amount is bigger than budget
                amount = val['amount']
                budget = val['budget']
                if amount > budget:
                    ov = ov +1
            ov_totals.append(ov/tt)
        else:
            # no files
            pass
    for x in equity_files:
        res = equityquickanal(x, user)
        ov = 0
        tt = len(res[0])
        if res[0]:
            for cat, val in res[0].items():
                # get total values where amount is bigger than budget
                amount = val['amount']
                budget = val['budget']
                if amount > budget:
                    ov = ov +1
            ov_totals.append(ov/tt)
        else:
            # no files
            pass
    try:
        overspend_ind = sum(ov_totals)/len(ov_totals)
    except:
        overspend_ind = 0
    return overspend_ind*100
    
