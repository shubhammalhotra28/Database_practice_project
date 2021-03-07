import unittest
from src.rideshare import *
from src.rideshare import connect

class TestChat(unittest.TestCase):

    def test_build_tables(self):
        """Build the tables"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        cur.execute('SELECT * FROM rider_table')
        cur.execute('SELECT * FROM driver_table')
        self.assertEqual([], cur.fetchall(), "no rows in example_table")
        conn.close()

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuildTables()
        rebuildTables()
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM driver_table')
        self.assertEqual([], cur.fetchall(), "no rows in example_table")
        cur.execute('SELECT * FROM rider_table')
        self.assertEqual([], cur.fetchall(), "no rows in example_table")
        conn.close()

    def test_drivers_table_1(self):
        """
        test drivers_table
        :return:
        """

        seedAllData()

        con = connect()
        cur = con.cursor()
        # 1st case
        cur.execute('Select driver_id from driver_bridge_table where driver_id = 1')
        # query = cur.fetchall()
        # print(query)
        self.assertEqual(2,len(cur.fetchall()),"Passed 1st case")

        con.close()

    def test_rider_table(self):
        """
        test rider_table
        :return:
        """
        seedAllData()

        con = connect()
        cur = con.cursor()

        # 2nd case
        cur.execute('Select count(*) from driver_bridge_table where rider_id = 2')
        driver_ids_set = set()
        driver_ids_set.add(0)
        driver_ids_set.add(1)


        self.assertEqual([(1,)],cur.fetchall(),"Passed 2nd test case")

        con.close()



    def test_driver_table_2(self):
        """
        test bridge table
        :return:
        """
        seedAllData()

        con = connect()
        cur = con.cursor()

        # 3rd case
        cur.execute('Select driver_id from driver_bridge_table where driver_id = 3')
        ####
        self.assertEqual(0,len(cur.fetchall()),"Passed 3rd case")
        con.close()
    
    def test_driver_rating(self):
        """
        method to check the rating from driver_table
        :return:
        """

        seedAllData()

        con = connect()
        cur = con.cursor()

        # 4th case
        cur.execute('Select avg_rating from driver_table where id = 1')
        ####
        self.assertEqual([(3.2,)],cur.fetchall(),"Passed 3rd Case")

        con.close()


    def testcreation(self):

        """
        method  to test rider_trip_review, driver_trip_review, trip_details,rider_table : update and insertion
        :return:
        """
        seedAllData()

        con = connect()
        cur = con.cursor()

        # rider_review check
        cur.execute('Select count(*) from rider_trip_review')
        self.assertEqual(4,cur.fetchall()[0][0],"Passed")

        # driver_Review_check

        cur.execute('Select count(*) from driver_trip_review')
        self.assertEqual(2,cur.fetchall()[0][0],"Passed")


        cur.execute('Select count(*) from trip_details')
        self.assertEqual(9,cur.fetchall()[0][0],"Passed")

        cur.execute("select is_available from rider_table where name = '{}'".format("Ms. Daisy"))
        self.assertEqual(False,cur.fetchall()[0][0],"Passed")

        con.close()


    def test_checkUpdate(self):
        """
        Method responsible to check if the update is working perfectly within driver_table
        :return:
        """
        seedAllData()
        con = connect()
        cur = con.cursor()

        cur.execute("Update driver_table Set car_make = '{0}' where name = '{1}'".format('Toyota',"Tom Magliozzi"))
        cur.execute("Select car_make from driver_table where name = '{0}'".format("Tom Magliozzi"))
        self.assertEqual("Toyota", cur.fetchall()[0][0], "Passed")

        cur.execute("Update driver_table Set car_make = '{0}' where name = '{1}'".format('Dodge',"Ray Magliozzi"))
        cur.execute("Select car_make from driver_table where name = '{0}'".format("Ray Magliozzi"))

        self.assertEqual("Dodge", cur.fetchall()[0][0], "Passed")

        con.close()


    def test_no_reciepts(self):
        """
        test to check the reciepts generated if no ride is taken
        :return:
        """
        seedAllData()
        con = connect()
        cur = con.cursor()

        cur.execute("Select count(*) from rider_trip_review where is_completed = {}".format(True))
        self.assertEqual([(1,)],cur.fetchall())

        cur.execute("Select count(*) from driver_trip_review where is_completed = {}".format(True))
        # cur.execute('Select * from driver_trip_review')
        # print(cur.fetchall())
        self.assertEqual([(1,)], cur.fetchall())

        con.close()


    def test_amount_split(self):
        """
        test to check amount split

        :return:
        """
        seedAllData()
        con = connect()
        cur = con.cursor()

        cur.execute("Select id from driver_table where name = '{}'".format("Alex"))
        alex_driver_id = cur.fetchall()[0][0]

        cur.execute("select sum(amount) from trip_details where driver_id = {}".format(alex_driver_id))
        self.assertEqual(12, cur.fetchall()[0][0])

        con.close()



    def test_feedback(self):
        """
        test to check comment feature to riders_reviews
        :return:
        """

        seedAllData()
        con = connect()
        cur = con.cursor()

        cur.execute('Select comment from comment_rider_review')
        self.assertEqual([('Thanks for the feedback',)],cur.fetchall())

        con.close()

    def test_unavailable_driver(self):
        """
        test to check is_active field for driver
        :return:
        """

        seedAllData()
        con = connect()
        cur = con.cursor()
        # cur.execute("select sum(amount) from trip_details where driver_id = {}".format(alex_driver_id))

        cur.execute("Select count(id) from driver_table where is_active = '{}'".format(False))
        self.assertEqual([(1,)],cur.fetchall())

        con.close()


    def test_all_data(self):
        """
        test to check all the seeded data

        :return:
        """

        seedAllData()
        con = connect()
        cur = con.cursor()

        result = db04Functionalities()
        self.assertEqual(result,[(1, 'Tom Magliozzi', 'Dont drive like my brother', 3.2, None, None, None, None, True, 1, 'Mike Easter', None, 4.3, None, None, True, 1, 1, 1), (2, 'Ray Magliozzi', 'Dont drive like my brother', 3.4, None, None, None, None, True, 1, 'Mike Easter', None, 4.3, None, None, True, 2, 2, 1), (1, 'Tom Magliozzi', 'Dont drive like my brother', 3.2, None, None, None, None, True, 2, 'Ray Magliozzi', None, None, None, None, True, 3, 1, 2)]
)
        con.close()


    def test_billing_info(self):
        """
        test to check the billing info
        :return:
        """


        seedAllData()
        con = connect()
        cur = con.cursor()
        cur.execute('Select driver_id from driver_bridge_table where driver_id = 3')

        cur.execute("Select bill,hour from billing_details where hour between '3' and '4'")
        result = cur.fetchall()
        self.assertEqual(result,[(5.0, '3:30')])
        cur.execute("Select avg(bill) from billing_details where hour between '4' and '5'")
        res = cur.fetchall()
        self.assertEqual(res,[(15.0,)])

        con.close()
