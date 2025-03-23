# Contents

- [Contents](#contents)
- [Agdesk Farm Management](#agdesk-farm-management)
- [Platform Setup Instructions](#platform-setup-instructions)
  - [Install PostGIS Database](#install-postgis-database)
  - [pgAdmin4](#pgadmin4)
  - [SQL Shell](#sql-shell)
  - [VS CODE EXPLORER](#vs-code-explorer)
  - [Using Terminal](#using-terminal)
  - [Running the Django Server](#running-the-django-server)
  - [Useful Resources](#useful-resources)

# Agdesk Farm Management

This repository provides the source code for AgDesk Farm Management, a web-based application designed to streamline and optimize farm operations.

`This guide assumes that AgDesk is being configured on a Windows x64 based operating environment`

# Platform Setup Instructions

To understand the Company Guidelines for Programming, click [here][Guidelines]

In case you can't see the images below, please check `Platform Setup Instructions` in the link above.

[PostgreSQL]: https://www.postgresql.org/download/
[Python]: https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
[PythonCode]: https://www.w3schools.com/python/
[Django]: https://docs.djangoproject.com/en/5.1/
[Guidelines]: https://drive.google.com/drive/folders/1zdl1Sj5JfqQgwdTPyQeEQtGngYgkfSun?usp=drive_link

## Install PostGIS Database

- [Install the latest version of PostgreSQL][PostgreSQL]
- Go with the default settings for everything except for things mentioned below.
  - Set password as `pass`
  - Select `port 5432` (or your port)
  - Select `PostgreSQL 16 (x64) on port 5432` (or your port) from the drop down menu.
- Check `ADD TO PYTHON PATH` or something similar on one of the pages.
- When you reach the following page, select the options mentioned below:
  - Expand the Database server option, then ensure that `PostgreSQL (64 bit) v16.4-1` is checked
  - Select the Spatial Extensions option and check the box called `PostGIS 3.4.2 bundle for PostgreSQL 16 (64 bit) v3.4.2`

![gisExtension](https://i.imgur.com/wnGnOgX.jpg)

- Ensure the selected packages to install are correct before proceding.  
 `If the installer stops responding - WAIT! It will resume`
- On the following menu, leave the option to `skip installation` unchecked and click next.
- Accept the license agreement in the PostGIS Bundle popup window
- On the Choose components menu, ensure that the following boxes are checked:
  - `PostGIS Bundle`
  - `Register PROJ_LIB Env Variable`
  - `Register GDAL_DATA Env Variable`
  - `Enable Key GDAL Drivers`
  - `Allow Out-db Rasters`
  - `Register SSL Bundle`
- Set the install location of PostGIS. Installing it in the default listed directory is recommended for simplicity.
- Select Close and Finish the installation.
- SQL Shell and pgAdmin4 will be installed automatically once the installation above finishes.

## pgAdmin4

- Open `pgAdmin4` and log in with the password used during installation.
- Go to `Servers -> PostgreSQL 16 -> Databases` and right-click it to create a new database named `agdesk`.

![gisExtension](https://i.imgur.com/2D9ybmN.png)

## SQL Shell

- Open `SQL Shell`. Everything in square brackets is the default value. Hit enter to keep the default values. Only change the default value of Database to `agdesk` and Password to `pass` (installation password).

  ![Untitled](https://i.imgur.com/6RX5kzO.png)

## VS CODE EXPLORER

- Navigate to the project's web folder and copy contents of `.env_defaults` onto a new `.env` file.
- Change the password here if needed

![gisExtension](https://i.imgur.com/SglJuCT.png)

## Using Terminal

- Clone this repo and change directory in the terminal to where the repo is stored.
- [Install Python version 3.12][Python]
- Execute the code in a terminal (command prompt for Windows users):
- Check if Python version 3.12 is installed using `py -0`.
- Create and activate virtual environment:

 ```shell
  py -3.12 -m venv venv
  .\venv\Scripts\activate.bat
```

- Install all the required packages:

```shell
  pip install -r requirements.txt
```

- Check if the requirements were installed using `pip list`
- Move to AgDeskDjango directory `cd AgDeskDjango`
- Run the following commands in this directory:

```shell
python delete_migrations.py
```

```shell
python manage.py makemigrations
```

```shell
python manage.py migrate
```

Upon re-opening PgAdmin4, all of the models from Django should now have a tabular representation in the following directory `Servers -> PostgreSQL 16 -> Databases -> agdesk -> Schemas -> Tables`

![gisExtension](https://i.imgur.com/5kUDsQ2.png)

## Running the Django Server

Confirm that the application works by running the following from the root directory of the project.

```shell
python manage.py runserver
```

To check if the tables are being filled:
- Go to `Servers -> PostgreSQL 16 -> Databases -> agdesk -> Schemas -> Tables -> <table name>`
- Right click the `<table name>` and select `View/Edit Data -> All Rows`

![gisExtension](https://i.imgur.com/4927Eee.png)

## Useful Resources

- [Python Documentation][PythonCode]
- [Django Documentation][Django]
