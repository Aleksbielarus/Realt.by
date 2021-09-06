import Connection

# postgresql connection check
dbname = 'postgres'
if __name__ == "__main__":
    db = Connection.connect(dbname)
    cursor = db.cursor()
    cursor.execute("select * from data_source.main_page_results limit 10")
    records = cursor.fetchall()
    for i in records:
        print(i)
    db.close()