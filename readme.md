# What is this
It's a personal learning thing, you probably don't want 
anything to do w/this code `:o`

# DB Info
## Tables
users = ROWID, name (text, uniq)

categories = ROWID, category (text, uniq), description (txt)

events = ROWID, user (int), ts (int, PK), category (int)

Map the integers representing user & category in the events table 
to corresponding ROWID for user in users table, and similar for 
categories.

# Reminders
sqlite includes a ROWID column when creating tables, unless prevented 
from doing so. Using that for PK in most (all?) instances.  Mention 
ROWID in table descriptions above - they are not part of the table 
creation process.

The time associated with events is a unix timestamp - without seconds 
e.g. no fractional part.

# Project Structure
* App is in tos/
* lib/ holds the functions that do the work, e.g. adding users, or 
* events, etc.
* data/ holds data files, including the sqlite db
* scripts/ holds utility scripts - not part of the app
* the `experiment.py` module is the place to try out code that "does 
stuff"; add your code then run that module
* If there's no requirements.txt file it's b/c the project is not yet 
using 3rd party packages.

# Todo
* Add more "api" functions - see docs on use cases
* Add tests - SOON before it gets out of hand
* Build the web app bits - pending framework selection