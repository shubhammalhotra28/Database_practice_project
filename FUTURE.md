#Surge Pricing

----------------
What tables need changing and/or adding?

For this, we can increase the prices, if there are more request for cabs, by adding another table which contains the entry if there are more than 5(max_limit) number of cabs from particular start point of the rider

------------------
What API methods would you provide?

We can hav ea get method which will check if the count of riders booking at particular start point is greater than 5 (max_limit), then add an entry to the newly created table, along with the start_point

-------------------

How might existing API methods change?

We, will be creating a new table which will be getting an entry (row), when the count at particular start_point of riders increase by 5 (max_limit)

-------------------

# Future Scheduling


What tables need changing and/or adding?

We will be adding a new column within the trip_details table, which will allow us to add the rides at later dates.

--------------------
What API methods would you provide?

There will be a method posting to the db table and creating a row (entry) within trip_details tabl.

---------------------
How might existing API methods change?

We just need to make sure that we are updating the new column values, if the ride is scheduled for later dates, otherwise we can pre initialise the entry within that colum with some default (None) value.

-----------------------




