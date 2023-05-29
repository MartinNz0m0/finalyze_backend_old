import pandas as pd


def pandasanal():


    # module for pandas analysis
    df = pd.read_csv(
        './uploads/MPESA_Statement_2023-02-01_to_2023-02-27_2547xxxxxx607.pdf.csv')
    df.fillna(0, inplace=True)
    df.replace('\r', ' ', regex=True, inplace=True)


    # sort = df.sort_values(by=['Withdrawn'], ascending=False)

    remw = df.loc[df.Withdrawn != "Withdrawn"].copy()
    remw['Withdrawn'] = remw.Withdrawn.str.replace("-", "", regex=False)
    remw['Withdrawn'] = remw.Withdrawn.str.replace(",", "", regex=False)
    remw['Withdrawn'] = remw['Withdrawn'].fillna(0).astype(float)
    num = remw['Withdrawn'].sum()

    # cponvert paid in numbers to float
    remw['Paid In'] = remw['Paid In'].str.replace(",", "", regex=False)
    remw['Paid In'] = remw['Paid In'].fillna(0).astype(float)
    # convert to int

    # groupings the
    group = remw.groupby('Details')
    # group = remw.groupby('Details').agg({'Withdrawn': ['sum', 'size']}).sort_values(('Withdrawn', 'size'), ascending=False)
    # print(group)
    # largest withdrawal in each group
    max_withdrawal = remw.groupby('Details')["Withdrawn", "Paid In"].max().tail(10)
    count = remw.groupby('Details')["Withdrawn"].size(
    ).sort_values(ascending=False).head(10)
    # sum of all paid in groups
    group_paid_in = remw.groupby('Details').agg(
        {'Paid In': ['sum', 'size']}).sort_values(('Paid In', 'size'), ascending=False)
    group_paid_in.loc[:, ('Paid In', 'count')
                    ] = group_paid_in.loc[:, ('Paid In', 'size')]

# wrap in try catch
    try:

        # get transcation charges groups
        sndmoneycosts = group.get_group('Customer Transfer of Funds Charge')
        # print(sndmoneycosts['Withdrawn'].agg(['sum', 'size', 'mean', 'std', 'min', 'max']))

        # get costs for paybill costs
        paybillcosts = group.get_group('Pay Bill Charge')
        # print(paybillcosts['Withdrawn'].agg(['sum', 'size', 'mean', 'std', 'min', 'max']))
        max = paybillcosts['Withdrawn'].max()
        id = paybillcosts['Withdrawn'].idxmax()+1
        dets = df.loc[id, 'Details']
        pbamount = df.loc[id, 'Withdrawn']
        # print(dets)

        # get costs for withdraw costs
        withdrawalcosts = group.get_group('Withdrawal Charge')
        # print(withdrawalcosts['Withdrawn'].agg(['sum', 'size', 'mean', 'std', 'min', 'max']))
        withdrawid = withdrawalcosts['Withdrawn'].idxmax()+1
        withdrawdets = df.loc[withdrawid, 'Details']
        withdrawamount = df.loc[withdrawid, 'Withdrawn']
        # print(withdrawdets)

        # get airtime purchases
        airtimes = group.get_group('Airtime Purchase')
        aitimeid = airtimes['Withdrawn'].idxmax()
        airtimecount = airtimes['Withdrawn'].agg(['size'])
        # print(airtimecount)

        # get costs for till charges
        tillcosts = group.get_group('Pay Merchant Charge')
        # print(tillcosts['Withdrawn'].agg(['sum', 'size', 'mean', 'std', 'min', 'max']))
        tillid = tillcosts['Withdrawn'].idxmax()+1
        tilldets = df.loc[tillid, 'Details']
        tillamount = df.loc[tillid, 'Withdrawn']


    except Exception as exception:
        # print('no costs')
        # print(exception)
        pass
