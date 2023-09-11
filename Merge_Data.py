from Web_Cost_Index import data
from Map import master

# Spalten leere, da hier Daten von numbeo oder Abfrage rein sollen
master['Kosten Food'] = 0
master['Kosten Leben'] = 0
master['Interesse'] = 0
master['Score'] = 0

for  index, row in master.iterrows():
    y = master.at[index, "Stadt/Region"]
    print(f"Put in your interest for location: {y}. (Score 1 to 10) ")
    x = input()
    master.at[index,'Interesse'] = float(x)

data = data.set_index("Stadt")
master = master.set_index("Stadt/Region")

for index, row in master.iterrows(): # Füge die Spaltenwerte aus data in die entsprechenden Stellen in master ein
    try:
        master.at[index,'Kosten Food'] = data.loc[index, "Lebensmittel-Index"]
        master.at[index,'Kosten Leben'] = data.loc[index, "Lebenshaltungskosten-Index"]
    except(KeyError):
        pass

for index, row in master.iterrows(): # Berechne einen Score
    if (row['Interesse'] != 0 and row["Kosten Food"] != 0 and row["Kosten Leben"] != 0):
       master.at[index,'Score'] = round(row['Interesse']/10*1/(row["Kosten Food"] + row["Kosten Leben"])*10000,2)
    else:
       master.at[index,'Score'] = 0


#next up
#1. Anhand meiner Interesseeingabe neuen Score berechnen und plotten DONE
#2. Fragebogen für Interesse erstellen
#3. Datensatz zu bisherigen Städten verbessern