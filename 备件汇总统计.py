import csv


f = open("input.csv")
fw = open("output.csv", "w")
reader = csv.reader(f)
writer = csv.writer(fw)
d = dict()


for r in reader:
    print(r)
    if not d.get(r[1]):
        d[r[1]] = [r[0],r[1],r[2],r[3],float(r[4]),r[5]+':'+str(r[4])]
     else:
        d[r[1]][4] += float(r[4])
        d[r[1]][5] += '-'+r[5]+':'+str(r[4])
		
writer.writerows(d.values())


f.close()
fw.close()