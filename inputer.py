import sys
file1 = open('datainput.in', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character


import psycopg2

try:
    connection = psycopg2.connect(host=sys.argv[1],
                                         database='app',
                                         user='postgres',
                                         password='supersecretpassword',
                                         port=5432)
    connection.autocommit = True
    for line in Lines:
        count += 1
        cursor = connection.cursor()
        print(line.strip())
        cursor.execute(line.strip())
        print("DONE")

    # connection.commit()    

except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

