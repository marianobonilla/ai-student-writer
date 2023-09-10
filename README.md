# ai-student-writer

# local set up
brew install postgresql
brew services start postgresql
createdb pdf_chat_db
to stop local db: brew services stop postgresql

Flask Configuration
cd ai-student-writer
optional: consider using venv for virtual environments. create a virtual env in the root of the project 
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
For local development:
export FLASK_ENV=dev
After setting up the db and config, run the migrations to create the necessary table in your local db
flask db init (only one time needed when first setting up db config)
flash db upgrade

Development Workflow

Database Migrations
Use Flask-Migrate to handle database migrations. Always test migrations against the local database before applying them to the production AWS RDS.

Generate Migrations:
After defining or updating your models, generate a migration script:
flask db migrate -m "Description of changes"
Apply Migrations:
flask db upgrade