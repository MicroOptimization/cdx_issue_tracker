from sqlalchemy import create_engine, URL, text, insert, Table, MetaData, Column, Integer, String, select
import os
import bcrypt

class Db_helper:
    user_account = None
    engine = None

    def __init__(self):
        url_object = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password=os.environ["pg_pw"],  # DO NOT ESCAPE THIS PASSWORD 
            host="localhost",
            database="not_jira",
        )

        self.engine = create_engine(url_object)
        
        metadata_obj = MetaData()
        self.user_account = Table(
            "user_account",
            metadata_obj,
            Column("user_id", Integer),
            Column("username", String(30)),
            Column("pword", String),
            Column("email", String),
        )

        self.project = Table(
            "project",
            metadata_obj,
            Column("project_id", Integer),
            Column("title", String),
            Column("description", String),
            Column("key_id", String),
        )

        self.projects_users = Table(
            "projects_users",
            metadata_obj,
            Column("project_id", Integer),
            Column("user_id", Integer),
        )

    def create_user(self, username_input, password_input, email_input):
        with self.engine.connect() as conn:
            stmt = select(self.user_account).where((self.user_account.c.username == username_input) or (self.user_account.c.email == email_input))
            #problem statement^ Maybe we can just make two statements
            #we're trying to prevent accounts being made that have existing usernames and emails in our database

            result = conn.execute(stmt)
            rd = result.mappings().all()
            print(rd)
            if len(rd) >= 1:
                return False
            else:
                passwd = password_input #password input for when you're making your password for the first time

                #Do both of these for when you make a pw for the first time or reset your pw
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(passwd.encode('utf8'), salt)
                #put hashed into your database under password
                password_hash = hashed.decode('utf8') # decode the hash to prevent is encoded twice

                stmt = insert(self.user_account).values(username=username_input, pword=password_hash, email=email_input)

                result = conn.execute(stmt)
                conn.commit()
                conn.close()
                return True
        
    def login(self, username_input, password_input):
        with self.engine.connect() as conn:
            stmt = select(self.user_account).where(self.user_account.c.username == username_input)
            
            
            result = conn.execute(stmt)
            conn.close()

            rd = result.mappings().all()
            if len(rd) == 0:
                #no username in db
                print("here")
                return (False, None)
            else:
                correct_password = rd[0]["pword"]
                if bcrypt.checkpw(password_input.encode('utf8'), correct_password.encode('utf8')):
                    return (True, rd[0])
                else:
                    return (False, None)
        return (False, None)
    
    def create_project(self, project_details, uid):
        with self.engine.connect() as conn:
            stmt = insert(self.project).values(title=project_details[0], key_id=project_details[1], description=project_details[2]).returning(self.project.c.project_id)
            res = conn.execute(stmt) #returns a sqlalchemy.engine.cursor.CursorResult object

            


            #<sqlalchemy.engine.cursor.CursorResult object at 0x000001FE8F83E4C0>
            temp = res.mappings().all()[0]
            #res.mappings().all() returns a list
            #res.mappings() returns a sqlalchemy.engine.result.MappingResult
            #res.mappings().all()[0] returns a sqlalchemy.engine.row.RowMapping

            pid = temp["project_id"]

            stmt = insert(self.projects_users).values(project_id=pid, user_id=uid)
            conn.execute(stmt)
            conn.commit()
            conn.close()
            return True
        return False


#dbh = Db_helper()
#dbh.create_project(("many_many_test", "mmt", "we're gonna test our many to many relationships and connect this to spaghetti's account"), uid="24")


#dbh.create_user("1", "2", "1@gmail.com")

#print(dbh.login("1", "4"))

#dbh.create_user("bearsley", "grizz", "bzl@gmail.com")