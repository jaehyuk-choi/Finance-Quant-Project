# 오라클 연동 및 접속
import cx_Oracle
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# load sql to python
dsn=cx_Oracle.makedsn('localhost',1521,'xe')
cx_Oracle.init_oracle_client(lib_dir="/Volumes/instantclient-basic-macos.x64-19.8.0.0.0dbru")
conn = cx_Oracle.connect('QUANT_PROJECT/ORACLE@localhost:1521/xe')
cs = conn.cursor()

sql_query =   """
        select *
        from MERGE_DATA
        """
rs = cs.execute(sql_query)

# sql to pandas df
df_sql = pd.read_sql(sql_query, con=conn)
df_sql['CHANGE'] = df_sql['CHANGE'].str.replace('%', '')
df_sql['CHANGE'] = pd.to_numeric(df_sql['CHANGE'])
print(df_sql['CHANGE'])


print(df_sql['VOLUME'])
for index,data in enumerate(df_sql['VOLUME']):
    if data != None:
        if data[-1] == 'K':
            data = data.replace('K','')
            data = round(float(data)*1000)
            df_sql['VOLUME'][index] = data
        elif data[-1] == 'M':
            data = data.replace('M','')
            data = round(float(data) * 1000000)
            df_sql['VOLUME'][index] = data
    else:
        df_sql['VOLUME'][index] = 0
df_sql['VOLUME'] = df_sql['VOLUME'].astype(int)

print(df_sql)
print(df_sql.info())
print(df_sql.describe())

print(df_sql[['CLOSE','OPEN']].corr())

print(df_sql[['CLOSE','VOLUME']].corr())

print(df_sql.index)
# df_two = df.iloc[[]]

date=df_sql['DATES']
close=df_sql['CLOSE']
x=list(date)
y=list(close)
plt.plot(x, y, color = 'g', linestyle = 'solid', label = "Close Price")
plt.xlabel('Date')
plt.xticks(rotation = 25)
plt.ylabel('CLose Price')
plt.title('Dates')
plt.legend()
plt.show()


