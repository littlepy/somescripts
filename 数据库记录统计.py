import subprocess
import calendar
import sys
import csv


#返回从数据库查到的数据, type:list
def query(sql):
    result = subprocess.Popen(sql, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    err = result.stderr.read()
    if err:
        print err
        sys.exit(1)
    data = result.stdout.readlines()
    data = [i.strip() for i in data if i and i.strip()]
    data = [i.split('\xa9\xa7') for i in data]
    data = [[i.strip() for i in j if i and i.strip()] for j in data]
    return data

#返回SQL查询语句, type:str
def sqlgen(daylist, sql):
    for _ in daylist:
        yield sql.format(_[0], _[1])


#返回每个月第一天和最后一天的日期，type:tuple
def dategen(year, month_counts):
    for _ in range(1, month_counts+1):
        month = '0'+str(_) if _<10 else str(_)
        firstday = str(year) + month + '01'
        lastday = str(year)+month+str(calendar.monthrange(year, _)[1])
        yield (firstday, lastday)


#将查询结果写入csv文件
def main(year, month_counts):
    sql = '''dbtools "select notetype, name, s.amtcounts, s.counts from noteinfo, (select notetype as mynote, count(*) as counts, sum(settlamt) as amtcounts from hisdb..trnjour where clearstate='C' and workdate between '{0}' and '{1}' group by notetype) as s where noteinfo.notetype=s.mynote"'''
    daylist = dategen(year, month_counts)
    anoterdaylist = dategen(year, month_counts)
    with open('calresult.csv', 'wb') as f:
        writer = csv.writer(f)
        for sql in sqlgen(daylist, sql):
            data = query(sql)
            writer.writerow([anoterdaylist.next(), 'notename', 'settlamt', 'bill_counts'])
            writer.writerows(data)


if __name__ == '__main__':
    main(2015, 6)