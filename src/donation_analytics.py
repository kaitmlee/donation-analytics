# -*- coding: utf-8 -*-
import sys
import pandas as pd

def scan(donors, percentile):
    #Add name/zipcode: first year to dict. 
    #check if they are there already update year if out of order
    lines = []
    unique_donors = dict()
    #Iterate through df to add all unique donors to list
    for index, row in donors.iterrows():
        #already in list
        if (row["NAME"], row["ZIP_CODE"]) in unique_donors:
            #if year2<year1 then update value in dict/drop row from df.
            if(row["TRANSACTION_DT"]<unique_donors[row["NAME"], row["ZIP_CODE"]]):
                unique_donors[row["NAME"], row["ZIP_CODE"]] = row["TRANSACTION_DT"]
                donors.drop(index, inplace=True)
            #otherwise there needs to be output
            else:
                lines.append(output(donors, index, percentile))
        #not a repeat, add to list, drop row from df
        else: 
            unique_donors[row["NAME"], row["ZIP_CODE"]] = row["TRANSACTION_DT"]
            donors.drop(index, inplace=True)
    return lines

def find_percentile(amounts, percentile):
    #find the rank
    rank = int(((percentile/100) * len(amounts) + 0.5))
    if(rank==0):
        #amount should be rounded to nearest dollar
        return int(amounts[0] + 0.5)
    else: return int(amounts[rank-1] + 0.5)

def output(donors, index, percentile):
    recip = donors.loc[index,"CMTE_ID"]
    zipcode = donors.loc[index,"ZIP_CODE"]
    year = donors.loc[index,"TRANSACTION_DT"]
    amounts = []
    #getting a list of relevent amounts
    for i, row in donors.iterrows():
        #don't need the whole df
        if (i <= index):
            #calc values from same zip and year
            if(row["ZIP_CODE"] == zipcode and row["TRANSACTION_DT"] == year):
                #add to list of donation amounts
                amounts.append(row["TRANSACTION_AMT"])
        else: break
    perc = find_percentile(amounts, percentile)
    amt = int(sum(amounts) + 0.5)
    cnt = len(amounts)
    return str("{0}|{1}|{2}|{3}|{4}|{5}".format(recip,zipcode,
               year,perc,amt,cnt))

def cleanData(donors):
    #OTHER_ID SHOULD BE NULL
    donors = donors[donors.OTHER_ID.isnull()]
    #DROP ROW IF ANY OTHER VALUE IS NULL
    donors.dropna(subset=["CMTE_ID", "NAME", "ZIP_CODE", "TRANSACTION_DT",
                      "TRANSACTION_AMT"])
    #ZIP CODE SHOULD BE AT LEAST 5 DIGITS
    donors = donors[donors["ZIP_CODE"].apply(lambda x: len(str(x))>4)]
    #CHANGE ZIPCODE TO 5 DIGITS
    donors.ZIP_CODE = donors.ZIP_CODE.astype(str).str.slice(0, 5)
    #DATE SHOULD BE AT LEAST 6 DIGITS FOR MM/DD/YYYY
    donors = donors[donors["TRANSACTION_DT"].apply(lambda x: len(str(x))==8)]
    #DATE IS CHANGED TO YYYY
    donors.TRANSACTION_DT = donors.TRANSACTION_DT.astype(str).str.slice(-4)
    return donors

def main(argv):
    itcont, perc, out = argv 
    
    percentile = int(open(perc, "r").read())
    
    donors = pd.read_csv(itcont, sep="|", 
                         header=None,
                         converters={10: lambda x: str(x),
                                     13: lambda x: str(x)},
                         usecols=[0,7,10,13,14,15])
    donors.columns = ["CMTE_ID", "NAME", "ZIP_CODE", "TRANSACTION_DT",
                      "TRANSACTION_AMT", "OTHER_ID"]
    donors = cleanData(donors)

    lines = scan(donors, percentile)

    with open(out, 'w') as output:
        output.write('\n'.join(lines))
    
if __name__ =="__main__":
    main(sys.argv[1:])
