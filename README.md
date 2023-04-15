# Startel Client Report Viewer

This is a simple [Django application](https://www.djangoproject.com/) that
allows you to view the Startel HTML Clients Report by client.

# Setup

⚠️ The commands in this readme assume you are either using bash or PowerShell.

## Install Python
If on Windows, [download and install Python 3.11](https://www.python.org/downloads/).

If on Linux, install Python 3.11 either by compiling from source or using the
appropriate repositories in your package management system. The minimum version
required is 3.8.5.

## Download release or clone
Download the [release
archive](https://github.com/voughtdq/startel-clients-html-viewer/tags) or clone
this repository. If you want to clone it, make sure to [install
git](https://git-scm.com/download) then run

`git clone https://github.com/voughtdq/startel-clients-html-viewer`

## Set up virtual environment
In the same folder that the files were extracted to, create a virtual environment:

`python -m venv env`

This will create the virtual environment in a folder called `env`. 

To activate the virtual environment run

`env\Scripts\activate` on Windows or
`env/bin/activate` on Linux

## Install dependencies
Run

`pip install -r requirements.txt`

If on Windows, you may need to run

`python -m pip install -r requirements.txt`

## Create settings file
Copy `clients/settings.example.py` into a new file called `clients/settings.py`
or follow the instructions in the last section to use a custom settings file.

We need to copy the secret key into the settings file.

On Windows, run

`python -c 'from django.core.management.utils import get_random_secret_key; print(f""SECRET_KEY = ''{get_random_secret_key()}''"")'`

On Linux run

`python -c 'from django.core.management.utils import get_random_secret_key; print(f"SECRET_KEY = \'{get_random_secret_key()}\'")'`

Then paste the output into `settings.py`.

If you intend on listening from a host other than `localhost` you can either add
it to `ALLOWED_HOSTS` in `settings.py` or replace `localhost` with the address
you are using. Please note that you will need to properly configure your reverse
proxy to direct requests to the host you've chosen to this application.

## Run initial database migrations
This application uses sqlite by default. No database connection is necessary.

Run
`python manage.py migrate`

## Run the server
Start the server:

`python manage.py runserver`

The server will begin listening on port 8000. You can navigate to http://localhost:8000/ to see the application

To view a client, type in the ID and submit the query. See the next part for how to import client information.

If you need to change the settings file, use the `DJANGO_SETTINGS_MODULE` environment variable:

`$env:DJANGO_SETTINGS_MODULE="clients.other_settings"`
`python manage.py runserver` on Windows or
`DJANGO_SETTINGS_MODULE=clients.other_settings python manage.py runserver` on Linux

## Import Startel HTML Clients Report
Navigate to SAC > Reports > System Reports > Clients

⚠️ For the import to run correctly, "1-line Headers" must be checked and "Add
Page Break Between Clients" must be checked.

To begin the import, run

`python startel_clients_html_importer.py path/to/your/report.htm`

The script will tell you which client IDs are imported. The script can be run on
the same or successive reports. It will simply overwrite data of existing
clients or import a new client as needed. The script does not yet remove
inactive clients.

The class that runs the import can also be imported if you want to use it in
another Python script.