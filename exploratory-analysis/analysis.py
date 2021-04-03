import pandas as pd
import numpy as np 
import os
from tabulate import tabulate
from matplotlib import pyplot as plt

#Critical keys for data: 
# FTHG, FTAG : maç sonucu goller FTDif
# HTHG, HTAG : ilk yarı goller HTDif
# SHHG, SHAG : ikinci yarı goller SHDif
# BbAvH : Ev sahibinin kazanma ortalama bahsi
# BbAvD : Beraberlik ortalama bahsi
# BbAvA : Deplasman takımı kazanma ortalama bahsi
# BbAv>2.5 : üst bahsi
# BbAv<2.5 : alt bahsi


os.chdir(r"C:\Users\oseker16\Documents\vs studio\soccer research\explanatory analysis")

data_bySeasons = list() #indexed with seasons 
data_byLeagues = list() #indexed with leagues

leagues = ['E0',
 'D1',
 'SP1',
 'I1',
 'F1',
 'B1',
 'N1',
 'P1',
 'T1',
 'G1']
seasons = ['2018-2019',
 '2017-2018',
 '2016-2017',
 '2015-2016',
 '2014-2015',
 '2013-2014',
 '2012-2013',
 '2011-2012',
 '2010-2011',
 '2009-2010',
 '2008-2009']

def readData():

    for s in seasons:
        name = "sezon" + s + ".csv"
        df = pd.read_csv(name)
        df["Season"] = s
        data_bySeasons.append(df)

    for l in leagues:
        name = "lig" + l + ".csv"
        df = pd.read_csv(name)
        data_byLeagues.append(df)

    data_all = pd.concat(data_bySeasons)
    return data_all

data_all = readData()
keys1 = ['FTHG','FTAG','HTHG','HTAG','SHHG', 'SHAG']



def describeDFkeys(df, keys):

    res = list()
    for s in keys:
        res.append( round(df[s].mean(),3) )
        res.append( round(df[s].std(),3))

    return res

def tablebyLeagueSeason(keys):
    names = list()
    names.append("lig/sezon")
    for s in keys:
        names.append(s + " mean")
        names.append(s + " std")

    vals = list()
    for i in range(len(seasons)):
        df = data_bySeasons[i]
        name = seasons[i]
        gd = describeDFkeys(df, keys)
        gd.insert(0, name)
        vals.append(gd)

    table = tabulate(vals, headers=names)

    file = open('table_seasons.txt','w')
    file.write(str(table))
    file.close()
        

    vals = list()
    for i in range(len(leagues)):
        df = data_byLeagues[i]
        name = leagues[i]
        gd = describeDFkeys(df, keys)
        gd.insert(0, name)
        vals.append(gd)

    table = tabulate(vals, headers=names)

    file = open('table_leagues.txt','w')
    file.write(str(table))
    file.close()

def tablebydata(keys, data):
    names = list()
    for s in keys:
        names.append(s + " mean")
        names.append(s + " std")

    vals = list()
    for i in range(len(data)):
        df = data[i]
        gd = describeDFkeys(df, keys)
        vals.append(gd)

    table = tabulate(vals, headers=names)

    return table

def allseasonsaslistforleague(leag):
    data = list()
    for df in data_bySeasons:   
        data.append(df[df['Div']==leag])
    return data

def tablebyleaguelistseasontable(league_list, keys):

    file = open("tabletest.txt", 'w')
    for lig in league_list:
        yaz = tablebydata(keys, allseasonsaslistforleague(lig))
        file.write("***** " + lig + " *****" + "\n")
        file.write(yaz)
        file.write("\n")

    file.close()

keys2 = ['SHHG', 'SHAG', 'SHDif']
i = 0
file = open('testtable.txt', 'w')

for df in data_byLeagues:

    datas = list()
    datas.append(df)
    datas.append(df[df['HTDif']==0])

    datas.append(df[df['HTDif']==1])

    datas.append(df[df['HTDif']==-1])
    datas.append(df[df['HTDif']==2])
    datas.append(df[df['HTDif']==-2])
    file.write("**** " + leagues[i] + " ***** \n")
    file.write(tablebydata(keys2,datas))
    file.write("\n")
    file.write("older season \n")
    i=i+1
file.close()


def KeyandValueGoalGraphs(att, val):
    
    data = data_all[data_all[att] == val]
    keys1 = ['FTHG','FTAG','HTHG','HTAG','SHHG', 'SHAG']
    for key in keys1:
        probs = []
        values = []
        for x in range(int(data_all[key].max()) + 1 ):
            probs.append( len(data_all[data_all[key] == x]) / len(data_all))
            values.append(x)

        fig, axes = plt.subplots()
        axes.set_title(key + "given " + att + " is " + str(val))
        axes.bar(values, probs, align="center")
    return probs

def tableprobsforkeyandvalue (att, val):
    data = data_all[data_all[att] == val]
    keys1 = ['FTHG','FTAG','HTHG','HTAG','SHHG', 'SHAG']
    prob = list()
    for key in keys1:
        probs = []
        values = []
        for x in range(int(data_all[key].max()) + 1 ):
            probs.append( len(data_all[data_all[key] == x]) / len(data_all))
            values.append(x)

        prob.append(probs)
        fig, axes = plt.subplots()
        axes.set_title(key + "given " + att + " is " + str(val))
        axes.bar(values, probs, align="center")

def DataSelection(data, keys, values):
    df = data
    i = 0
    for key in keys:
        if type(values[i]) == list:
            df1 = pd.DataFrame()
            for val in values[i]:
                df1 = pd.concat([df[df[key] == val],df1])
            df = df1
        else: df = df[df[key] == values[i]]
        i = i + 1
    return df


def ConditionalProbTabulate(data, key_prob, key_cond):
    vals_prob = data_all[key_prob].dropna().unique()
    vals_cond = data_all[key_cond].dropna().unique()
    vals_cond = sorted(vals_cond, key= lambda row: abs(row))
    vals_prob = sorted(vals_prob, key= lambda row: abs(row))
    probs = list()
    names = list()
    names.append("conditions")
    p1 = list()
    p1.append("priors")
    for val in vals_prob:
        p1.append(np.round(len(data[data[key_prob]==val])/len(data),3))
        names.append("p("+key_prob+"="+str(val)+")")
    probs.append(p1)

    for val_cond in vals_cond:
        dat = DataSelection(data, [key_cond], [val_cond])
        p1 = list()
        p1.append(key_cond+"="+str(val_cond))
        for val in vals_prob:
            p1.append(np.round(len(dat[dat[key_prob]==val])/len(dat),3))
        probs.append(p1)
    
    table = tabulate(probs, headers=names)
    return table

def ConditionalProbGraphforCond(data, key_prob, key_cond):
    vals_prob = data[key_prob].dropna().unique()
    vals_cond = data[key_cond].dropna().unique()
    vals_cond = sorted(vals_cond, key= lambda row: abs(row))
    vals_prob = sorted(vals_prob, key= lambda row: abs(row))

    fig, axes = plt.subplots()
    axes.set_title("priors for " + key_prob + "  ; n=" + str(len(data)))
    axes.set(xticks=vals_prob)
    axes.hist(data[key_prob], bins= np.arange(min(vals_prob)-0.5, max(vals_prob) + 0.5, 1), density = True, align= 'mid', rwidth= 0.75)


    for val_cond in vals_cond:
        dat = DataSelection(data, [key_cond], [val_cond])
        n = len(dat)
        if n > 40: 
            fig, axes = plt.subplots()
            axes.set_title("prob of " + key_prob + " for given " + key_cond + "="+ str(val_cond)+ "  ; n=" + str(n))
            axes.set(xticks=vals_prob)
            axes.hist(np.array(dat[key_prob]).astype(int), bins= np.arange(min(vals_prob)-0.5, max(vals_prob) + 0.5, 1), density = True, align= 'mid', rwidth= 0.75)

    
ConditionalProbGraphforCond(data_all, "SHDif", "HTDif")

def ConditionalProbGraphforProb(data, key_prob, key_cond):
    vals_prob = data[key_prob].dropna().unique()
    vals_cond = data[key_cond].dropna().unique()
    vals_cond = sorted(vals_cond, key= lambda row: abs(row))
    vals_prob = sorted(vals_prob, key= lambda row: abs(row))
    probs = list()
    for valp in vals_prob:
        probs.append(list())
    for valc in vals_cond:
        dat = DataSelection(data, [key_cond], [valc])
        for i in range(len(vals_prob)):
            valp = vals_prob[i]
            p = len(dat[dat[key_prob]==valp])/len(dat)
            probs[i].append(p)
    
    for i in range(len(vals_prob)):
        valp = vals_prob[i]
        name = "P(" + key_prob + "=" + str(valp)+") for given " + key_cond + "=x"
        fig, axes = plt.subplots()
        axes.set_title(name)
        axes.set(xticks=vals_cond)
        axes.scatter(vals_cond, probs[i])

ConditionalProbGraphforProb(data_all, "SHDif", "HTDif")

table = ConditionalProbTabulate(data_all, "FTDif", "HTDif")

file = open('testtable.txt', 'w')
file.write(table)
file.close()
key_cond = "FTDif"
key_prob = "HTDif"



names_c.append("p("+key_prob+"="+str(val)+")")



