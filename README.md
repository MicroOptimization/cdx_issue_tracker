# We're gonna make a jira-like web app that helps teams manage tickets

## Essential Features: 
- Users (Login, password (hashed), email, projects that they're associated with)
  - Login
  - Create User
  - Password Reset
    - Activated via email
  - User Type (Site Admin, Project Manager, Developer)
- Projects (Issues[states])
  - Users associated with the project
  - Issues per project
    - States: (To Do / In Progress / Done)
    - Comments from the team
    - priority (low, medium, high, none)
    - ticket search
    - File uploader (attach images and documents to tickets)
    - system to assign tickets to people
- Notification System
  - Notifies users when a new ticket appears for a project they're a part of
- User Management System
  - For Project Managers (and site admins)

##Technologies
I'm thinking of doing this with flask, html, css (might try bootstrap, but 
I think it's nice to learn some more css). I haven't decided what database to
use yet, but probably not sqlite again. Maybe Postgres or Mongo. I'm also
trying to decide whether or not I should host this on my personal domain (jackiezhen.com)
or to buy a more generic domain for it (codiacstech.com)
