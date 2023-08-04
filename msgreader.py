import re
import csv
import datetime
import dbquery
import pandas as pd

msg = [{'body': 'RGV5VROQXJ Confirmed. Ksh200.00 paid to Msafiri butchery. on 31/7/23 at 4:15 PM.New M-PESA balance is Ksh1,274.01. Transaction cost, Ksh0.00. Amount you can transact within the day is 298,685.00. To move money from bank to M-PESA, dial *334#>Withdraw>From bank to MPESA',
        'date': '2023-07-31 16:52:58.778'}, 
        {'body': 'RH292Q2VCV Confirmed.You have received Ksh100.00 from GEORGE  MUITA 0711326005 on 2/8/23 at 4:09 PM  New M-PESA balance is Ksh100.00. Register for lipa na M-PESA till for free today. Click https://m-pesaforbusiness.co.ke/LNM/', 'date': '2023-07-25 19:26:56.053'}, 
        {'body': 'RH13YGJIUB Confirmed. Ksh500.00 sent to Anna  Mutinda 0748328395 on 1/8/23 at 2:27 PM. New M-PESA balance is Ksh767.01. Transaction cost, Ksh7.00. Amount you can transact within the day is 299,500.00. Dial *234*0# to check your FULIZA LIMIT.', 'date': '2023-07-31 16:52:58.778'},
        {'body': 'RGU9T1EY8D Confirmed. Ksh11,000.00 sent to Co-operative Bank Money Transfer for account 01109212586000 on 30/7/23 at 4:51 PM New M-PESA balance is Ksh2,602.01. Transaction cost, Ksh57.00.Amount you can transact within the day is 288,200.00. Pay your water/KPLC bill conveniently using M-PESA APP or use Paybill option on Lipa Na M-PESA.', 'date': '2023-07-31 16:52:58.778'}
        ]


def mpesa_msgreader(file):
    # loop through the list and check regex
    final = []
    regex_pattern_till = r'([A-Z0-9]+) Confirmed\. Ksh(\d+\.\d{2}) paid to ([A-Za-z0-9\s]+)\. on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\.New M-PESA balance is Ksh(\d+\,\d+\.\d{2})\. Transaction cost, Ksh(\d+\.\d{2})\. Amount you can transact within the day is (\d+\,\d+\.\d{2})\.'
    regex_pattern_rec = r'([A-Z0-9]+) Confirmed\.You have received Ksh(\d+\.\d{2}) from ([A-Za-z\s]+)\s+(\d{10}) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)  New M-PESA balance is Ksh(\d+\.\d{2})\.'
    regex_pattern_snd = r'([A-Z0-9]+) Confirmed\. Ksh(\d+\.\d{2}) sent to ([A-Za-z\s]+)\s+(\d{10}) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\. New M-PESA balance is Ksh(\d+\.\d{2})\. Transaction cost, Ksh(\d+\.\d{2})\. Amount you can transact within the day is (\d+\,\d+\.\d{2})\.'
    regex_pattern_pbill = r'([A-Z0-9]+) Confirmed\. Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) sent to ([A-Za-z\s-]+) for account (\d+) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+) New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\.Amount you can transact within the day is (\d{1,3}(?:,\d{3})*\.\d{2})\.'
    for i in range(len(msg)):
        if 'received' in msg[i]['body']: # TODO: check for failed, cancelled and fuliza transcations
            match = re.match(regex_pattern_rec, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                sender = match.group(3)
                sender_phone = match.group(4)
                date = match.group(5)
                time = match.group(6)
                new_balance = match.group(7)
            # print(transaction_id, amount, sender, sender_phone, date, time,
            #       new_balance)
            if mpesa_check_csv(transaction_id, sender ,file):
                print('skipping')
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Received from {sender} {sender_phone}",
                'Paid In': amount,
                'Paid Out': 0,
                'Balance': new_balance
            }
            final.append(obj)
        elif 'sent to' in msg[i]['body'] and 'for account' not in msg[i]['body']:
            match = re.match(regex_pattern_snd, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3)
                recipient_phone = match.group(4)
                date = match.group(5)
                time = match.group(6)
                new_balance = match.group(7)
                transaction_cost = match.group(8)
            # print(transaction_id, amount, recipient, recipient_phone, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient ,file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Send money {recipient} {recipient_phone}",
                'Paid In': 0,
                'Paid Out': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Paid Out': transaction_cost,
                    'Balance': new_balance
                })
        elif 'for account' in msg[i]['body']:
            match = re.match(regex_pattern_pbill, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3)
                recipient_account = match.group(4)
                date = match.group(5)
                time = match.group(6)
                new_balance = match.group(7)
                transaction_cost = match.group(8)
            # print(transaction_id, amount, recipient, recipient_account, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient ,file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Pay Bill to {recipient} {recipient_account}",
                'Paid In': 0,
                'Paid Out': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Paid Out': transaction_cost,
                    'Balance': new_balance
                })
        else:
            match = re.match(regex_pattern_till, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3)
                date = match.group(4)
                time = match.group(5)
                new_balance = match.group(6)
                transaction_cost = match.group(7)
            # print(transaction_id, amount, recipient, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient ,file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Buy goods {recipient}",
                'Paid In': 0,
                'Paid Out': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Paid Out': transaction_cost,
                    'Balance': new_balance
                })
    print(final)
    return final



def mpesa_csvwriter(file, user):
    data = mpesa_msgreader(file)
    if not data:
        return
        print('No new data')
    else:
        with open(f'uploads/{file}', 'w') as csvfile: # TODO: add change file name and add date to database
            fieldnames = ['Receipt No', 'Completion Time', 'Details', 'Paid In', 'Paid Out', 'Balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(data)):
                writer.writerow(data[i])
        date = datetime.datetime.now()
        res = dbquery.update_last_sync(user, date)
        return res

# def mpesa_check_csv(rcpt, det ,file):
#     try:
#         with open(f'uploads/{file}', 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 print(row)
#                 if row['Receipt No'] == rcpt:
#                     #print(row['Receipt No'], rcpt, det)
#                     return True
#             return False
#     except FileNotFoundError:
#         print('File not found')
#         return False

def mpesa_check_csv(rcpt, det, file):
    try:
        f = pd.read_csv(f'uploads/{file}')
        df = pd.DataFrame(f)
        rec = df['Receipt No']
        #print(rec)
        for i in range(len(rec)):
            if rec[i] == rcpt:
                return True
        return False
    except FileNotFoundError:
        print('File not found')
        return False
        
    

mpesa_csvwriter('mpesa.csv', 'marto')