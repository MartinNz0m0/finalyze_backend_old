from flask import *
import tabula
from pypdf import PdfReader
import csv
import random


# app = Flask(__name__)




# @app.route('/csv', methods=['POST'])
# def convert():
#     print(request.json)
#     pwd = request.json.get('pdfpwd')
#     name = request.json.get('fileselected')
  
#     # pdf_path = request.json.get('filepath')or './uploads'
#     pdf_path = './uploads'
    
#     try:
#         reader = PdfReader(request.json.get('filepath'))
#         reader.decrypt(pwd)
#         print(len(reader.pages))
#         pages = len(reader.pages)
#         first = tabula.convert_into(request.json.get('filepath'), f'./uploads/{name}f.csv', output_format='csv',
#                             pages='1', lattice=True, guess=False, area=[211.68, 33.12, 314.64, 558.72], password=pwd)
#         table = tabula.convert_into(request.json.get('filepath'), f'./uploads/{name}.csv', output_format='csv',
#                             pages='1', lattice=True, guess=False, area=[334.08, 33.12, 711.36, 558.72], password=pwd)
#         other = tabula.convert_into(request.json.get('filepath'), f'./uploads/{name}t.csv', output_format='csv',
#                             pages=f'2-{pages}', lattice=True, guess=False, area=[58.32, 33.12, 711.36, 558.72], password=pwd)
#     except Exception as e:
#         print(e)
#         return jsonify({'error': str(e)})
    
#     return jsonify({'s': 'Success'})

# if __name__=='__main__':
#     app.run(debug=True, port=8001)


# making a demo account for demo purposes

# edit an existing csv, replace real names with fake names

# make a new csv with fake names

fake_names = ['775 Mama Chai', '889 Gaddafi Ndungu', '420 Kevin Fisi', '512 Mary Madeni', '254 Fatma Sokoni', '663 Grace Kibarua', '985 Shadrack Jembe', '546 Simba Kiboko']
fake_till = ['6523154 Kwa Base Wines', '6548965 Drinking Water Investments', '785424 Kitu Nzito Gen Shop', '985632 Peter Mutura na Supu', '658796 Kila Kitu Online Store']
fake_pbill = ['986523 Online Store Ingine', '875256 Airtel Airtime Purchase', '985447 Kenya Power Payment', '9854562 DSTV Pia Muhimu', '87542 Betting site ya Kiboko', '854696 Betting site ingine']
fake_wdraw = ['25632 Toa Pesa Hapa', '985481 Withdraw Cash Here', '4200521 ATM Withdrawal']
fake_dep = ['Betting site ya Kiboko', 'COOP Bank to Mpesa', 'Equity Bank to Mpesa']

def rndgen():
    return random.randint(0, 9)

rows = []
with open('./uploads/MPESA_Statement_2023-04-01_to_2023-05-01_2547xxxxxx607.pdf.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
    
        # push header to rows
        if row[0] == 'Date':
            rows.append(row)
            continue
        # replace names with fake names
        if row[2].startswith('Customer Transfer to'):
            row[2] = f'Customer Transfer to - 2547******' + random.choice(fake_names)
        elif row[2].startswith('Customer Transfer Fuliza MPesa'):
            row[2] = f'Customer Transfer Fuliza MPesa to - 2547******' + random.choice(fake_names)
        elif row[2].startswith('Merchant Payment to') or row[2].startswith('Merchant Payment Online'):
            row[2] = f'Merchant Payment to - ' + random.choice(fake_till)
        elif row[2].startswith('Merchant Payment Fuliza M-Pesa'):
            row[2] = f'Merchant Payment Fuliza M-Pesa to - ' + random.choice(fake_till)
        elif row[2].startswith('Pay Bill to') or row[2].startswith('Pay Bill Online'):
            row[2] = f'Pay Bill to - ' + random.choice(fake_pbill)
        elif row[2].startswith('Pay Bill Fuliza M-Pesa'):
            row[2] = f'Pay Bill Fuliza M-Pesa to - ' + random.choice(fake_pbill)
        elif row[2].startswith('Business Payment from'):
            row[2] = f'Business Payment from - ' + random.choice(fake_dep)
        elif row[2].startswith('Customer Withdrawal'):
            row[2] = f'Customer Withdrawal At Agent Till - ' + random.choice(fake_wdraw)
        elif row[2].startswith('Funds received'):
            row[2] = f'Funds received from - 2547******' + random.choice(fake_names)
        else:
            pass
        # write to new csv
        rows.append(row)

with open('./uploads/demo-mpesa1.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(rows)


# # for bank statements
# with open('./uploads/AccountStatement36653223_01MAY2023_21411314.pdf.csv', 'r') as t:
#     reader = csv.reader(t)
#     rows = []
#     for row in reader:
#         spl = row[2].split(' ')
#         if 'TRANSFER' in spl:
#             spl[-1] = f'2547{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}'
#             new_row = ' '.join(spl)
#             print(new_row)
#             rows.append([row[0], row[1], new_row, row[3], row[4], row[5], row[6]])
#         elif 'SAFARICOM' in spl:
#             new_row = 'SAFARICOM MPESA Charges'
#             rows.append([row[0], row[1], new_row, row[3], row[4], row[5], row[6]])
#         else:
#             rows.append(row)

# with open('./uploads/demo-coop.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows(rows)

# with open('./uploads/equitydemo.csv', 'r') as p:
#     reader = csv.reader(p)
#     rows = []
#     for row in reader:
#         if row[1].startswith('MPS'):
#             row[1] = f'MPS Deposit from 2547{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()} {random.choice(fake_names)}'
#             rows.append(row)
#             print(row)
#         elif row[1].endswith('MPESA'):
#             row[1] = f'MPESA Transfer to 2547{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()}{rndgen()} {random.choice(fake_names)}'
#             rows.append(row)
#             print(row)
#         else:
#             rows.append(row)

# with open('./uploads/demo-equity.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows(rows)
        
           