from src.swen344_db_utils import connect
import csv
import os

def rebuildTables():
    """
    BuildTables : Function responsible to build tables
    :return:
    """

    conn = connect()
    cur = conn.cursor()

    drop_driver_sql = """
            DROP TABLE IF EXISTS driver_table
        """
    drop_rider_sql = """
            DROP TABLE IF EXISTS rider_table
        """
    drop_bridge_sql = """
                DROP TABLE IF EXISTS driver_bridge_table
            """

    drop_trip_details = """
                DROP TABLE IF EXISTS trip_details
            """

    drop_driver_trip_review = """
                DROP TABLE IF EXISTS driver_trip_review
            """

    drop_rider_trip_review = """
                DROP TABLE IF EXISTS rider_trip_review
            """

    drop_comment_rider = """
                DROP TABLE IF EXISTS comment_rider_review
    """

    drop_comment_driver = """
                DROP TABLE IF EXISTS comment_driver_review
    """

    drop_billing_sql = """
                DROP TABLE IF EXISTS billing_details
    """

    create_rider_sql = """
        CREATE TABLE rider_table(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            special_instructions VARCHAR(40),
            avg_rating FLOAT,
            is_created TEXT,
            zip_code INTEGER,
            is_available BOOLEAN DEFAULT TRUE
        )
    """

    create_driver_sql = """
        CREATE TABLE driver_table(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            special_instructions VARCHAR(40) DEFAULT NULL,
            avg_rating FLOAT,
            car_make VARCHAR(20),
            car_model VARCHAR(20),
            zip_code INTEGER,
            is_created TEXT,
            is_active BOOLEAN DEFAULT TRUE
        )
    """

    driver_bridge_sql = """
        
        CREATE TABLE driver_bridge_table(
            id SERIAL PRIMARY KEY,
            driver_id INTEGER,
            rider_id INTEGER,
            FOREIGN KEY (driver_id) REFERENCES driver_table(id),
            FOREIGN KEY (rider_id) REFERENCES rider_table(id)
        )
    
    """


    # zipcode : not sure, as lat and long will be getting the appropraite address
    # billing will be split with the update sql in trip_details

    trip_details_sql  = """
        
        CREATE TABLE trip_details(
            id SERIAL PRIMARY KEY,
            starting_point FLOAT,
            end_point FLOAT,
            zip_code INTEGER,
            ride_instructions TEXT,
            driver_id INTEGER,
            rider_id INTEGER,
            created_at TEXT,
            amount float,
            FOREIGN KEY (driver_id) REFERENCES driver_table(id),
            FOREIGN KEY (rider_id) REFERENCES rider_table(id)
        
        )
    
    """


    driver_trip_review_sql = """
        
        CREATE TABLE driver_trip_review(
            id SERIAL PRIMARY KEY,
            trip_id INTEGER,
            driver_id INTEGER,
            is_completed BOOLEAN,
            rate FLOAT,
            FOREIGN KEY (driver_id) REFERENCES driver_table(id),
            FOREIGN KEY (trip_id) REFERENCES rider_table(id)
        )
    """

    #is_completed : to see if the ride booked is comple6ted or not

    rider_trip_review_sql = """
        
        CREATE TABLE rider_trip_review(
            id SERIAL PRIMARY KEY,
            trip_id INTEGER,
            rider_id INTEGER,
            is_completed BOOLEAN,
            rate FLOAT,
            FOREIGN KEY (rider_id) REFERENCES rider_table(id),
            FOREIGN KEY (trip_id) REFERENCES driver_table(id)
        )
    """

    comment_driver_sql = """
        CREATE TABLE comment_rider_review(
            id SERIAL PRIMARY KEY,
            trip_id TEXT NOT NULL,
            rider_id INTEGER,
            driver_id INTEGER,
            comment TEXT,
            FOREIGN KEY (rider_id) REFERENCES rider_table(id),
            FOREIGN KEY (driver_id) REFERENCES driver_table(id)
        )
    """


    comment_rider_sql = """
        
        CREATE TABLE comment_driver_review(
            id SERIAL PRIMARY KEY,
            trip_id TEXT NOT NULL,
            rider_id INTEGER,
            driver_id INTEGER,
            comment TEXT,
            FOREIGN KEY (rider_id) REFERENCES rider_table(id),
            FOREIGN KEY (driver_id) REFERENCES driver_table(id)
        )
        
    """

    billing_split_sql = """
        CREATE TABLE billing_details(
            id SERIAL PRIMARY KEY,
            trip_id INTEGER,
            bill float,
            hour TEXT
        )
    
    """


    cur.execute(drop_bridge_sql)

    cur.execute(drop_comment_driver)
    cur.execute(drop_comment_rider)

    cur.execute(drop_billing_sql)
    cur.execute(drop_trip_details)
    cur.execute(drop_driver_trip_review)
    cur.execute(drop_rider_trip_review)
    cur.execute(drop_driver_sql)
    cur.execute(drop_rider_sql)


    cur.execute(create_rider_sql)
    cur.execute(create_driver_sql)
    cur.execute(driver_bridge_sql)

    cur.execute(trip_details_sql)
    cur.execute(driver_trip_review_sql)
    cur.execute(rider_trip_review_sql)
    cur.execute(comment_driver_sql)
    cur.execute(comment_rider_sql)
    cur.execute(billing_split_sql)

    conn.commit()
    conn.close()



def seedRiders():
    """
    Seed Riders Table
    :return:
    """
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO rider_table (name,avg_rating) VALUES ('Mike Easter',4.3)")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Ray Magliozzi')")

    cur.execute("INSERT INTO rider_table (name,zip_code) VALUES ('Hoke Colburn',30301)")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Ms. Daisy')")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Godot')")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Bobby')")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Louie')")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Elaine')")
    cur.execute("INSERT INTO rider_table (name) VALUES ('Tony')")

    cur.execute("INSERT INTO rider_table (name) VALUES ('Alex')")



    con.commit()
    con.close()


def seedDrivers():
    """
    Seed drivers table
    :return:
    """

    con = connect()
    cur = con.cursor()

    '''
    Drivers “Tom Magliozzi” and “Ray Magliozzi”. Their average ratings are 3.2 and 3.4 respectively. Both of their special instructions are “Don't drive like my brother.”
    '''
    cur.execute("INSERT INTO driver_table (name,special_instructions,avg_rating) VALUES ('Tom Magliozzi','Dont drive like my brother',3.2)")
    cur.execute("INSERT INTO driver_table (name,special_instructions,avg_rating) VALUES ('Ray Magliozzi','Dont drive like my brother',3.4)")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Mike Easter')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Hoke Colburn')")
    cur.execute("INSERT INTO driver_table (name,zip_code,is_created) VALUES ('Ms.Daisy',30301,'December 13,11:55')")

    cur.execute("INSERT INTO driver_table (name) VALUES ('Alex')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Bobby')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Louie')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Elaine')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Tony')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Vladimir')")
    cur.execute("INSERT INTO driver_table (name) VALUES ('Tony')")






    con.commit()
    con.close()

def seedDriverBridge():

    """
    Seed Drivers Bridge table (Driver -> Bridge -> Rider)
    :return:
    """
    con = connect()
    cur = con.cursor()

    cur.execute("Select id from driver_table where name = '{0}'".format("Tom Magliozzi"))
    driv_tom_id = (cur.fetchall())[0][0]

    cur.execute("Select id from driver_table where name = '{0}'".format("Ray Magliozzi"))
    driv_ray_id = (cur.fetchall())[0][0]

    cur.execute("Select id from rider_table where name = '{0}'".format("Mike Easter"))
    rider_mike_id = (cur.fetchall())[0][0]

    cur.execute("Select id from rider_table where name = '{0}'".format("Ray Magliozzi"))
    rider_ray_id = (cur.fetchall())[0][0]

    cur.execute("INSERT INTO driver_bridge_table(driver_id,rider_id) VALUES ({},{})".format(driv_tom_id,rider_mike_id))
    cur.execute("INSERT INTO driver_bridge_table(driver_id,rider_id) VALUES ({},{})".format(driv_ray_id,rider_mike_id))
    cur.execute("INSERT INTO driver_bridge_table(driver_id,rider_id) VALUES ({},{})".format(driv_tom_id,rider_ray_id))

    con.commit()
    cur.close()


def createDriverRider():
    """
    Parses csv file and seed the databases
    :return:
    """

    con = connect()
    cur = con.cursor()

    files = []

    import csv

    # print("current dir " , os.getcwd())

    with open('src/rideshare.csv', 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            files.append(row)
            # name,rider or driver, joining date
    files = files[1:]
    for i in range(len(files)):

        name = files[i][0]
        joining_date = files[i][2]
        driver = {'.driver':1,'driver':1,' driver':1}
        rider = {'rider':1}
        if files[i][1] in driver:
            cur.execute("INSERT INTO driver_table (name,is_created) VALUES (%s,%s)",(name,joining_date))
        elif files[i][1] in rider:
            cur.execute("INSERT INTO rider_table (name,is_created) VALUES (%s,%s)",(name,joining_date))

        else:
            print('exception')




    con.commit()
    con.close()

def newDB2TestCases():

    """
    Seed the databases with respect to use cases for db-2
    :return:
    """
    con = connect()
    cur = con.cursor()

    # Hoke Colburn drove Ms.Daisy to a location on December 13, 1989 at 12: 00pm. :::::::::
    cur.execute("Select id from driver_table where name = '{}'".format("Hoke Colburn"))
    hoke_id = cur.fetchall()[0][0]
    cur.execute("Select id from rider_table where name = '{}'".format("Ms. Daisy"))
    # print('che',cur.fetchall())
    daisy_id = cur.fetchall()[0][0]
    cur.execute('Insert into trip_details (created_at,driver_id,rider_id) VALUES (%s,%s,%s)',("December 13,1989 12: 00pm",hoke_id,daisy_id))


    # Both  Ms.Daisy and Hoke rated each other for the ride ::::::::
    cur.execute('Select id from trip_details')

    trip_id = cur.fetchall()[0][0]
    # cur.execute("INSERT INTO driver_bridge_table(driver_id,rider_id) VALUES ({},{})".format(driv_tom_id,rider_ray_id))

    cur.execute("Insert into driver_trip_review (trip_id,driver_id,is_completed,rate) VALUES ({},{},{},{})".format(trip_id,hoke_id,True,4.8))
    cur.execute("Insert into rider_trip_review (trip_id,rider_id,is_completed,rate) VALUES ({},{},{},{})".format(trip_id,daisy_id,True,4.8))


    # Tom Magliozzi drove Hoke Colburn to a location on December 14, 1989 at 4: 00 pm :::::

    cur.execute("Select id from driver_table where name = '{}'".format("Tom Magliozzi"))

    tom_id = cur.fetchall()[0][0]

    cur.execute("Select id from rider_table where name = '{}'".format("Hoke Colburn"))

    hoke_rider_id = cur.fetchall()[0][0]
    cur.execute('Insert into trip_details (created_at,driver_id,rider_id) VALUES (%s,%s,%s)',("December 13,1989 12: 00pm",tom_id,hoke_rider_id))
    # Ms.Daisy, after all of this, is able to remove her account. :::::

    cur.execute("Update rider_table Set is_available = '{0}' where id = '{1}'".format(False,daisy_id))




    con.commit()
    con.close()


def newDB03Data():
    """
    inserting db-3 data according to use cases
    :return:
    """


    con = connect()
    cur = con.cursor()

    cur.execute("Select id from driver_table where name = '{}'".format("Vladimir"))
    vladimir_driver_id = cur.fetchall()[0][0]
    cur.execute("Select id from rider_table where name = '{}'".format("Godot"))
    godot_rider_id = cur.fetchall()[0][0]

    cur.execute('INsert into trip_details (driver_id,rider_id) VALUES (%s,%s)',(vladimir_driver_id,godot_rider_id))

    cur.execute("Select id from trip_details where driver_id = '{}'".format(vladimir_driver_id))
    trip_id = cur.fetchall()[0][0]


    cur.execute('Insert into driver_trip_review (trip_id,driver_id,is_completed) VALUES (%s,%s,%s)',(trip_id,vladimir_driver_id,False))
    cur.execute('Insert into rider_trip_review (trip_id,rider_id,is_completed) VALUES (%s,%s,%s)',(trip_id, godot_rider_id, False))


    cur.execute("Select id from driver_table where name = '{}'".format("Alex"))
    alex_driver_id = cur.fetchall()[0][0]

    cur.execute("Select id from rider_table where name = '{}'".format("Bobby"))
    bobby_rider_id = cur.fetchall()[0][0]
    cur.execute("Select id from rider_table where name = '{}'".format("Louie"))
    louie_rider_id = cur.fetchall()[0][0]
    cur.execute("Select id from rider_table where name = '{}'".format("Elaine"))
    elaine_rider_id = cur.fetchall()[0][0]
    cur.execute("Select id from rider_table where name = '{}'".format("Tony"))
    tony_rider_id = cur.fetchall()[0][0]

    cur.execute('Insert into trip_details (driver_id,rider_id,amount) VALUES (%s,%s,%s)',(alex_driver_id,bobby_rider_id,3))

    cur.execute('Insert into trip_details (driver_id,rider_id,amount) VALUES (%s,%s,%s)',(alex_driver_id,louie_rider_id,3))

    cur.execute('Insert into trip_details (driver_id,rider_id,amount) VALUES (%s,%s,%s)',(alex_driver_id,elaine_rider_id,3))

    cur.execute('Insert into trip_details (driver_id,rider_id,amount) VALUES (%s,%s,%s)',(alex_driver_id,tony_rider_id,3))

    cur.execute("Select id from trip_details where driver_id = '{}'".format(alex_driver_id))
    alex_trip_ids = cur.fetchall()
    # print(alex_trip_ids)

    cur.execute('Insert into rider_trip_review (rider_id,trip_id,rate) VALUES (%s,%s,%s)',(alex_trip_ids[1][0],alex_driver_id,2))

    cur.execute('Insert into rider_trip_review (rider_id,trip_id,rate) VALUES (%s,%s,%s)',(alex_trip_ids[0][0],alex_driver_id,5))

    # 5 : louie  _ id _ trp

    cur.execute('Insert into comment_rider_review (trip_id,rider_id,driver_id,comment) VALUES (%s,%s,%s,%s)',(alex_trip_ids[1][0],louie_rider_id,alex_driver_id,"Thanks for the feedback"))

    cur.execute("Select id from driver_table where name = '{}'".format("Tony"))
    tony_driver_id = cur.fetchall()[0][0]
    cur.execute("Select id from rider_table where name = '{}'".format("Alex"))
    alex_rider_id = cur.fetchall()[0][0]

    cur.execute('Insert into trip_details (driver_id,rider_id) VALUES (%s,%s)',(tony_driver_id,elaine_rider_id))
    cur.execute('Insert into trip_details (driver_id,rider_id) VALUES (%s,%s)',(tony_driver_id,alex_rider_id))

    cur.execute("Update driver_table Set is_active = '{0}' where id = '{1}'".format(False,tony_driver_id))

    con.commit()
    con.close()


def db04Functionalities():
    """
    function getting all the required data from the tables
    :return:
    """

    con = connect()
    cur = con.cursor()
    cur.execute("Select id from driver_table where name = '{}'".format("Vladimir"))
    cur.execute('Select * from driver_table d INNER JOIN (Select * from rider_table r Inner Join driver_bridge_table b ON b.rider_id = r.id) as a on d.id = a.driver_id')
    result = cur.fetchall()

    con.commit()
    con.close()
    # print(result)
    return result



def seedBillingDetails():
    """
    seeding the billing data according to the test cases
    :return:
    """

    con = connect()
    cur = con.cursor()

    cur.execute("Insert into billing_details (bill,hour) VALUES (5,'3:30')")

    cur.execute("Insert into billing_details (bill,hour) VALUES (10,'4:55')")

    cur.execute("Insert into billing_details (bill,hour) VALUES (20,'4:59')")


    con.commit()
    con.close()




def seedAllData():
    """
    Seeding all the databases together
    :return:
    """

    rebuildTables()
    seedRiders()
    seedDrivers()
    createDriverRider()
    seedDriverBridge()
    newDB2TestCases()
    newDB03Data()
    db04Functionalities()
    seedBillingDetails()
