from sqlalchemy import create_engine, URL, text, Table, MetaData, Column, Integer, String, select, delete, update, insert
import os
import bcrypt
from datetime import datetime, timedelta
import secrets

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
        self.engine = create_engine(url_object) #engines are a connection factory essentially, and we use connections to have our orm generate
        #sql queries and use them on our sql database.
        
        metadata_obj = MetaData()
        
        #these are representations of our tables, that we'll use to reference later when we're making queries.
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

        self.ticket = Table(
            "ticket",
            metadata_obj,
            Column("ticket_id", Integer),
            Column("title", String),
            Column("description", String),
            Column("date_created", String),
            Column("date_completed", String),
            Column("project_id", Integer),
            Column("project_title", String),
            Column("col_id", Integer),
        )

        self.tickets_users = Table(
            "tickets_users",
            metadata_obj,
            Column("user_id", Integer),
            Column("ticket_id", Integer),   
        )

        self.col = Table(
            "col",
            metadata_obj,
            Column("col_id", Integer),
            Column("col_title", String),
            Column("project_id", Integer),    
        )

        self.password_token = Table(
            "password_token",
            metadata_obj,
            Column("token_id", Integer),
            Column("chars", String),
            Column("date_created", String),
            Column("user_id", Integer),
        )

    def create_user(self, username_input, password_input, email_input):
        with self.engine.connect() as conn:
            stmt = select(self.user_account).where((self.user_account.c.username == username_input) or (self.user_account.c.email == email_input))
            #problem statement^ Maybe we can just make two statements
            #we're trying to prevent accounts being made that have existing usernames and emails in our database

            result = conn.execute(stmt)
            rd = result.mappings().all()
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

            temp = res.mappings().all()[0]
            #res.mappings().all() returns a list
            #res.mappings() returns a sqlalchemy.engine.result.MappingResult
            #res.mappings().all()[0] returns a sqlalchemy.engine.row.RowMapping
            
            conn.commit()#this is important because next we add our user to our project, and this commit makes it so our project exists in 
            #our postgres db, and things will explode if we try to add our user to a project that doesn't exist yet.

            pid = temp["project_id"] #we need this to add an entry to our many to many table for users and projects
            self.add_user_to_project(uid, pid) #adds the person who made the project to the project

            conn.commit()
            conn.close()
            return True
        return False
    
    def get_uid_by_email(self, email):
        with self.engine.connect() as conn:
            stmt = select(self.user_account).where(self.user_account.c.email == email)
            res = conn.execute(stmt)
            rows = res.mappings().all()
            uid = rows[0]["user_id"]
            conn.close()
            return uid
        
    def add_user_to_project(self, uid, pid):
        with self.engine.connect() as conn:
            stmt = insert(self.projects_users).values(project_id=pid, user_id=uid)
            conn.execute(stmt)

            conn.commit()
            conn.close()
            return True
        return False



    def get_pids(self, uid):
        with self.engine.connect() as conn:
            stmt = select(self.projects_users).where(self.projects_users.c.user_id == uid)
            res = conn.execute(stmt)
            projects = res.mappings().all()

            pids = []
            for relationship in projects:
                pids.append(relationship["project_id"])
            conn.close()
            return pids #returning a list of all the project IDs
        return None

    def get_project_info(self, pids):
        #pids is a list of project IDs
        info = []
        with self.engine.connect() as conn:
            for c_pid in pids:
                #c_pid = current project id
                stmt = select(self.project).where(self.project.c.project_id == c_pid) #getting the 
                res = conn.execute(stmt)
                row = res.mappings().all() #(this is a list of all rows that match our select project id)
                info.append(row[0])
            conn.close()
            return info #this is a list of dictionaries, each dictionary represents a project row, where the keys are columns 
        return None
    


    def create_ticket(self, pid, ticket_details):
        with self.engine.connect() as conn:
            stmt = insert(self.ticket).values(
                title=ticket_details["title"],
                description=ticket_details["description"], 
                project_id=pid, 
                project_title=ticket_details["project_title"],
                col_id=ticket_details["col_id"]
            ).returning(self.ticket.c.ticket_id)

            res = conn.execute(stmt)
            tid = res.mappings().all()[0]["ticket_id"] #useful once we decide 

            conn.commit()
            conn.close()
            return True
        return False
    
    def get_user_tickets(self, uid):
        
        with self.engine.connect() as conn:
            stmt = select(self.tickets_users).where(self.tickets_users.c.user_id == uid) #gets user_ticket pairs
            res = conn.execute(stmt)
            rows = res.mappings().all() #user-ticket pairs

            tickets = []
            for row in rows: #populates list tickets by going through each u/t pair and getting the corresponding ticket 
                tid = row["ticket_id"] 
                stmt = select(self.ticket).where(self.ticket.c.ticket_id == tid)
                res2 = conn.execute(stmt)
                rows2 = res2.mappings().all() #dict of the current row of tid 
                tickets.append(rows2)

            conn.close()

            return tickets #list of ticket data rows (each row is a dict with columns as keys)
        return None

    def assign_ticket_to_user(self, uid, tid):
        with self.engine.connect() as conn:
            stmt = insert(self.tickets_users).values(user_id=uid, ticket_id=tid)
            conn.execute(stmt)
            conn.commit()
            conn.close()

        return False    



    def get_project_title_from_id(self, pid):
        with self.engine.connect() as conn:
            stmt = select(self.project).where(self.project.c.project_id == pid)
            res = conn.execute(stmt)
            project_name = res.mappings().all()[0] #every row that satisfies our query
            conn.close()
            return project_name["title"]
        return None

    def get_cols(self, pid):
        with self.engine.connect() as conn:
            stmt = select(self.col).where(self.col.c.project_id == pid)
            res = conn.execute(stmt)
            rows = res.mappings().all()
            conn.close()
            return rows #list of every column row in our project
        
    def get_tickets_from_col(self, cid):
        with self.engine.connect() as conn:
            stmt = select(self.ticket).where(self.ticket.c.col_id == cid)
            res = conn.execute(stmt)
            rows = res.mappings().all()
            conn.close()
            return rows    

    def get_ticket_info_by_id(self, tid):
        with self.engine.connect() as conn:
            stmt = select(self.ticket).where(self.ticket.c.ticket_id == tid)
            res = conn.execute(stmt)
            conn.close()
            return res.mappings().all()[0]
        
    def remove_ticket(self, tid):
        #so basically if you want to remove a row that is a part of a many-many relationship, delete the rows of many-many relationship first
        #I believe that that's because the many-many relationship references a row, and that probably causes something like a 
        #null pointer. don't forget to commit.
        with self.engine.connect() as conn:
            self.remove_ticket_relationships(tid) 
            stmt = delete(self.ticket).where(self.ticket.c.ticket_id == tid)
            res = conn.execute(stmt)
            conn.commit()
            conn.close()
    
    def remove_ticket_relationships(self, tid): ######### will be useful later
        with self.engine.connect() as conn:
            stmt = delete(self.tickets_users).where(self.tickets_users.c.ticket_id == tid)
            res = conn.execute(stmt)
            conn.commit()
            conn.close()

    def remove_project(self, pid):
        with self.engine.connect() as conn:
            self.remove_project_relationships(pid)
            stmt = delete(self.project).where(self.project.c.project_id == pid)
            conn.execute(stmt)
            
            conn.commit()
            conn.close()

    def remove_project_relationships(self, pid):
        with self.engine.connect() as conn:
            stmt = delete(self.projects_users).where(self.projects_users.c.project_id == pid)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def add_col(self, pid, name):
        with self.engine.connect() as conn:
            stmt = insert(self.col).values(
                col_title = name,
                project_id = pid 
            )
            conn.execute(stmt) #col id here if you need it later
            conn.commit()
            conn.close()
    
    def delete_col(self, cid):
        with self.engine.connect() as conn:
            tickets = self.get_tickets_from_col(cid)
            if len(tickets) > 0: #there are associated tickets
                #delete all associated tickets first if cols have tickets.
                for ticket in tickets:
                    self.remove_ticket(ticket['ticket_id'])
            #and now we delete the column
            stmt = delete(self.col).where(self.col.c.col_id == cid)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def get_project_tickets(self, pid):
        with self.engine.connect() as conn:
            stmt = select(self.ticket).where(self.ticket.c.project_id == pid)
            res = conn.execute(stmt)
            tickets = res.mappings().all()
            conn.close()
            return tickets #list of row dicts
        
    def get_project_users(self, pid):
        with self.engine.connect() as conn:
            stmt = select(self.projects_users).where(self.projects_users.c.project_id == pid)
            res = conn.execute(stmt)
            conn.close()
            rows = res.mappings().all()
            uids = []
            for relationship in rows:
                uids.append(relationship["user_id"])
            users = self.get_users_from_uids(uids)

            return users
        
    def get_users_from_uids(self, uids):
        rows = []
        with self.engine.connect() as conn:
            for uid in uids:
                stmt = select(self.user_account).where(self.user_account.c.user_id == uid)
                res = conn.execute(stmt)
                row = res.mappings().all()[0]
                rows.append(row)
            conn.close()
            return rows #returns a list of user row dicts

    def remove_user_from_project(self, uid, pid):
        with self.engine.connect() as conn:
            stmt = delete(self.projects_users).where((self.projects_users.c.project_id == pid) & (self.projects_users.c.user_id == uid))
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def edit_project_desc(self, pid, new_text):
        with self.engine.connect() as conn:
            stmt = update(self.project).where(self.project.c.project_id == pid).values(description=new_text)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def edit_project_title(self, pid, new_title):
        with self.engine.connect() as conn:
            stmt = update(self.project).where(self.project.c.project_id == pid).values(title=new_title)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def edit_ticket_desc(self, tid, new_text):
        with self.engine.connect() as conn:
            stmt = update(self.ticket).where(self.ticket.c.ticket_id == tid).values(description=new_text)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def edit_ticket_title(self, tid, new_title):
        with self.engine.connect() as conn:
            stmt = update(self.ticket).where(self.ticket.c.ticket_id == tid).values(title=new_title)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def edit_col(self, cid, new_title):
        with self.engine.connect() as conn:
            stmt = update(self.col).where(self.col.c.col_id == cid).values(col_title=new_title)
            conn.execute(stmt)
            conn.commit()
            conn.close()

    def check_email(self, email): #checks if a email is being used by a current account
        with self.engine.connect() as conn:
            stmt = select(self.user_account).where(self.user_account.c.email == email)
            res = conn.execute(stmt)
            rows = res.mappings().all()
            conn.close()
            return len(rows) != 0 

    def create_token(self, uid):
        token = secrets.token_hex(3)
        with self.engine.connect() as conn:  
            stmt = select(self.password_token).where(self.password_token.c.user_id == uid) #check if old token exists
            res = conn.execute(stmt)
            rows = res.mappings().all()
            if len(rows) != 0: #previous token exists   
                stmt = delete(self.password_token).where(self.password_token.c.user_id == uid) #remove previous token
                conn.execute(stmt)
            stmt = insert(self.password_token).values(chars=token,user_id=uid) #add new token
            conn.execute(stmt)
            conn.commit()
            conn.close()

            return token
    
    def verify_token(self, token):
        with self.engine.connect() as conn:  
            stmt = select(self.password_token).where(self.password_token.c.chars == token) #check if token exists
            res = conn.execute(stmt)
            rows = res.mappings().all()

            if len(rows) != 0: #token exists
                date_created = rows[0]["date_created"]
                current_time = datetime.now()
                td = current_time - date_created #td = time delta which is what you get from doing math with datetime objects
                minutes_since_creation = td.seconds // 60 % 60 #for some reason they have seconds and days but not minutes lol idk
                time_limit = 15 #in minutes, the time after the token is generated in which the user is allowed to submit the token for reset
                
                stmt = delete(self.password_token).where(self.password_token.c.chars == token) #delete our old expired token or old but valid token
                conn.execute(stmt)
                conn.commit()
                conn.close()

                return minutes_since_creation < time_limit #token valid if you entered it in time (15 min)
            else:
                conn.close()
                return False #len of rows is 0, so token DNE in our DB
dbh = Db_helper()
pid = 3
uid = 6

#dbh.create_token(6)
#536d5f
#2b8b7c
#print(dbh.verify_token("536d5g"))

#print(dbh.check_email("parma@gmail.com"))


