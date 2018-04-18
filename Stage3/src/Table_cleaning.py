import csv
import re

ID_num = 0
with open('Table_IMDB.csv','r') as csvinput:
    with open('Table_IMDB_with_ID3.csv', 'w') as csvoutput:
#with open('Table_Allmovie.csv','r') as csvinput:
#    with open('Table_Allmovie_with_ID3.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)
#MID,Title,Certificate,Genre,Rating,Running Time,Directors,Writers,Stars Cast,Country,Language,Budget,Gross,Release Date,Production Company
        ID = 0
        for row in csv.reader(csvinput):


            if ID == 0:
                mid = "MID"
            else:
                mid = ID
            ID = ID + 1
            release_month = ""
            #REMOVE 'NULL' value
            for i in range(14):
                if row[i]=='NULL':
                    row[i] = ''
            release = row[12]


            #fixing Certificate
            row[1] = row[1].replace("-", "")

            #fixing Running Time
            min1 = 0
            min2 = 0
            m = re.match(".* (\d+)min", row[4])
            if m:
                min2 = int(m.group(1))
            m1 = re.match("^(\d+).?min", row[4])
            if m1:
                min2 = int(m1.group(1))
            m0 = re.match("(\d+)h", row[4])
            if m0:
                min1 = int(m0.group(1))*60
            if row[0] != "Title":
                row[4] = str(min1+min2)+" min"

            #fixing Release Date
            #for AllMovie release date format
            r = re.match("(\w+ )(\d+).*(\d\d\d\d).*", row[12])
            if r:
                mon = ["Jan ", "Feb ", "Mar ", "Apr ", "May ", "Jun ", "Jul ", "Aug ", "Sep ", "Oct ", "Nov ", "Dec "]
                month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                for i in range(12):
                    if r.group(1)==mon[i]:
                        release = r.group(2) + " " + month[i] + " " + r.group(3)
                        release_month = month[i]

            #for IMDB Release date format
            r1 = re.match("(\d+ )(\w+).*(\d\d\d\d).*", row[12])
            if r1:
                release = r1.group(1) + r1.group(2) + " " + r1.group(3)
                release_month = r1.group(2)

            #for Release year
            if row[0] == "Title":
                year = "Release Year"
            else:
                year = ""
            r2 = re.match(".*(\d\d\d\d).*", row[12])
            if r2:
                year = r2.group(1)

            #for Release month
            if row[0] == "Title":
                release_month = "Release Month"
            writer.writerow((mid, row[0], row[1], row[2], row[3], row[4], row[5], row[7], row[8], release, row[13], year, release_month))
