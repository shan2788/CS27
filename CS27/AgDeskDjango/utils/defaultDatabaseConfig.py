"""
A local configuration file intended to be added to .gitignore shortly
"""

def databaseContext():
    try:
        databaseConfig = {
            'NAME': "AgDeskDjango",
            'USER': "postgres",
            'PASSWORD': "admin123",
        }
        return databaseConfig
    except:
        return {"err": "Something went wrong there!"}