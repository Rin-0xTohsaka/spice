import os

# Define the name of the directory to be created
dirs = [
    'spice',
    'spice/spice',
    'spice/spice/api',
    'spice/spice/static',
    'spice/spice/static/css',
    'spice/spice/static/js',
    'spice/spice/static/lib',
    'spice/spice/templates'
]

for dir_name in dirs:
    try:
        # Create directories
        os.makedirs(dir_name)
        print("Directory ", dir_name, " Created ")
    except FileExistsError:
        print("Directory ", dir_name, " already exists")

# Create files
files = [
    'spice/.env',
    'spice/.gitignore',
    'spice/config.py',
    'spice/README.md',
    'spice/requirements.txt',
    'spice/wsgi.py',
    'spice/spice/__init__.py',
    'spice/spice/app.py',
    'spice/spice/api/__init__.py',
    'spice/spice/api/brc20_api.py',
    'spice/spice/api/data.py',
    'spice/spice/api/transaction_history.py',
    'spice/spice/api/token_holdings.py',
    'spice/spice/api/env.py',
    'spice/spice/static/css/main.css',
    'spice/spice/static/js/main.js',
    'spice/spice/static/lib/chart.min.js',
    'spice/spice/templates/index.html',
    'spice/spice/templates/transaction_history.html',
    'spice/spice/templates/token_holdings.html'
]

for file_name in files:
    with open(file_name, 'a') as f:
        pass
    print("File ", file_name, " Created ")
