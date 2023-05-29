import pandas as pd
import dbquery
import bank

def searchfunc(query, user, sttype):
    file = dbquery.get_file_names(user, sttype)


    #search functions for all files
    searchres = []
    finalres = []
    # loop through the files and search for the query
    for x in file:
        df2 = pd.read_csv(f'./uploads/{x}.csv')
        df2.fillna(0, inplace=True)
        df2.replace('\r', ' ', regex=True, inplace=True)
        resp = df2['Details'].str.upper()
        respon = df2[resp.str.contains(query)]
        searchres.append(respon.to_dict('records'))
    # limit eh search results to 10
    for x in searchres:
        if len(x) > 10:
            x = x[:20]
            finalres.append(x)
        else:
            finalres.append(x)

    return(finalres)

def searchone(query, user ,filename):
    df = pd.read_csv(
        filename)
    df.fillna(0, inplace=True)
    df.replace('\r', ' ', regex=True, inplace=True)

    # sort = df.sort_values(by=['Withdrawn'], ascending=False)

    remw = df.loc[df.Withdrawn != "Withdrawn"].copy()
    remw['Withdrawn'] = remw.Withdrawn.str.replace("-", "", regex=False)
    remw['Withdrawn'] = remw.Withdrawn.str.replace(",", "", regex=False)
    remw['Withdrawn'] = remw['Withdrawn'].fillna(0).astype(float)
    remw['Paid In'] = remw['Paid In'].str.replace(",", "", regex=False)
    remw['Paid In'] = remw['Paid In'].fillna(0).astype(float)
    #module for search function
    #search function
   
    # get details in uppercase and compare
    resupper = remw['Details'].str.upper()
    res = remw[resupper.str.contains(query)]
    totalsent = res['Withdrawn'].sum()
    print(res, "\n" ,f"Total sent to {query}:", totalsent)
    return(res.to_dict('records'))

def coopsearchfunc(query, user, sttype):
    file = dbquery.get_file_names(user, sttype)
    #search functions for all files
    searchres = []
    finalres = []
    # loop through the files and search for the query
    try:
        for x in file:
            df2 = bank.coopstatementssearch(x)
            resp = df2['Details'].str.upper()
            respon = df2[resp.str.contains(query)]
            searchres.append(respon.to_dict('records'))
        # limit eh search results to 10
        for x in searchres:
            if len(x) > 10:
                x = x[:20]
                finalres.append(x)
            else:
                finalres.append(x)
    except Exception as e:
        print(e)
        return('No results found')
    return(finalres)

def equitysearchfunc(query, user, sttype):
    file = dbquery.get_file_names(user, sttype)

    #search functions for all files
    searchres = []
    finalres = []
    # loop through the files and search for the query
    try:
        for x in file:
            df2 = bank.equitystatementsearch(x)
            resp = df2['Details'].str.upper()
            respon = df2[resp.str.contains(query)]
            searchres.append(respon.to_dict('records'))
        # limit eh search results to 10
        for x in searchres:
            if len(x) > 10:
                x = x[:20]
                finalres.append(x)
            else:
                finalres.append(x)
        return(finalres)
    except Exception as e:
        print(e)
        return('No results found')