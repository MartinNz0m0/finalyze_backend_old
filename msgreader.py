import re
import csv
import datetime
import os
import dbquery
import pandas as pd




def mpesa_msgreader(msg, file):
    # loop through the list and check regex
    final = []
    fuliza = []
    regex_pattern_till = r'([A-Z0-9]+) Confirmed\. Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) paid to ([A-Za-z0-9\s./*()-]+) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\.New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Amount you can transact within the day is (\d{1,3}(?:,\d{3})*\.\d{2})\.'
    regex_pattern_rec = r'([A-Z0-9]+) Confirmed\.You have received Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) from ([A-Za-z0-9\s-]+) ([0-9]+)? on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)(?:\s)*New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\.'
    regex_pattern_snd = r'([A-Z0-9]+) Confirmed\. Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) sent to ([A-Za-z\s]+)\s+(\d{10}) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\. New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Amount you can transact within the day is (\d+\,\d+\.\d{2})\.'
    regex_pattern_pbill = r'([A-Z0-9]+) Confirmed\. Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) sent to ([A-Za-z\s\-()]+(?: \d+)?) for account ([A-Za-z0-9\s\-()*!?]+) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+) New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\.'
    regex_pattern_pbill_airtime = r"([A-Z0-9]+) Confirmed\. Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) sent to ([A-Za-z\s\-()]+(?: \d+)?) for account on (\d+/\d+/\d+) at (\d+:\d+\s+[APM\.]+) New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\."
    regex_pattern_airtime = r'([A-Z0-9]+) confirmed\.You bought Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) of airtime for ([0-9]+) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\.New  balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Amount you can transact within the day is (\d{1,3}(?:,\d{3})*\.\d{2})\.'
    regex_pattern_wdraw = r"([A-Z0-9]+) Confirmed\.on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)Withdraw Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) from (\d+)\s-\s([A-Za-z0-9\s-]+) New M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Transaction cost, Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\. Amount you can transact within the day is (\d{1,3}(?:,\d{3})*\.\d{2})\."
    regex_pattern_mshwari_wdraw = r"([A-Z0-9]+) Confirmed\.Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) transferred from ([A-Za-z0-9\s-]+) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\. ([A-Za-z0-9\s-]+) balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\s?.*?M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\s?.*?Transaction cost Ksh\.(\d+\.\d{2})"
    regex_pattern_mshwari_dep = r"([A-Z0-9]+) Confirmed\.Ksh(\d{1,3}(?:,\d{3})*\.\d{2}) transferred to ([A-Za-z0-9\s-]+) on (\d+/\d+/\d+) at (\d+:\d+ [APM]+)\. ([A-Za-z0-9\s-]+) balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\s?.*?New ([A-Za-z0-9\s-]+) balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\s?.*?Transaction cost Ksh\.(\d+\.\d{2})"
    regex_pattern_fuliza_repay = r"([A-Z0-9]+)(?:\r\n|\r|\n\s)* Confirmed\. Ksh (\d{1,3}(?:,\d{3})*\.\d{2}) from your M-PESA has been used to (?:[A-Za-z\s]+) pay your outstanding Fuliza M-PESA\. (?:[A-Za-z\s]+) M-PESA limit is Ksh (\d{1,3}(?:,\d{3})*\.\d{2})\. M-PESA balance is Ksh(\d{1,3}(?:,\d{3})*\.\d{2})\."
    regex_pattern_fuliza_charged = r"([A-Z0-9]+) Confirmed\. Fuliza M-PESA amount is Ksh (\d{1,3}(?:,\d{3})*\.\d{2})\. Interest charged Ksh (\d{1,3}(?:,\d{3})*\.\d{2})\. Total Fuliza M-PESA outstanding amount is Ksh (\d{1,3}(?:,\d{3})*\.\d{2}) due on ([0-9/]+)\."
    for i in range(len(msg)):
        msg[i]['body'] = msg[i]['body'].replace('\n', ' ').replace('  ', ' ')
        # TODO: check for failed, cancelled and fuliza transcations
        if re.match(regex_pattern_mshwari_dep, msg[i]['body']):
            match = re.match(regex_pattern_mshwari_dep, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                date = match.group(4)
                time = match.group(5)
                new_balance = match.group(7)
                transaction_cost = match.group(8)
            else:
                continue
            # print(transaction_id, amount, recipient, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Deposit to {recipient}",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)
        elif re.match(regex_pattern_mshwari_wdraw, msg[i]['body']):
            match = re.match(regex_pattern_mshwari_wdraw, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                date = match.group(4)
                time = match.group(5)
                new_balance = match.group(8)
                transaction_cost = match.group(9)
            else:
                continue
            # print(transaction_id, amount, recipient, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Withdraw from {recipient}",
                'Paid In': amount,
                'Withdrawn': 0,
                'Balance': new_balance
            }
            final.append(obj)
        elif re.match(regex_pattern_fuliza_charged, msg[i]['body']):
            match = re.match(regex_pattern_fuliza_charged, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                interest = match.group(3)
                total = match.group(4)
                due_date = match.group(5)
            else:
                continue
            # print(transaction_id, amount, interest, total, due_date)
            if mpesa_check_csv(transaction_id, 'Fuliza M-PESA', file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': "Fuliza deposit",
                'Paid In': amount,
                'Withdrawn': 0,
                'Balance': f'-{total}'
            }
            final.append(obj) # change to a diff array
            fuliza.append(transaction_id)

        elif re.match(regex_pattern_fuliza_repay, msg[i]['body']):
            print(msg[i]['body'])
            match = re.match(regex_pattern_fuliza_repay, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                limit = match.group(3)
                new_balance = match.group(4)
            else:
                continue
            # print(transaction_id, amount, limit, new_balance)
            if mpesa_check_csv(transaction_id, 'Fuliza M-PESA', file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': "Fuliza repayment",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)

        elif 'received' in msg[i]['body']:
            match = re.match(regex_pattern_rec, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                sender = match.group(3).replace('  ', ' ').upper()
                sender_phone = match.group(4).replace('  ', ' ').upper()
                date = match.group(5)
                time = match.group(6)
                new_balance = match.group(7)
            else:
                continue
            # print(transaction_id, amount, sender, sender_phone, date, time,
            #       new_balance)
            if mpesa_check_csv(transaction_id, sender, file):
                print('skipping')
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Received from {sender} {sender_phone}",
                'Paid In': amount,
                'Withdrawn': 0,
                'Balance': new_balance
            }
            final.append(obj)
        elif 'sent to' in msg[i]['body'] and 'for account' not in msg[i]['body']:
            match = re.match(regex_pattern_snd, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                recipient_phone = match.group(4).replace('  ', ' ').upper()
                date = match.group(5)
                time = match.group(6)
                new_balance = match.group(7)
                transaction_cost = match.group(8)
            else:
                continue
            # print(transaction_id, amount, recipient, recipient_phone, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Send money {recipient} {recipient_phone}",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Withdrawn': transaction_cost,
                    'Balance': new_balance
                })
        elif all(x in msg[i]['body'] for x in ['sent to', 'for account']):
            match = re.match(regex_pattern_pbill, msg[i]['body'])
            safmatch = re.match(regex_pattern_pbill_airtime, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                recipient_account = match.group(4).replace('  ', ' ').upper()
                date = match.group(5)
                time = match.group(6)
                new_balance = match.group(7)
                transaction_cost = match.group(8)
            # print(transaction_id, amount, recipient, recipient_account, date, time,
            #       new_balance, transaction_cost)
            elif safmatch:
                transaction_id = safmatch.group(1)
                amount = safmatch.group(2)
                recipient = safmatch.group(3).replace('  ', ' ').upper()
                recipient_account = 'SELF'
                date = safmatch.group(4)
                time = safmatch.group(5)
                new_balance = safmatch.group(6)
                transaction_cost = safmatch.group(7)
            else:
                continue
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Pay Bill to {recipient} {recipient_account}",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Withdrawn': transaction_cost,
                    'Balance': new_balance
                })
        elif all(x in msg[i]['body'] for x in ['of airtime for']):
            match = re.match(regex_pattern_airtime, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                date = match.group(4)
                time = match.group(5)
                new_balance = match.group(6)
                transaction_cost = match.group(7)
                amount_left = match.group(8)
            else:
                continue
            # print(transaction_id, amount, recipient, date, time,
            #       new_balance, transaction_cost, amount_left)
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Buy airtime {recipient}",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Withdrawn': transaction_cost,
                    'Balance': new_balance
                })
        elif 'paid to' in msg[i]['body']:
            match = re.match(regex_pattern_till, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                date = match.group(4)
                time = match.group(5)
                new_balance = match.group(6)
                transaction_cost = match.group(7)
            else:
                continue
            # print(transaction_id, amount, recipient, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Buy goods {recipient}",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Withdrawn': transaction_cost,
                    'Balance': new_balance
                })
        elif all(x in msg[i]['body'] for x in ['Withdraw', 'from']):
            match = re.match(regex_pattern_wdraw, msg[i]['body'])
            if match:
                transaction_id = match.group(1)
                date = match.group(2)
                time = match.group(3)
                amount = match.group(4)
                recipient = match.group(5).replace('  ', ' ').upper()
                new_balance = match.group(7)    
                transaction_cost = match.group(8)
            else:
                continue
            # print(transaction_id, amount, recipient, date, time,
            #       new_balance, transaction_cost)
            if mpesa_check_csv(transaction_id, recipient, file):
                continue
            obj = {
                'Receipt No': transaction_id,
                'Completion Time': msg[i]['date'],
                'Details': f"Withdraw from {recipient}",
                'Paid In': 0,
                'Withdrawn': amount,
                'Balance': new_balance
            }
            final.append(obj)
            if transaction_cost != '0.00':
                final.append({
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': "Transaction cost",
                    'Paid In': 0,
                    'Withdrawn': transaction_cost,
                    'Balance': new_balance
                })
        else:
            continue
        # modify details for fuliza
        if i == len(msg)-1:
            print('end of list')
            print(fuliza)
            for i in range(len(fuliza)):
                for j in range(len(final)):
                    if final[j]['Receipt No'] == fuliza[i] and final[j]['Details'] not in ['Fuliza deposit', 'Transaction cost']:
                        print(final[j]['Details'])
                        stri = final[j]['Details'].split(' ')
                        # push to pos 2
                        stri.insert(2, 'fuliza')
                        final[j]['Details'] = ' '.join(stri)
    return final


def mpesa_csvwriter(file, msg, user):
    data = mpesa_msgreader(msg, file)
    exists = os.path.isfile(f'uploads/{file}')
    date = datetime.datetime.now()
    if not data:
        return
        print('No new data')
    else:
        # TODO: add change file name and add date to database
        with open(f'uploads/{file}', 'a') as csvfile:
            fieldnames = ['Receipt No', 'Completion Time',
                          'Details', 'Paid In', 'Withdrawn', 'Balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # check if header exists
            if not exists:
                writer.writeheader()
            for i in range(len(data)):
                writer.writerow(data[i])
        res = dbquery.update_last_sync(user, date)
        return res


def mpesa_check_csv(rcpt, det, file):
    try:
        f = pd.read_csv(f'uploads/{file}')
        df = pd.DataFrame(f)
        rec = df['Receipt No']
        # print(rec)
        for i in range(len(rec)):
            if rec[i] == rcpt:
                return True
        return False
    except FileNotFoundError:
        print('File not found')
        return False

# print(mpesa_msgreader(msg, 'mpesa.csv'))

def coop_msg_reader(msg):
    final = []

    reg_pattern = r'Ref:([A-Z0-9]+):.*?KES ([0-9]+) to ([A-Za-z0-9\s./*()-]+) was successful.*?MPESA Ref:([A-Z0-9]+)'
    reg_card_goods = r"Card GOODS transaction dated (\d{1,2}-[A-Z]{3}-\d{4} \d{1,2}:\d{2}:\d{2}) of ([A-Z]+) ([0-9]+)\s+([A-Za-z0-9\s./*()+.><-]+) Was Successful\."
    reg_card_cash = r"Card CASH transaction dated (\d{1,2}-[A-Z]{3}-\d{4} \d{1,2}:\d{2}:\d{2}) of ([A-Z]+) ([0-9]+)\s+([A-Za-z0-9\s./*()+.><-]+) Was Successful\."

    for i in range(len(msg)):
        if 'MPESA transfer' and 'was successful' in msg[i]:
            match = re.match(reg_pattern, msg[i])
            if match:
                transaction_id = match.group(1)
                amount = match.group(2)
                recipient = match.group(3).replace('  ', ' ').upper()
                mpesa_ref = match.group(4)
                obj = {
                    'Receipt No': transaction_id,
                    'Completion Time': msg[i]['date'],
                    'Details': f"Send money {recipient} {mpesa_ref}",
                    'Paid In': 0,
                    'Withdrawn': amount,
                    'Balance': 0
                }
                final.append(obj)