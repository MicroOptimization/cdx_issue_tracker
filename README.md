# Not Jira
We're gonna make a jira-like web app that helps teams manage tickets.

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

## Technologies
I'm thinking of doing this with flask, html, css (might try bootstrap, but 
I think it's nice to learn some more css). I haven't decided what database to
use yet, but probably not sqlite again. Maybe Postgres or Mongo. I'm also
trying to decide whether or not I should host this on my personal domain (jackiezhen.com)
or to buy a more generic domain for it (codiacstech.com)

After this, I think I'll learn Node and React lol.

## Resume Value:
### Familiarity
- Pretty much everyone uses some ticketing system like jira
  - People looking to hire can recognize instantly what I made
    - Could be a downside in terms of standout value (got the idea from yt)

### Complexity
- There are quite a few moving parts
  - Proving that I can organize these moving parts will be a boon 

### Practicality
- My Last project was a weather dashboard, which isn't exactly the most useful
  - Tricky to differentiate as a real product (type temp in google lol)
  - This atleast could be something I actually use.
  
### Executability
- This isn't exactly something I haven't done, it's more like an amalgamation of things I've done, but on a bigger scale.
  - So essentially this project is doable, but has some more meat on its bones than what I've done in the past
