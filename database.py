import sqlite3 as lite
import sys
import pandas as pd
from helper import Helper
from config import Hyper

class Data:
    sql_get_tweet_user_locations = "SELECT tweet_id, user_location FROM tweets WHERE country_code = '';"
    sql_get_user_location_table = "SELECT user_location, code FROM user_locations"
       
    def __init__(self) -> None:
        self.db = Hyper.db
        self.create_connection()

        Helper.printline("Database opened successfully") 
    
    def create_connection(self):
        """ create a database connection to the SQLite database
            :param:
            :return:
        """
        self.con = None
        try:
            self.con = lite.connect(self.db, 
                            detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)
        except Exception as e:
            sys.exit(f"Error with database connection: {e}")

    def get_user_location_dictionary(self):
        #self.con.row_factory = self.dict_factory
        c = self.con.cursor()
        c.execute(self.sql_get_user_location_table)
        list = c.fetchall() 
        self.user_locations = dict(list)
 
    def dict_factory(self, cursor, row):
        d = {}
        d[row[1]] = row[0]
        return d
            
    def save_user_location(self, user_location, code):
        table_name = "user_locations"        
        #row = {user_location : code}
        #user_location_x = f"'{user_location}'"
        row = {"user_location": user_location, "code": code}
        df_tweet = pd.DataFrame([row])
        try:
            df_tweet.to_sql(table_name, self.con, if_exists='append', index=False)
            self.con.commit()
        except Exception as e:
            sys.exit(f"Error inserting into user location the row - '{row}': {e}")
 
    def get_tweet_user_locations(self):
        c = self.con.cursor()
        c.execute(self.sql_get_tweet_user_locations)
        self.tweet_user_locations = c.fetchall() 
   
    def save_tweet_country_code(self, tweet_id, country_code):
        sql_script = f"UPDATE tweets SET country_code = '{country_code}' WHERE tweet_id == {tweet_id}"
        c = self.con.cursor()
        try:
            c.execute(sql_script)
            self.con.commit()
        except Exception as e:
            sys.exit(f"Error inserting country code {country_code} into tweet with tweet_id {tweet_id}: {e}")
       