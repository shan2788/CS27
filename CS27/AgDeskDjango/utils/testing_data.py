"""
This file contains the code and seed data necessary to generate all of the testing data for AgDesk.
"""

# Imports
from datetime import datetime, timedelta
from time import time


FARM_SET_VALID_FARM_NAME = [
    "Farm A",
    "Farm B",
    "Farm C",
    "Farm D",
    "Farm E",
    "Farm F",
    "Farm G",
    "Farm H",
    "Farm I",
    "Farm J"
]

FARM_SET_VALID_FARM_STREET = [
    "123 Example Street",
    "456 Another Street",
    "789 Sample Road"   ,
    "101 Test Avenue"   ,
    "202 Demo Boulevard",
    "303 Mock Lane"     ,
    "404 Fake Street"   ,
    "505 Real Road"     ,
    "606 Imaginary Blvd",
    "707 Fictional Ave"
]

FARM_SET_VALID_FARM_STATE = [
    "Example State",
    "Sample State" ,
    "Test State"   ,
    "Demo State"   ,
    "Mock State"   ,
    "Alpha State"  ,
    "Beta State"   ,
    "Gamma State"  ,
    "Delta State"  ,
    "Epsilon State"
]

FARM_SET_VALID_FARM_POSTCODE = [
    "123456",
    "654321",
    "112233",
    "445566",
    "778899",
    "990011",
    "223344",
    "556677",
    "889900",
    "001122"
]

FARM_SET_VALID_FARM_BIO = [
    "This is a bio for Farm A. It is a large farm with many crops and animals."               ,
    "This is a bio for Farm B. It is a small farm specializing in organic vegetables."        ,
    "This is a bio for Farm C. It is a medium-sized farm with a focus on dairy production."   ,
    "Farm D is known for its extensive orchards and fruit production."                        ,
    "Farm E is a family-owned farm with a rich history in grain farming."                     ,
    "Farm F is a modern farm utilizing the latest technology in agriculture."                 ,
    "Farm G is an organic farm dedicated to sustainable farming practices."                   ,
    "Farm H is a livestock farm with a variety of animals including cows, pigs, and chickens.",
    "Farm I is a vineyard producing high-quality wines."                                      ,
    "Farm J is a flower farm known for its beautiful and diverse flower species."
]

FARM_SET_VALID_FARM_IMAGE = [
    "images/farm_images/farm_a.png",
    "images/farm_images/farm_b.png",
    "images/farm_images/farm_c.png",
    "images/farm_images/farm_d.png",
    "images/farm_images/farm_e.png",
    "images/farm_images/farm_f.png",
    "images/farm_images/farm_g.png",
    "images/farm_images/farm_h.png",
    "images/farm_images/farm_i.png",
    "images/farm_images/farm_j.png"
]

FARM_SET_VALID_BOUNDARY_FARM_NAME = [
    "A"      , # Minimum length
    "A" * 100  # Maximum length
]

FARM_SET_VALID_BOUNDARY_FARM_STREET = [
    "A"      , # Minimum length
    "A" * 100  # Maximum length
]

FARM_SET_VALID_BOUNDARY_FARM_STATE = [
    "A"     , # Minimum length
    "A" * 20  # Maximum length
]

FARM_SET_VALID_BOUNDARY_FARM_POSTCODE = [
    "A"    , # Minimum length
    "A" * 6  # Maximum length
]

FARM_SET_VALID_BOUNDARY_FARM_BIO = [
    "A"       , # Minimum length
    "A" * 1000  # Arbitrary large length for testing
]

FARM_SET_VALID_BOUNDARY_FARM_IMAGE = [
    "images/farm_images/a.png"          , # Minimum valid path
    f"images/farm_images/{'a' * 80}.png"  # Long valid path
]

FARM_SET_INVALID_FARM_NAME = [
    ""          , # Empty string
    "A" * 101   , # Exceeds max length of 100
    None        , # None value
    123         , # Non-string value
    "Farm@Name!", # Special characters
    " " * 10      # Only spaces
]

FARM_SET_INVALID_FARM_STREET = [
    ""            , # Empty string
    "A" * 101     , # Exceeds max length of 100
    None          , # None value
    456           , # Non-string value
    "Street@Name!", # Special characters
    " " * 10        # Only spaces
]

FARM_SET_INVALID_FARM_STATE = [
    ""           , # Empty string
    "A" * 21     , # Exceeds max length of 20
    None         , # None value
    789          , # Non-string value
    "State@Name!", # Special characters
    " " * 10       # Only spaces
]

FARM_SET_INVALID_FARM_POSTCODE = [
    ""          , # Empty string
    "A" * 7     , # Exceeds max length of 6
    None        , # None value
    112233      , # Non-string value
    "Post@Code!", # Special characters
    " " * 10      # Only spaces
]

FARM_SET_INVALID_FARM_BIO = [
    ""         , # Empty string
    None       , # None value
    12345      , # Non-string value
    "Bio@Text!", # Special characters
    " " * 10     # Only spaces
]

FARM_SET_INVALID_FARM_IMAGE = [
    ""                                    , # Empty string
    None                                  , # None value
    "invalid_path"                        , # Invalid file path
    12345                                 , # Non-string value
    "images/farm_images/invalid_image.txt", # Invalid file type
    " " * 10                                # Only spaces
]

FARM_SET_INVALID_BOUNDARY_FARM_NAME = [
    ""       , # Empty string
    "A" * 101  # Exceeds max length of 100
]

FARM_SET_INVALID_BOUNDARY_FARM_STREET = [
    ""       , # Empty string
    "A" * 101  # Exceeds max length of 100
]

FARM_SET_INVALID_BOUNDARY_FARM_STATE = [
    ""      , # Empty string
    "A" * 21  # Exceeds max length of 20
]

FARM_SET_INVALID_BOUNDARY_FARM_POSTCODE = [
    ""     , # Empty string
    "A" * 7  # Exceeds max length of 6
]

FARM_SET_INVALID_BOUNDARY_FARM_BIO = [
    ""  , # Empty string
    None  # None value
]

FARM_SET_INVALID_BOUNDARY_FARM_IMAGE = [
    ""                                  , # Empty string
    None                                , # None value
    f"images/farm_images/{'a' * 81}.png"  # Exceeds typical file path length
]

FARM_SUPERSET = {
    "farm_name"    : [
        FARM_SET_VALID_FARM_NAME           ,
        FARM_SET_INVALID_FARM_NAME         ,
        FARM_SET_VALID_BOUNDARY_FARM_NAME  ,
        FARM_SET_INVALID_BOUNDARY_FARM_NAME
    ],
    "farm_street"  : [
        FARM_SET_VALID_FARM_STREET           ,
        FARM_SET_INVALID_FARM_STREET         ,
        FARM_SET_VALID_BOUNDARY_FARM_STREET  ,
        FARM_SET_INVALID_BOUNDARY_FARM_STREET
    ],
    "farm_state"   : [
        FARM_SET_VALID_FARM_STATE           ,
        FARM_SET_INVALID_FARM_STATE         ,
        FARM_SET_VALID_BOUNDARY_FARM_STATE  ,
        FARM_SET_INVALID_BOUNDARY_FARM_STATE
    ],
    "farm_postcode": [
        FARM_SET_VALID_FARM_POSTCODE           ,
        FARM_SET_INVALID_FARM_POSTCODE         ,
        FARM_SET_VALID_BOUNDARY_FARM_POSTCODE  ,
        FARM_SET_INVALID_BOUNDARY_FARM_POSTCODE
    ],
    "farm_bio"     : [
        FARM_SET_VALID_FARM_BIO           ,
        FARM_SET_INVALID_FARM_BIO         ,
        FARM_SET_VALID_BOUNDARY_FARM_BIO  ,
        FARM_SET_INVALID_BOUNDARY_FARM_BIO
    ],
    "farm_image"   : [
        FARM_SET_VALID_FARM_IMAGE           ,
        FARM_SET_INVALID_FARM_IMAGE         ,
        FARM_SET_VALID_BOUNDARY_FARM_IMAGE  ,
        FARM_SET_INVALID_BOUNDARY_FARM_IMAGE
    ]
}

FILERECORD_SET_VALID_FILE_NAME = [
    "Document A"         ,
    "Farm Report"        ,
    "Annual Summary"     ,
    "Financial Statement",
    "Crop Data"          ,
    "Livestock Records"  ,
    "Soil Analysis"      ,
    "Weather Data"       ,
    "Pesticide Usage"    ,
    "Harvest Report"
]

FILERECORD_SET_VALID_BOUNDARY_FILE_NAME = [
    "A"      , # Minimum length
    "A" * 100  # Maximum length
]

FILERECORD_SET_INVALID_FILE_NAME = [
    ""          , # Empty string
    "A" * 101   , # Exceeds max length of 100
    None        , # None value
    12345       , # Non-string value
    "File@Name!", # Special characters
    " " * 10      # Only spaces
]

FILERECORD_SET_INVALID_BOUNDARY_FILE_NAME = [
    ""       , # Empty string
    "A" * 101  # Exceeds max length of 100
]

FILERECORD_SET_VALID_REVIEW_DATE = [
    "2023-01-01",
    "2023-06-15",
    "2023-12-31",
    "2024-03-20",
    "2024-09-10",
    "2025-05-05",
    "2025-11-25",
    "2026-07-07",
    "2026-02-14",
    "2027-08-30"
]

FILERECORD_SET_VALID_BOUNDARY_REVIEW_DATE = [
    "1900-01-01", # Very old date
    "9999-12-31"  # Far future date
]

FILERECORD_SET_INVALID_REVIEW_DATE = [
    "2023-13-01"  , # Invalid month
    "2023-00-10"  , # Invalid month
    "2023-02-30"  , # Invalid day
    "2023-04-31"  , # Invalid day
    "2023-06-31"  , # Invalid day
    "2023-11-31"  , # Invalid day
    "2023-12-32"  , # Invalid day
    "2023-02-29"  , # Invalid leap year day
    "invalid-date", # Non-date string
    123456          # Non-string value
]

FILERECORD_SET_INVALID_BOUNDARY_REVIEW_DATE = [
    "2023-13-01"  , # Invalid month
    "2023-00-10"  , # Invalid month
    "2023-02-30"  , # Invalid day
    "2023-04-31"  , # Invalid day
    "2023-06-31"  , # Invalid day
    "2023-11-31"  , # Invalid day
    "2023-12-32"  , # Invalid day
    "2023-02-29"  , # Invalid leap year day
    "invalid-date", # Non-date string
    123456          # Non-string value
]

FILERECORD_SET_VALID_FILE = [
    "files/document_a.pdf"         ,
    "files/farm_report.docx"       ,
    "files/annual_summary.xlsx"    ,
    "files/financial_statement.pdf",
    "files/crop_data.csv"          ,
    "files/livestock_records.docx" ,
    "files/soil_analysis.pdf"      ,
    "files/weather_data.csv"       ,
    "files/pesticide_usage.xlsx"   ,
    "files/harvest_report.pdf"
]

FILERECORD_SET_VALID_BOUNDARY_FILE = [
    "files/a.pdf"          , # Minimum valid path
    f"files/{'a' * 80}.pdf"  # Long valid path
]

FILERECORD_SET_INVALID_FILE = [
    ""                      , # Empty string
    None                    , # None value
    "invalid_path"          , # Invalid file path
    12345                   , # Non-string value
    "files/invalid_file.txt", # Invalid file type
    " " * 10                  # Only spaces
]

FILERECORD_SET_INVALID_BOUNDARY_FILE = [
    ""                     , # Empty string
    None                   , # None value
    f"files/{'a' * 81}.pdf"   # Exceeds typical file path length
]

FILERECORD_SET_VALID_FILE_CATEGORY = [
    1 , # Assuming ID 1 corresponds to a valid FileCategory
    2 , # Assuming ID 2 corresponds to a valid FileCategory
    3 , # Assuming ID 3 corresponds to a valid FileCategory
    4 , # Assuming ID 4 corresponds to a valid FileCategory
    5 , # Assuming ID 5 corresponds to a valid FileCategory
    6 , # Assuming ID 6 corresponds to a valid FileCategory
    7 , # Assuming ID 7 corresponds to a valid FileCategory
    8 , # Assuming ID 8 corresponds to a valid FileCategory
    9 , # Assuming ID 9 corresponds to a valid FileCategory
    10  # Assuming ID 10 corresponds to a valid FileCategory
]

FILERECORD_SET_VALID_BOUNDARY_FILE_CATEGORY = [
    1, # Assuming ID 1 corresponds to a valid FileCategory
    2  # Assuming ID 2 corresponds to a valid FileCategory
]

FILERECORD_SET_INVALID_FILE_CATEGORY = [
    None     , # None value
    "invalid", # Non-integer value
    -1       , # Invalid negative ID
    99999    , # Non-existent ID
    0        , # Zero ID
    1.5      , # Non-integer value
    {}       , # Invalid type (dictionary)
    []       , # Invalid type (list)
    True     , # Invalid type (boolean)
    "1"        # String instead of integer
]

FILERECORD_SET_INVALID_BOUNDARY_FILE_CATEGORY = [
    None , # None value
    -1   , # Invalid negative ID
    99999, # Non-existent ID
    0      # Zero ID
]

FILRECORD_SUPERSET = {
    "fileName"    : [
        FILERECORD_SET_VALID_FILE_NAME           ,
        FILERECORD_SET_INVALID_FILE_NAME         ,
        FILERECORD_SET_VALID_BOUNDARY_FILE_NAME  ,
        FILERECORD_SET_INVALID_BOUNDARY_FILE_NAME
    ],
    "reviewDate"  : [
        FILERECORD_SET_VALID_REVIEW_DATE           ,
        FILERECORD_SET_INVALID_REVIEW_DATE         ,
        FILERECORD_SET_VALID_BOUNDARY_REVIEW_DATE  ,
        FILERECORD_SET_INVALID_BOUNDARY_REVIEW_DATE
    ],
    "file"        : [
        FILERECORD_SET_VALID_FILE           ,
        FILERECORD_SET_INVALID_FILE         ,
        FILERECORD_SET_VALID_BOUNDARY_FILE  ,
        FILERECORD_SET_INVALID_BOUNDARY_FILE
    ],
    "fileCategory": [
        FILERECORD_SET_VALID_FILE_CATEGORY           ,
        FILERECORD_SET_INVALID_FILE_CATEGORY         ,
        FILERECORD_SET_VALID_BOUNDARY_FILE_CATEGORY  ,
        FILERECORD_SET_INVALID_BOUNDARY_FILE_CATEGORY
    ]
}

FARMCONTACTS_SET_VALID_FARM_ID = [
    1, # Assuming ID 1 corresponds to a valid FarmInfo
    2, # Assuming ID 2 corresponds to a valid FarmInfo
    3, # Assuming ID 3 corresponds to a valid FarmInfo
    4, # Assuming ID 4 corresponds to a valid FarmInfo
    5  # Assuming ID 5 corresponds to a valid FarmInfo
]

FARMCONTACTS_SET_BOUNDARY_VALID_FARM_ID = [
    1 , # Assuming ID 1 corresponds to a valid FarmInfo
    2 , # Assuming ID 2 corresponds to a valid FarmInfo
]

FARMCONTACTS_SET_INVALID_FARM_ID = [
    None     , # None value
    99999    , # Non-existent ID
    -1       , # Negative value
    0        , # Zero ID
    "invalid"  # Non-integer value
]

FARMCONTACTS_SET_BOUNDARY_INVALID_FARM_ID = [
    None , # None value
    -1   , # Invalid negative ID
    99999, # Non-existent ID
    0      # Zero ID
]

FARMCONTACTS_SET_VALID_ORDER = [
    1,
    2,
    3,
    4,
    5
]

FARMCONTACTS_SET_BOUNDARY_VALID_ORDER = [
    1         , # Minimum positive integer
    2147483647  # Maximum value for a 32-bit signed integer
]

FARMCONTACTS_SET_INVALID_ORDER = [
    0        , # Zero value
    "invalid", # Non-integer value
    None     , # None value
    1.5        # Non-integer value
]

FARMCONTACTS_SET_BOUNDARY_INVALID_ORDER = [
    0         , # Zero value
    2147483648  # Exceeds maximum value for a 32-bit signed integer
]


FARMCONTACTS_SET_VALID_NAME = [
    "John Doe"     ,
    "Jane Smith"   ,
    "Alice Johnson",
    "Bob Brown"    ,
    "Charlie Davis"
]

FARMCONTACTS_SET_BOUNDARY_VALID_NAME = [
    "A"     , # Minimum length
    "A" * 64  # Maximum length
]

FARMCONTACTS_SET_INVALID_NAME = [
    ""        , # Empty string
    "A" * 65  , # Exceeds max length of 64
    None      , # None value
    12345     , # Non-string value
    "Name@123", # Special characters
    " " * 10    # Only spaces
]

FARMCONTACTS_SET_BOUNDARY_INVALID_NAME = [
    ""      , # Empty string
    "A" * 65  # Exceeds max length of 64
]

FARMCONTACTS_SET_VALID_IMAGE = [
    "images/contact_images/john_doe.png"     ,
    "images/contact_images/jane_smith.png"   ,
    "images/contact_images/alice_johnson.png",
    "images/contact_images/bob_brown.png"    ,
    "images/contact_images/charlie_davis.png"
]

FARMCONTACTS_SET_BOUNDARY_VALID_IMAGE = [
    "images/contact_images/a.png"          , # Minimum valid path
    f"images/contact_images/{'a' * 60}.png"  # Long valid path
]

FARMCONTACTS_SET_INVALID_IMAGE = [
    ""                                      , # Empty string
    None                                    , # None value
    "invalid_path"                          , # Invalid file path
    12345                                   , # Non-string value
    "images/contact_images/invalid_file.txt", # Invalid file type
    " " * 10                                  # Only spaces
]

FARMCONTACTS_SET_BOUNDARY_INVALID_IMAGE = [
    ""                                     , # Empty string
    None                                   , # None value
    f"images/contact_images/{'a' * 81}.png"  # Exceeds typical file path length
]

FARMCONTACTS_SET_VALID_DESC = [
    "Farm Manager"        ,
    "Assistant Manager"   ,
    "Field Supervisor"    ,
    "Livestock Specialist",
    "Crop Specialist"
]

FARMCONTACTS_SET_BOUNDARY_VALID_DESC = [
    "A"      , # Minimum length
    "A" * 128  # Maximum length
]

FARMCONTACTS_SET_INVALID_DESC = [
    ""        , # Empty string
    "A" * 129 , # Exceeds max length of 128
    None      , # None value
    12345     , # Non-string value
    "Desc@123", # Special characters
    " " * 10    # Only spaces
]

FARMCONTACTS_SET_BOUNDARY_INVALID_DESC = [
    ""       , # Empty string
    "A" * 129  # Exceeds max length of 128
]

#This should also be used for boundary testing
FARMCONTACTS_SET_VALID_DELETED = [
    False,
    True
]

#This should also be used for boundary testing
FARMCONTACTS_SET_INVALID_DELETED = [
    None     , # None value
    "invalid", # Non-boolean value
    12345    , # Non-boolean value
    "True"   , # String instead of boolean
    "False"    # String instead of boolean
]

FARMCONTACTS_SUPERSET = {
    "farmID" : [
        FARMCONTACTS_SET_VALID_FARM_ID           ,
        FARMCONTACTS_SET_INVALID_FARM_ID         ,
        FARMCONTACTS_SET_BOUNDARY_VALID_FARM_ID  ,
        FARMCONTACTS_SET_BOUNDARY_INVALID_FARM_ID
    ],
    "order"  : [
        FARMCONTACTS_SET_VALID_ORDER           ,
        FARMCONTACTS_SET_INVALID_ORDER         ,
        FARMCONTACTS_SET_BOUNDARY_VALID_ORDER  ,
        FARMCONTACTS_SET_BOUNDARY_INVALID_ORDER
    ],
    "name"   : [
        FARMCONTACTS_SET_VALID_NAME           ,
        FARMCONTACTS_SET_INVALID_NAME         ,
        FARMCONTACTS_SET_BOUNDARY_VALID_NAME  ,
        FARMCONTACTS_SET_BOUNDARY_INVALID_NAME
    ],
    "image"  : [
        FARMCONTACTS_SET_VALID_IMAGE           ,
        FARMCONTACTS_SET_INVALID_IMAGE         ,
        FARMCONTACTS_SET_BOUNDARY_VALID_IMAGE  ,
        FARMCONTACTS_SET_BOUNDARY_INVALID_IMAGE
    ],
    "desc"   : [
        FARMCONTACTS_SET_VALID_DESC           ,
        FARMCONTACTS_SET_INVALID_DESC         ,
        FARMCONTACTS_SET_BOUNDARY_VALID_DESC  ,
        FARMCONTACTS_SET_BOUNDARY_INVALID_DESC
    ],
    "deleted": [
        FARMCONTACTS_SET_VALID_DELETED  ,
        FARMCONTACTS_SET_INVALID_DELETED
    ]
}

CONTACTINFO_SET_VALID_FARM_CONTACT_ID = [
    1, # Assuming ID 1 corresponds to a valid FarmContacts
    2, # Assuming ID 2 corresponds to a valid FarmContacts
    3, # Assuming ID 3 corresponds to a valid FarmContacts
    4, # Assuming ID 4 corresponds to a valid FarmContacts
    5  # Assuming ID 5 corresponds to a valid FarmContacts
]

CONTACTINFO_SET_BOUNDARY_VALID_FARM_CONTACT_ID = [
    1, # Assuming ID 1 corresponds to a valid FarmContacts
    2  # Assuming ID 2 corresponds to a valid FarmContacts
]

CONTACTINFO_SET_INVALID_FARM_CONTACT_ID = [
    None     , # None value
    99999    , # Non-existent ID
    0        , # Zero ID
    "invalid"  # Non-integer value
]

CONTACTINFO_SET_BOUNDARY_INVALID_FARM_CONTACT_ID = [
    None, # None value
]

CONTACTINFO_SET_VALID_ORDER = [
    1,
    2,
    3,
    4,
    5
]

CONTACTINFO_SET_BOUNDARY_VALID_ORDER = [
    1         , # Minimum positive integer
    2147483647, # Maximum value for a 32-bit signed integer
]

CONTACTINFO_SET_INVALID_ORDER = [
    "invalid", # Non-integer value
    None     , # None value
    1.5        # Non-integer value
]

CONTACTINFO_SET_BOUNDARY_INVALID_ORDER = [
    "invalid"
]

CONTACTINFO_SET_VALID_FIELD = [
    "PH", # Phone
    "EM", # Email
    "AD", # Address
    "WB", # Website
    "NA"  # Other
]

CONTACTINFO_SET_BOUNDARY_VALID_FIELD = [
    "PH", # Phone
    "EM", # Email
    "AD", # Address
    "WB", # Website
    "NA"  # Other
]

CONTACTINFO_SET_INVALID_FIELD = [
    ""   , # Empty string
    "A"  , # Less than 2 characters
    "AA" , # Not in FIELD_CHOICES
    "XX" , # Not in FIELD_CHOICES
    None , # None value
    12345  # Non-string value
]

CONTACTINFO_SET_BOUNDARY_INVALID_FIELD = [
    ""  , # Empty string
    "A" , # Less than 2 characters
    "AA", # Not in FIELD_CHOICES
    "XX", # Not in FIELD_CHOICES
    None  # None value
]

CONTACTINFO_SET_VALID_INFO = [
    "123-456-7890"              , # Phone number
    "example@example.com"       , # Email address
    "123 Farm Lane, Farmville"  , # Address
    "http://www.farmwebsite.com", # Website
    "Additional info"             # Other
]

CONTACTINFO_SET_BOUNDARY_VALID_INFO = [
    "A"     , # Minimum length
    "A" * 64  # Maximum length
]

CONTACTINFO_SET_INVALID_INFO = [
    ""      , # Empty string
    "A" * 65, # Exceeds max length of 64
    None    , # None value
    12345   , # Non-string value
    " " * 10  # Only spaces
]

CONTACTINFO_SET_BOUNDARY_INVALID_INFO = [
    ""      , # Empty string
    "A" * 65, # Exceeds max length of 64
    None      # None value
]

CONTACTINFO_SET_VALID_DELETED = [
    False,
    True
]

CONTACTINFO_SET_INVALID_DELETED = [
    None     , # None value
    "invalid", # Non-boolean value
    12345    , # Non-boolean value
    "True"   , # String instead of boolean
    "False"    # String instead of boolean
]

CONTACTINFO_SUPERSET = {
    "farmContactID": [
        CONTACTINFO_SET_VALID_FARM_CONTACT_ID           ,
        CONTACTINFO_SET_INVALID_FARM_CONTACT_ID         ,
        CONTACTINFO_SET_BOUNDARY_VALID_FARM_CONTACT_ID  ,
        CONTACTINFO_SET_BOUNDARY_INVALID_FARM_CONTACT_ID
    ],
    "order"        : [
        CONTACTINFO_SET_VALID_ORDER           ,
        CONTACTINFO_SET_INVALID_ORDER         ,
        CONTACTINFO_SET_BOUNDARY_VALID_ORDER  ,
        CONTACTINFO_SET_BOUNDARY_INVALID_ORDER
    ],
    "field"        : [
        CONTACTINFO_SET_VALID_FIELD           ,
        CONTACTINFO_SET_INVALID_FIELD         ,
        CONTACTINFO_SET_BOUNDARY_VALID_FIELD  ,
        CONTACTINFO_SET_BOUNDARY_INVALID_FIELD
    ],
    "info"         : [
        CONTACTINFO_SET_VALID_INFO           ,
        CONTACTINFO_SET_INVALID_INFO         ,
        CONTACTINFO_SET_BOUNDARY_VALID_INFO  ,
        CONTACTINFO_SET_BOUNDARY_INVALID_INFO
    ],
    "deleted"      : [
        CONTACTINFO_SET_VALID_DELETED  ,
        CONTACTINFO_SET_INVALID_DELETED
    ]
}

# TODO: Styling done up to here

QUICKLINKS_SET_VALID_QUICKLINKNAME = [
    "Google", # Typical name
    "A" * 50  # Maximum length
]

QUICKLINKS_SET_BOUNDARY_VALID_QUICKLINKNAME = [
    "A", # Minimum length
    "A" * 50  # Maximum length
]

QUICKLINKS_SET_INVALID_QUICKLINKNAME = [
    "", # Empty string
    "A" * 51, # Exceeds max length of 50
    None, # None value
    12345  # Non-string value
]

QUICKLINKS_SET_BOUNDARY_INVALID_QUICKLINKNAME = [
    "", # Empty string
    "A" * 51  # Exceeds max length of 50
]

QUICKLINKS_SET_VALID_LINK = [
    "http://www.google.com", # Typical URL
    "https://www.example.com/path/to/resource?query=param#fragment", # Complex URL
    "A" * 255  # Maximum length
]

QUICKLINKS_SET_BOUNDARY_VALID_LINK = [
    "A", # Minimum length
    "A" * 255  # Maximum length
]

QUICKLINKS_SET_INVALID_LINK = [
    "", # Empty string
    "A" * 256, # Exceeds max length of 255
    None, # None value
    "invalid_url", # Invalid URL format
    12345  # Non-string value
]

QUICKLINKS_SET_BOUNDARY_INVALID_LINK = [
    "", # Empty string
    "A" * 256  # Exceeds max length of 255
]

QUICKLINKS_SET_VALID_ICON = [
    "images/quick_link_icons/icon1.png", # Typical image path
    "images/quick_link_icons/" + "a" * 80 + ".png"  # Long valid path
]

QUICKLINKS_SET_BOUNDARY_VALID_ICON = [
    "images/quick_link_icons/a.png", # Minimum valid path
    "images/quick_link_icons/" + "a" * 80 + ".png"  # Long valid path
]

QUICKLINKS_SET_INVALID_ICON = [
    "", # Empty string
    None, # None value
    "images/quick_link_icons/" + "a" * 81 + ".png", # Exceeds typical file path length
    "invalid_path", # Invalid file path
    12345  # Non-string value
]

QUICKLINKS_SET_BOUNDARY_INVALID_ICON = [
    "", # Empty string
    "images/quick_link_icons/" + "a" * 81 + ".png"  # Exceeds typical file path length
]

QUICKLINKS_SET_VALID_USER = [
    1, # Assuming ID 1 corresponds to a valid UserProfile
    2   # Assuming ID 2 corresponds to a valid UserProfile
]

QUICKLINKS_SET_BOUNDARY_VALID_USER = [
    1, # Assuming ID 1 corresponds to a valid UserProfile
    2   # Assuming ID 2 corresponds to a valid UserProfile
]

QUICKLINKS_SET_INVALID_USER = [
    None, # None value
    -1, # Invalid negative ID
    99999, # Non-existent ID
    0, # Zero ID
    "invalid"  # Non-integer value
]

QUICKLINKS_SET_BOUNDARY_INVALID_USER = [
    None, # None value
    -1, # Invalid negative ID
    0  # Zero ID
]

QUICKLINKS_SUPERSET = {
    "quickLinkName"   : [
        QUICKLINKS_SET_VALID_QUICKLINKNAME,
        QUICKLINKS_SET_INVALID_QUICKLINKNAME,
        QUICKLINKS_SET_BOUNDARY_VALID_QUICKLINKNAME,
        QUICKLINKS_SET_BOUNDARY_INVALID_QUICKLINKNAME],
    "link"            : [
        QUICKLINKS_SET_VALID_LINK,
        QUICKLINKS_SET_INVALID_LINK,
        QUICKLINKS_SET_BOUNDARY_VALID_LINK,
        QUICKLINKS_SET_BOUNDARY_INVALID_LINK],
    "icon"            : [
        QUICKLINKS_SET_VALID_ICON,
        QUICKLINKS_SET_INVALID_ICON,
        QUICKLINKS_SET_BOUNDARY_VALID_ICON,
        QUICKLINKS_SET_BOUNDARY_INVALID_ICON],
    "user"            : [
        QUICKLINKS_SET_VALID_USER,
        QUICKLINKS_SET_INVALID_USER,
        QUICKLINKS_SET_BOUNDARY_VALID_USER,
        QUICKLINKS_SET_BOUNDARY_INVALID_USER]
}

OPERATIONLOG_SET_VALID_ASSETID = [
    1, # Assuming ID 1 corresponds to a valid asset
    2   # Assuming ID 2 corresponds to a valid asset
]

OPERATIONLOG_SET_VALID_BOUNDARY_ASSETID = [
    1, # Assuming ID 1 corresponds to a valid asset
    2   # Assuming ID 2 corresponds to a valid asset
]

OPERATIONLOG_SET_INVALID_ASSETID = [
    None, # None value
    -1, # Invalid negative ID
    99999, # Non-existent ID
    0, # Zero ID
    "invalid"  # Non-integer value
]

OPERATIONLOG_SET_INVALID_BOUNDARY_ASSETID = [
    None, # None value
    -1, # Invalid negative ID
    0  # Zero ID
]

OPERATIONLOG_SET_VALID_USERID = [
    1, # Assuming ID 1 corresponds to a valid UserProfile
    2   # Assuming ID 2 corresponds to a valid UserProfile
]

OPERATIONLOG_SET_VALID_BOUNDARY_USERID = [
    1, # Assuming ID 1 corresponds to a valid UserProfile
    2   # Assuming ID 2 corresponds to a valid UserProfile
]

OPERATIONLOG_SET_INVALID_USERID = [
    None, # None value
    -1, # Invalid negative ID
    99999, # Non-existent ID
    0, # Zero ID
    "invalid"  # Non-integer value
]

OPERATIONLOG_SET_INVALID_BOUNDARY_USERID = [
    None, # None value
    -1, # Invalid negative ID
    0  # Zero ID
]


OPERATIONLOG_SET_VALID_STARTDATETIME = [
    datetime.now(), # Current date and time
    datetime.now() - timedelta(days=1)  # One day in the past
]

OPERATIONLOG_SET_INVALID_STARTDATETIME = [
    "invalid_date", # Invalid date format
    None, # None value
    12345  # Non-datetime value
]

OPERATIONLOG_SET_INVALID_BOUNDARY_STARTDATETIME = [
    "invalid_date", # Invalid date format
    None, # None value
    12345  # Non-datetime value
]

OPERATIONLOG_SET_VALID_ENDDATETIME = [
    datetime.now() + timedelta(hours=1), # One hour in the future
    None  # Null value
]

OPERATIONLOG_SET_VALID_BOUNDARY_ENDDATETIME = [
    datetime.now() + timedelta(seconds=1), # Just after the current time
    None  # Null value
]

OPERATIONLOG_SET_INVALID_ENDDATETIME = [
    "invalid_date", # Invalid date format
    12345  # Non-datetime value
]

OPERATIONLOG_SET_INVALID_BOUNDARY_ENDDATETIME = [
    "invalid_date", # Invalid date format
    12345  # Non-datetime value
]

OPERATIONLOG_SET_VALID_LOCATION = [
    "Field A", # Typical location
    "A" * 64  # Maximum length
]

OPERATIONLOG_SET_VALID_BOUNDARY_LOCATION = [
    "A", # Minimum length
    "A" * 64  # Maximum length
]

OPERATIONLOG_SET_INVALID_LOCATION = [
    "", # Empty string
    "A" * 65, # Exceeds max length of 64
    None, # None value
    12345  # Non-string value
]

OPERATIONLOG_SET_INVALID_BOUNDARY_LOCATION = [
    "", # Empty string
    "A" * 65, # Exceeds max length of 64
    None, # None value
    12345  # Non-string value
]

OPERATIONLOG_SET_VALID_NOTES = [
    "Routine check-up", # Typical note
    "A" * 256, # Maximum length
    None  # Null value
]

OPERATIONLOG_SET_VALID_BOUNDARY_NOTES = [
    "A", # Minimum length
    "A" * 256, # Maximum length
    None  # Null value
]

OPERATIONLOG_SET_INVALID_NOTES = [
    "A" * 257, # Exceeds max length of 256
    12345  # Non-string value
]

OPERATIONLOG_SET_INVALID_BOUNDARY_NOTES = [
    "A" * 257, # Exceeds max length of 256
    12345  # Non-string value
]

OPERATIONLOG_SET_VALID_DELETED = [
    False,
    True
]

OPERATIONLOG_SET_INVALID_DELETED = [
    None, # None value
    "invalid", # Non-boolean value
    12345  # Non-boolean value
]

OPERATIONLOG_SUPERSET = {
    "assetID"       : [
        OPERATIONLOG_SET_VALID_ASSETID,
        OPERATIONLOG_SET_INVALID_ASSETID,
        OPERATIONLOG_SET_VALID_BOUNDARY_ASSETID,
        OPERATIONLOG_SET_INVALID_BOUNDARY_ASSETID],
    "userID"        : [
        OPERATIONLOG_SET_VALID_USERID,
        OPERATIONLOG_SET_INVALID_USERID,
        OPERATIONLOG_SET_VALID_BOUNDARY_USERID,
        OPERATIONLOG_SET_INVALID_BOUNDARY_USERID],
    "startDateTime" : [
        OPERATIONLOG_SET_VALID_STARTDATETIME,
        OPERATIONLOG_SET_INVALID_STARTDATETIME,
        OPERATIONLOG_SET_INVALID_BOUNDARY_STARTDATETIME],
    "endDateTime"   : [
        OPERATIONLOG_SET_VALID_ENDDATETIME,
        OPERATIONLOG_SET_INVALID_ENDDATETIME,
        OPERATIONLOG_SET_VALID_BOUNDARY_ENDDATETIME,
        OPERATIONLOG_SET_INVALID_BOUNDARY_ENDDATETIME],
    "location"      : [
        OPERATIONLOG_SET_VALID_LOCATION,
        OPERATIONLOG_SET_INVALID_LOCATION,
        OPERATIONLOG_SET_VALID_BOUNDARY_LOCATION,
        OPERATIONLOG_SET_INVALID_BOUNDARY_LOCATION],
    "notes"         : [
        OPERATIONLOG_SET_VALID_NOTES,
        OPERATIONLOG_SET_INVALID_NOTES,
        OPERATIONLOG_SET_VALID_BOUNDARY_NOTES,
        OPERATIONLOG_SET_INVALID_BOUNDARY_NOTES],
    "deleted"       : [
        OPERATIONLOG_SET_VALID_DELETED,
        OPERATIONLOG_SET_INVALID_DELETED
    ]
}

ASSET_SET_VALID_ASSETPREFIX = [
    "SE",
    "LE",
    "LV",
    "HV"
]

ASSET_SET_INVALID_ASSETPREFIX = [
    "", # Empty string
    "A", # Less than 2 characters
    "ABC", # More than 2 characters
    "123", # More than 2 characters and contains numbers
    None, # Null value
]

ASSET_SET_VALID_ASSETNAME = [
    "Tractor", # Within 100 characters
    "Combine Harvester", # Within 100 characters
    "Irrigation Pump", # Within 100 characters
    "Plow", # Within 100 characters
    "Seeder", # Within 100 characters
    "Sprayer", # Within 100 characters
    "Baler", # Within 100 characters
    "Cultivator", # Within 100 characters
    "Mower", # Within 100 characters
    "Harvester", # Within 100 characters
]

ASSET_SET_VALID_BOUNDARY_ASSETNAME = [
    "A", # Minimum length (1 character)
    "A" * 100, # Maximum length (100 characters)
]

ASSET_SET_INVALID_ASSETNAME = [
    "", # Empty string
    "A" * 101, # More than 100 characters
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_ASSETNAME = [
    "", # Empty string
    "A" * 101, # More than 100 characters
]

ASSET_SET_VALID_FARMID = [
    1, # Valid foreign key reference
    2, # Valid foreign key reference
    3, # Valid foreign key reference
    4, # Valid foreign key reference
    5, # Valid foreign key reference
    6, # Valid foreign key reference
    7, # Valid foreign key reference
    8, # Valid foreign key reference
    9, # Valid foreign key reference
    10, # Valid foreign key reference
]

# Assuming FarmInfo objects with IDs 1 and 2 exist
ASSET_SET_VALID_BOUNDARY_FARMID = [
    1, # Minimum valid foreign key reference
    2, # Another valid foreign key reference
]

ASSET_SET_INVALID_FARMID = [
    None, # Null value
    "invalid_id", # Non-integer value
    -1, # Negative integer
    999999, # Non-existent foreign key reference
]

ASSET_SET_INVALID_BOUNDARY_FARMID = [
    None, # Null value
    -1, # Negative integer
]

ASSET_SET_VALID_MANUFACTURER = [
    "John Deere", # Within 100 characters
    "Caterpillar", # Within 100 characters
    "Kubota", # Within 100 characters
    "New Holland", # Within 100 characters
    "Case IH", # Within 100 characters
    "Massey Ferguson", # Within 100 characters
    "Claas", # Within 100 characters
    "Fendt", # Within 100 characters
    "Valtra", # Within 100 characters
    "Deutz-Fahr", # Within 100 characters
]

ASSET_SET_VALID_BOUNDARY_MANUFACTURER = [
    "A", # Minimum length (1 character)
    "A" * 100, # Maximum length (100 characters)
]

ASSET_SET_VALID_BOUNDARY_MANUFACTURER = [
    "A", # Minimum length (1 character)
    "A" * 100, # Maximum length (100 characters)
]

ASSET_SET_INVALID_MANUFACTURER = [
    "A" * 101, # More than 100 characters
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_MANUFACTURER = [
    "A" * 101, # More than 100 characters
]

ASSET_SET_VALID_PARTSLIST = [
    "Engine, Transmission, Wheels", # Within 255 characters
    "Pump, Motor, Hose", # Within 255 characters
    "Battery, Alternator, Radiator", # Within 255 characters
    "Blade, Handle, Motor", # Within 255 characters
    "Gearbox, Chain, Sprocket", # Within 255 characters
    "Hydraulic Pump, Cylinder, Valve", # Within 255 characters
    "Fuel Tank, Fuel Pump, Injector", # Within 255 characters
    "Axle, Differential, Driveshaft", # Within 255 characters
    "Clutch, Flywheel, Pressure Plate", # Within 255 characters
    "Starter, Alternator, Battery", # Within 255 characters
]

ASSET_SET_VALID_BOUNDARY_PARTSLIST = [
    "A", # Minimum length (1 character)
    "A" * 255, # Maximum length (255 characters)
]

ASSET_SET_INVALID_PARTSLIST = [
    "A" * 256, # More than 255 characters
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_PARTSLIST = [
    "A" * 256, # More than 255 characters
]

ASSET_SET_VALID_LOCATION = [
    "Barn", # Within 100 characters
    "Field", # Within 100 characters
    "Garage", # Within 100 characters
    "Warehouse", # Within 100 characters
    "Shed", # Within 100 characters
    "Workshop", # Within 100 characters
    "Storage Room", # Within 100 characters
    "Hangar", # Within 100 characters
    "Depot", # Within 100 characters
    "Yard", # Within 100 characters
]

ASSET_SET_VALID_BOUNDARY_LOCATION = [
    "A", # Minimum length (1 character)
    "A" * 100, # Maximum length (100 characters)
]

ASSET_SET_INVALID_LOCATION = [
    "", # Empty string
    "A" * 101, # More than 100 characters
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_LOCATION = [
    "", # Empty string
    "A" * 101, # More than 100 characters
]

ASSET_SET_VALID_DATEMANUFACTURED = [
    "2020-01-01", # Valid date format
    "2019-05-15", # Valid date format
    "2018-11-30", # Valid date format
    "2017-07-20", # Valid date format
    "2016-03-10", # Valid date format
    "2015-09-25", # Valid date format
    "2014-12-05", # Valid date format
    "2013-08-18", # Valid date format
    "2012-04-22", # Valid date format
    "2011-10-30", # Valid date format
]

ASSET_SET_VALID_BOUNDARY_DATEMANUFACTURED = [
    "1900-01-01", # Earliest reasonable date
    "2100-12-31", # Latest reasonable date
]

ASSET_SET_INVALID_DATEMANUFACTURED = [
    "2020-13-01", # Invalid month
    "2020-00-01", # Invalid month
    "2020-01-32", # Invalid day
    "invalid_date", # Non-date string
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_DATEMANUFACTURED = [
    "1899-12-31", # Date before the earliest reasonable date
    "2101-01-01", # Date after the latest reasonable date
]

ASSET_SET_VALID_DATEPURCHASED = [
    "2020-02-01", # Valid date format
    "2019-06-15", # Valid date format
    "2018-12-30", # Valid date format
    "2017-08-20", # Valid date format
    "2016-04-10", # Valid date format
    "2015-10-25", # Valid date format
    "2014-01-05", # Valid date format
    "2013-09-18", # Valid date format
    "2012-05-22", # Valid date format
    "2011-11-30", # Valid date format
]

ASSET_SET_VALID_BOUNDARY_DATEPURCHASED = [
    "1900-01-01", # Earliest reasonable date
    "2100-12-31", # Latest reasonable date
]

ASSET_SET_INVALID_DATEPURCHASED = [
    "2020-13-01", # Invalid month
    "2020-00-01", # Invalid month
    "2020-01-32", # Invalid day
    "invalid_date", # Non-date string
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_DATEPURCHASED = [
    "1899-12-31", # Date before the earliest reasonable date
    "2101-01-01", # Date after the latest reasonable date
]

ASSET_SET_VALID_ASSETIMAGE = [
    "images/asset_images/defaultImage.jpg", # Default image path
    "images/asset_images/tractor.jpg", # Custom image path
    "images/asset_images/harvester.jpg", # Custom image path
    "images/asset_images/plow.jpg", # Custom image path
    "images/asset_images/seeder.jpg", # Custom image path
    "images/asset_images/sprayer.jpg", # Custom image path
    "images/asset_images/baler.jpg", # Custom image path
    "images/asset_images/cultivator.jpg", # Custom image path
    "images/asset_images/mower.jpg", # Custom image path
    "images/asset_images/harvester_large.jpg", # Custom image path
]

ASSET_SET_VALID_BOUNDARY_ASSETIMAGE = [
    "images/asset_images/defaultImage.jpg", # Default image path
    "images/asset_images/boundaryImage.jpg", # Custom image path
]

ASSET_SET_INVALID_ASSETIMAGE = [
    "", # Empty string
    "invalid_path", # Invalid path
    None, # Null value
]

ASSET_SET_INVALID_BOUNDARY_ASSETIMAGE = [
    "", # Empty string
    "invalid_path", # Invalid path
]

ASSET_SET_VALID_DELETED = [
    False, # Valid boolean value
    True, # Valid boolean value
]

ASSET_SET_INVALID_DELETED = [
    "yes", # Non-boolean string
    2, # Integer not representing a boolean
    None, # Null value
]

ASSET_SUPERSET = {
    "assetPrefix" : [
        ASSET_SET_VALID_ASSETPREFIX,
        ASSET_SET_INVALID_ASSETPREFIX],
    "assetName" : [
        ASSET_SET_VALID_ASSETNAME,
        ASSET_SET_INVALID_ASSETNAME,
        ASSET_SET_VALID_BOUNDARY_ASSETNAME,
        ASSET_SET_INVALID_BOUNDARY_ASSETNAME],
    "farmID" : [
        ASSET_SET_VALID_FARMID,
        ASSET_SET_INVALID_FARMID,
        ASSET_SET_VALID_BOUNDARY_FARMID,
        ASSET_SET_INVALID_BOUNDARY_FARMID],
    "manufacturer" : [
        ASSET_SET_VALID_MANUFACTURER,
        ASSET_SET_INVALID_MANUFACTURER,
        ASSET_SET_VALID_BOUNDARY_MANUFACTURER,
        ASSET_SET_INVALID_BOUNDARY_MANUFACTURER],
    "partsList" : [
        ASSET_SET_VALID_PARTSLIST,
        ASSET_SET_INVALID_PARTSLIST,
        ASSET_SET_VALID_BOUNDARY_PARTSLIST,
        ASSET_SET_INVALID_BOUNDARY_PARTSLIST],
    "location" : [
        ASSET_SET_VALID_LOCATION,
        ASSET_SET_INVALID_LOCATION,
        ASSET_SET_VALID_BOUNDARY_LOCATION,
        ASSET_SET_INVALID_BOUNDARY_LOCATION],
    "dateManufactured" : [
        ASSET_SET_VALID_DATEMANUFACTURED,
        ASSET_SET_INVALID_DATEMANUFACTURED,
        ASSET_SET_VALID_BOUNDARY_DATEMANUFACTURED,
        ASSET_SET_INVALID_BOUNDARY_DATEMANUFACTURED],
    "datePurchased" : [
        ASSET_SET_VALID_DATEPURCHASED,
        ASSET_SET_INVALID_DATEPURCHASED,
        ASSET_SET_VALID_BOUNDARY_DATEPURCHASED,
        ASSET_SET_INVALID_BOUNDARY_DATEPURCHASED],
    "assetImage" : [
        ASSET_SET_VALID_ASSETIMAGE,
        ASSET_SET_INVALID_ASSETIMAGE,
        ASSET_SET_VALID_BOUNDARY_ASSETIMAGE,
        ASSET_SET_INVALID_BOUNDARY_ASSETIMAGE],
    "deleted" : [
        ASSET_SET_VALID_DELETED,
        ASSET_SET_INVALID_DELETED
    ]
}

# Valid cases for serialNumber
SMALL_EQUIPMENT_VALID_SERIAL_NUMBER = [
    "A12345", # Typical valid serial number
    "1234567890" * 10, # Exactly 100 characters
    "B", # Exactly 1 character
    "C" * 50, # Exactly 50 characters
    "D1234567890", # 11 characters
    "E" * 99 + "F", # Exactly 100 characters
    "GHIJKL", # 6 characters
    "M" * 25, # Exactly 25 characters
    "N" * 75, # Exactly 75 characters
    "O" * 10, # Exactly 10 characters
]

# Invalid cases for serialNumber
SMALL_EQUIPMENT_INVALID_SERIAL_NUMBER = [
    None, # None value
    "", # Empty string
    "P" * 101, # 101 characters, exceeds the maximum length
    "Q" * 150, # 150 characters, exceeds the maximum length
    "R" * 200, # 200 characters, exceeds the maximum length
    "S" * 102, # 102 characters, exceeds the maximum length
    "T" * 110, # 110 characters, exceeds the maximum length
    "U" * 120, # 120 characters, exceeds the maximum length
    "V" * 130, # 130 characters, exceeds the maximum length
    "W" * 140, # 140 characters, exceeds the maximum length
]

# Boundary valid cases for serialNumber
SMALL_EQUIPMENT_BOUNDARY_VALID_SERIAL_NUMBER = [
    "X", # Exactly 1 character
    "Y" * 100, # Exactly 100 characters
    "Z" * 99 + "A", # Exactly 100 characters
    "B" * 2, # Exactly 2 characters
    "C" * 3, # Exactly 3 characters
    "D" * 4, # Exactly 4 characters
    "E" * 5, # Exactly 5 characters
    "F" * 6, # Exactly 6 characters
    "G" * 7, # Exactly 7 characters
    "H" * 8, # Exactly 8 characters
]

# Boundary invalid cases for serialNumber
SMALL_EQUIPMENT_BOUNDARY_INVALID_SERIAL_NUMBER = [
    "", # Empty string
    "I" * 101, # 101 characters, exceeds the maximum length
    "J" * 102, # 102 characters, exceeds the maximum length
    "K" * 103, # 103 characters, exceeds the maximum length
    "L" * 104, # 104 characters, exceeds the maximum length
    "M" * 105, # 105 characters, exceeds the maximum length
    "N" * 106, # 106 characters, exceeds the maximum length
    "O" * 107, # 107 characters, exceeds the maximum length
    "P" * 108, # 108 characters, exceeds the maximum length
    "Q" * 109, # 109 characters, exceeds the maximum length
]

SMALL_EQUIPMENT_SUPERSET = {
    "assetSuperset": ASSET_SUPERSET,
    "serialNumber": [
        SMALL_EQUIPMENT_VALID_SERIAL_NUMBER,
        SMALL_EQUIPMENT_INVALID_SERIAL_NUMBER,
        SMALL_EQUIPMENT_BOUNDARY_VALID_SERIAL_NUMBER,
        SMALL_EQUIPMENT_BOUNDARY_INVALID_SERIAL_NUMBER
    ]
}

# Valid cases for vin
LARGE_EQUIPMENT_VALID_VIN = [
    "1HGCM82633A123456", # Typical valid VIN
    "1234567890" * 10, # Exactly 100 characters
    "A", # Exactly 1 character
    "B" * 50, # Exactly 50 characters
    "C1234567890", # 11 characters
    "D" * 99 + "E", # Exactly 100 characters
    "FGHIJKL", # 7 characters
    "H" * 25, # Exactly 25 characters
    "I" * 75, # Exactly 75 characters
    "J" * 10, # Exactly 10 characters
]

# Invalid cases for vin
LARGE_EQUIPMENT_INVALID_VIN = [
    None, # None value
    "", # Empty string
    "K" * 101, # 101 characters, exceeds the maximum length
    "L" * 150, # 150 characters, exceeds the maximum length
    "M" * 200, # 200 characters, exceeds the maximum length
    "N" * 102, # 102 characters, exceeds the maximum length
    "O" * 110, # 110 characters, exceeds the maximum length
    "P" * 120, # 120 characters, exceeds the maximum length
    "Q" * 130, # 130 characters, exceeds the maximum length
    "R" * 140, # 140 characters, exceeds the maximum length
]

# Boundary valid cases for vin
LARGE_EQUIPMENT_BOUNDARY_VALID_VIN = [
    "S", # Exactly 1 character
    "T" * 100, # Exactly 100 characters
    "U" * 99 + "V", # Exactly 100 characters
    "W" * 2, # Exactly 2 characters
    "X" * 3, # Exactly 3 characters
    "Y" * 4, # Exactly 4 characters
    "Z" * 5, # Exactly 5 characters
    "A1" * 3, # Exactly 6 characters
    "B2" * 4, # Exactly 8 characters
    "C3" * 5, # Exactly 10 characters
]

# Boundary invalid cases for vin
LARGE_EQUIPMENT_BOUNDARY_INVALID_VIN = [
    "", # Empty string
    "D4" * 50 + "E", # 101 characters, exceeds the maximum length
    "F5" * 51, # 102 characters, exceeds the maximum length
    "G6" * 51 + "H", # 103 characters, exceeds the maximum length
    "I7" * 52, # 104 characters, exceeds the maximum length
    "J8" * 52 + "K", # 105 characters, exceeds the maximum length
    "L9" * 53, # 106 characters, exceeds the maximum length
    "M0" * 53 + "N", # 107 characters, exceeds the maximum length
    "O1" * 54, # 108 characters, exceeds the maximum length
    "P2" * 54 + "Q", # 109 characters, exceeds the maximum length
]

LARGE_EQUIPMENT_SUPERSET = {
    "assetSuperset": ASSET_SUPERSET,
    "vin": [
        LARGE_EQUIPMENT_VALID_VIN,
        LARGE_EQUIPMENT_INVALID_VIN,
        LARGE_EQUIPMENT_BOUNDARY_VALID_VIN,
        LARGE_EQUIPMENT_BOUNDARY_INVALID_VIN
    ]
}

# Valid cases for assetID
DAMAGE_VALID_ASSET_ID = [
    1, # Assuming 1 is a valid asset ID
    2, # Assuming 2 is a valid asset ID
    3, # Assuming 3 is a valid asset ID
    4, # Assuming 4 is a valid asset ID
    5, # Assuming 5 is a valid asset ID
]

# Invalid cases for assetID
DAMAGE_INVALID_ASSET_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for assetID
DAMAGE_BOUNDARY_VALID_ASSET_ID = [
    1, # Assuming 1 is a valid asset ID
]

# Boundary invalid cases for assetID
DAMAGE_BOUNDARY_INVALID_ASSET_ID = [
    None, # None value
]

# Valid cases for damageObservedDate
DAMAGE_VALID_DAMAGE_OBSERVED_DATE = [
    "2023-01-01", # Valid date
    "2022-12-31", # Valid date
    "2021-06-15", # Valid date
    "2020-02-29", # Leap year date
    "2019-07-04", # Valid date
]

# Invalid cases for damageObservedDate
DAMAGE_INVALID_DAMAGE_OBSERVED_DATE = [
    None, # None value
    "", # Empty string
    "invalid-date", # Invalid date format
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
]

# Boundary valid cases for damageObservedDate
DAMAGE_BOUNDARY_VALID_DAMAGE_OBSERVED_DATE = [
    "0001-01-01", # Minimum valid date
    "9999-12-31", # Maximum valid date
]

# Boundary invalid cases for damageObservedDate
DAMAGE_BOUNDARY_INVALID_DAMAGE_OBSERVED_DATE = [
    None, # None value
    "0000-00-00", # Invalid date
]

# Valid cases for damageOccuredDate
DAMAGE_VALID_DAMAGE_OCCURED_DATE = [
    "2023-01-01", # Valid date
    "2022-12-31", # Valid date
    "2021-06-15", # Valid date
    "2020-02-29", # Leap year date
    "2019-07-04", # Valid date
]

# Invalid cases for damageOccuredDate
DAMAGE_INVALID_DAMAGE_OCCURED_DATE = [
    "", # Empty string
    "invalid-date", # Invalid date format
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
]

# Boundary valid cases for damageOccuredDate
DAMAGE_BOUNDARY_VALID_DAMAGE_OCCURED_DATE = [
    "0001-01-01", # Minimum valid date
    "9999-12-31", # Maximum valid date
]

# Boundary invalid cases for damageOccuredDate
DAMAGE_BOUNDARY_INVALID_DAMAGE_OCCURED_DATE = [
    "0000-00-00", # Invalid date
]

# Valid cases for damageType
DAMAGE_VALID_DAMAGE_TYPE = [
    "Scratch", # Valid damage type
    "Dent", # Valid damage type
    "Crack", # Valid damage type
    "Broken", # Valid damage type
    "Corrosion", # Valid damage type
]

# Invalid cases for damageType
DAMAGE_INVALID_DAMAGE_TYPE = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for damageType
DAMAGE_BOUNDARY_VALID_DAMAGE_TYPE = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for damageType
DAMAGE_BOUNDARY_INVALID_DAMAGE_TYPE = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

# Valid cases for damageSeverity
DAMAGE_VALID_DAMAGE_SEVERITY = [
    0, # Assuming 0 is a valid choice
    1, # Assuming 1 is a valid choice
    2, # Assuming 2 is a valid choice
    3, # Assuming 3 is a valid choice
    4, # Assuming 4 is a valid choice
]

# Invalid cases for damageSeverity
DAMAGE_INVALID_DAMAGE_SEVERITY = [
    None, # None value
    -1, # Negative value
    5, # Assuming 5 is not a valid choice
    "invalid", # Non-integer value
]

# Boundary valid cases for damageSeverity
DAMAGE_BOUNDARY_VALID_DAMAGE_SEVERITY = [
    0, # Minimum valid choice
    4, # Maximum valid choice
]

# Boundary invalid cases for damageSeverity
DAMAGE_BOUNDARY_INVALID_DAMAGE_SEVERITY = [
    -1, # Negative value
    5, # Exceeds maximum valid choice
]

# Valid cases for notes
DAMAGE_VALID_NOTES = [
    "Minor scratch on the surface.", # Valid note
    "Dent on the left side.", # Valid note
    "Crack on the handle.", # Valid note
    "Broken part needs replacement.", # Valid note
    "Corrosion observed on the base.", # Valid note
]

# Invalid cases for notes
DAMAGE_INVALID_NOTES = [
    "A" * 256, # Exceeds maximum length
]

# Boundary valid cases for notes
DAMAGE_BOUNDARY_VALID_NOTES = [
    "", # Empty string
    "B" * 255, # Exactly 255 characters
]

# Boundary invalid cases for notes
DAMAGE_BOUNDARY_INVALID_NOTES = [
    "C" * 256, # Exceeds maximum length
]

# Valid cases for damageImage
DAMAGE_VALID_DAMAGE_IMAGE = [
    "damageImages/image1.jpg", # Valid image path
    "damageImages/image2.png", # Valid image path
    "damageImages/image3.gif", # Valid image path
    "damageImages/image4.bmp", # Valid image path
    "damageImages/image5.tiff", # Valid image path
]

# Invalid cases for damageImage
DAMAGE_INVALID_DAMAGE_IMAGE = [
    None, # None value
    "", # Empty string
    "invalid/path/to/image", # Invalid path
]

# Boundary valid cases for damageImage
DAMAGE_BOUNDARY_VALID_DAMAGE_IMAGE = [
    "images/asset_images/defaultImage.jpg", # Default image path
]

# Boundary invalid cases for damageImage
DAMAGE_BOUNDARY_INVALID_DAMAGE_IMAGE = [
    "", # Empty string
]

# Valid cases for scheduledMaintenanceDate
DAMAGE_VALID_SCHEDULED_MAINTENANCE_DATE = [
    "2023-01-01", # Valid date
    "2022-12-31", # Valid date
    "2021-06-15", # Valid date
    "2020-02-29", # Leap year date
    "2019-07-04", # Valid date
]

# Invalid cases for scheduledMaintenanceDate
DAMAGE_INVALID_SCHEDULED_MAINTENANCE_DATE = [
    "", # Empty string
    "invalid-date", # Invalid date format
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
]

# Boundary valid cases for scheduledMaintenanceDate
DAMAGE_BOUNDARY_VALID_SCHEDULED_MAINTENANCE_DATE = [
    "0001-01-01", # Minimum valid date
    "9999-12-31", # Maximum valid date
]

# Boundary invalid cases for scheduledMaintenanceDate
DAMAGE_BOUNDARY_INVALID_SCHEDULED_MAINTENANCE_DATE = [
    "0000-00-00", # Invalid date
]

# Valid cases for deleted
DAMAGE_VALID_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for deleted
DAMAGE_INVALID_DELETED = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for deleted
DAMAGE_BOUNDARY_VALID_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for deleted
DAMAGE_BOUNDARY_INVALID_DELETED = [
    None, # None value
]

DAMAGE_SUPERSET = {
    "assetID" : [
        DAMAGE_VALID_ASSET_ID,
        DAMAGE_INVALID_ASSET_ID,
        DAMAGE_BOUNDARY_VALID_ASSET_ID,
        DAMAGE_BOUNDARY_INVALID_ASSET_ID],
    "damageObservedDate" : [
        DAMAGE_VALID_DAMAGE_OBSERVED_DATE,
        DAMAGE_INVALID_DAMAGE_OBSERVED_DATE,
        DAMAGE_BOUNDARY_VALID_DAMAGE_OBSERVED_DATE,
        DAMAGE_BOUNDARY_INVALID_DAMAGE_OBSERVED_DATE],
    "damageOccuredDate" : [
        DAMAGE_VALID_DAMAGE_OCCURED_DATE,
        DAMAGE_INVALID_DAMAGE_OCCURED_DATE,
        DAMAGE_BOUNDARY_VALID_DAMAGE_OCCURED_DATE,
        DAMAGE_BOUNDARY_INVALID_DAMAGE_OCCURED_DATE],
    "damageType" : [
        DAMAGE_VALID_DAMAGE_TYPE,
        DAMAGE_INVALID_DAMAGE_TYPE,
        DAMAGE_BOUNDARY_VALID_DAMAGE_TYPE,
        DAMAGE_BOUNDARY_INVALID_DAMAGE_TYPE],
    "damageSeverity" : [
        DAMAGE_VALID_DAMAGE_SEVERITY,
        DAMAGE_INVALID_DAMAGE_SEVERITY,
        DAMAGE_BOUNDARY_VALID_DAMAGE_SEVERITY,
        DAMAGE_BOUNDARY_INVALID_DAMAGE_SEVERITY],
    "notes" : [
        DAMAGE_VALID_NOTES,
        DAMAGE_INVALID_NOTES,
        DAMAGE_BOUNDARY_VALID_NOTES,
        DAMAGE_BOUNDARY_INVALID_NOTES],
    "damageImage" : [
        DAMAGE_VALID_DAMAGE_IMAGE,
        DAMAGE_INVALID_DAMAGE_IMAGE,
        DAMAGE_BOUNDARY_VALID_DAMAGE_IMAGE,
        DAMAGE_BOUNDARY_INVALID_DAMAGE_IMAGE],
    "scheduledMaintenanceDate" : [
        DAMAGE_VALID_SCHEDULED_MAINTENANCE_DATE,
        DAMAGE_INVALID_SCHEDULED_MAINTENANCE_DATE,
        DAMAGE_BOUNDARY_VALID_SCHEDULED_MAINTENANCE_DATE,
        DAMAGE_BOUNDARY_INVALID_SCHEDULED_MAINTENANCE_DATE],
    "deleted" : [
        DAMAGE_VALID_DELETED,
        DAMAGE_INVALID_DELETED,
        DAMAGE_BOUNDARY_VALID_DELETED,
        DAMAGE_BOUNDARY_INVALID_DELETED]
}

# Valid cases for assetID
MAINTENANCE_VALID_ASSET_ID = [
    1, # Assuming 1 is a valid asset ID
    2, # Assuming 2 is a valid asset ID
    3, # Assuming 3 is a valid asset ID
    4, # Assuming 4 is a valid asset ID
    5, # Assuming 5 is a valid asset ID
]

# Invalid cases for assetID
MAINTENANCE_INVALID_ASSET_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for assetID
MAINTENANCE_BOUNDARY_VALID_ASSET_ID = [
    1, # Assuming 1 is a valid asset ID
]

# Boundary invalid cases for assetID
MAINTENANCE_BOUNDARY_INVALID_ASSET_ID = [
    None, # None value
]

# Valid cases for completionDate
MAINTENANCE_VALID_COMPLETION_DATE = [
    "2023-01-01", # Valid date
    "2022-12-31", # Valid date
    "2021-06-15", # Valid date
    "2020-02-29", # Leap year date
    "2019-07-04", # Valid date
]

# Invalid cases for completionDate
MAINTENANCE_INVALID_COMPLETION_DATE = [
    None, # None value
    "", # Empty string
    "invalid-date", # Invalid date format
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
]

# Boundary valid cases for completionDate
MAINTENANCE_BOUNDARY_VALID_COMPLETION_DATE = [
    "0001-01-01", # Minimum valid date
    "9999-12-31", # Maximum valid date
]

# Boundary invalid cases for completionDate
MAINTENANCE_BOUNDARY_INVALID_COMPLETION_DATE = [
    None, # None value
    "0000-00-00", # Invalid date
]

# Valid cases for maintenanceType
MAINTENANCE_VALID_maintenance_TYPE = [
    0, # Assuming 0 is a valid choice
    1, # Assuming 1 is a valid choice
    2, # Assuming 2 is a valid choice
    3, # Assuming 3 is a valid choice
    4, # Assuming 4 is a valid choice
]

# Invalid cases for maintenanceType
MAINTENANCE_INVALID_maintenance_TYPE = [
    None, # None value
    -1, # Negative value
    5, # Assuming 5 is not a valid choice
    "invalid", # Non-integer value
]

# Boundary valid cases for maintenanceType
MAINTENANCE_BOUNDARY_VALID_maintenance_TYPE = [
    0, # Minimum valid choice
    4, # Maximum valid choice
]

# Boundary invalid cases for maintenanceType
MAINTENANCE_BOUNDARY_INVALID_maintenance_TYPE = [
    -1, # Negative value
    5, # Exceeds maximum valid choice
]

# Valid cases for maintenanceConductedBy
MAINTENANCE_VALID_MAINTENANCE_CONDUCTED_BY = [
    1, # Assuming 1 is a valid UserProfile ID
    2, # Assuming 2 is a valid UserProfile ID
    3, # Assuming 3 is a valid UserProfile ID
    4, # Assuming 4 is a valid UserProfile ID
    5, # Assuming 5 is a valid UserProfile ID
]

# Invalid cases for maintenanceConductedBy
MAINTENANCE_INVALID_MAINTENANCE_CONDUCTED_BY = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for maintenanceConductedBy
MAINTENANCE_BOUNDARY_VALID_MAINTENANCE_CONDUCTED_BY = [
    1, # Assuming 1 is a valid UserProfile ID
]

# Boundary invalid cases for maintenanceConductedBy
MAINTENANCE_BOUNDARY_INVALID_MAINTENANCE_CONDUCTED_BY = [
    None, # None value
]

# Valid cases for maintenanceLocation
MAINTENANCE_VALID_MAINTENANCE_LOCATION = [
    "Warehouse A", # Valid location
    "Site B", # Valid location
    "Garage C", # Valid location
    "Facility D", # Valid location
    "Workshop E", # Valid location
]

# Invalid cases for maintenanceLocation
MAINTENANCE_INVALID_MAINTENANCE_LOCATION = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for maintenanceLocation
MAINTENANCE_BOUNDARY_VALID_MAINTENANCE_LOCATION = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for maintenanceLocation
MAINTENANCE_BOUNDARY_INVALID_MAINTENANCE_LOCATION = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

# Valid cases for maintenanceTasksCompleted
MAINTENANCE_VALID_MAINTENANCE_TASKS_COMPLETED = [
    "Oil change", # Valid task
    "Filter replacement", # Valid task
    "Brake inspection", # Valid task
    "Tire rotation", # Valid task
    "Battery check", # Valid task
]

# Invalid cases for maintenanceTasksCompleted
MAINTENANCE_INVALID_MAINTENANCE_TASKS_COMPLETED = [
    None, # None value
    "", # Empty string
    "A" * 256, # Exceeds maximum length
]

# Boundary valid cases for maintenanceTasksCompleted
MAINTENANCE_BOUNDARY_VALID_MAINTENANCE_TASKS_COMPLETED = [
    "A", # Exactly 1 character
    "B" * 255, # Exactly 255 characters
]

# Boundary invalid cases for maintenanceTasksCompleted
MAINTENANCE_BOUNDARY_INVALID_MAINTENANCE_TASKS_COMPLETED = [
    "", # Empty string
    "C" * 256, # Exceeds maximum length
]

# Valid cases for repairsCompleted
MAINTENANCE_VALID_REPAIRS_COMPLETED = [
    1, # Assuming 1 is a valid Damage ID
    2, # Assuming 2 is a valid Damage ID
    3, # Assuming 3 is a valid Damage ID
    4, # Assuming 4 is a valid Damage ID
    5, # Assuming 5 is a valid Damage ID
]

# Invalid cases for repairsCompleted
MAINTENANCE_INVALID_REPAIRS_COMPLETED = [
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for repairsCompleted
MAINTENANCE_BOUNDARY_VALID_REPAIRS_COMPLETED = [
    1, # Assuming 1 is a valid Damage ID
]

# Boundary invalid cases for repairsCompleted
MAINTENANCE_BOUNDARY_INVALID_REPAIRS_COMPLETED = [
    None, # None value
]

# Valid cases for Cost
MAINTENANCE_VALID_COST = [
    0.00, # Minimum valid cost
    100.00, # Typical valid cost
    9999999.99, # Maximum valid cost
    1234.56, # Valid cost with decimal places
    98765.43, # Valid cost with decimal places
]

# Invalid cases for Cost
MAINTENANCE_INVALID_COST = [
    None, # None value
    -1.00, # Negative value
    "invalid", # Non-decimal value
    10000000.00, # Exceeds maximum digits
]

# Boundary valid cases for Cost
MAINTENANCE_BOUNDARY_VALID_COST = [
    0.00, # Minimum valid cost
    9999999.99, # Maximum valid cost
]

# Boundary invalid cases for Cost
MAINTENANCE_BOUNDARY_INVALID_COST = [
    None, # None value
    -0.01, # Negative value
    10000000.00, # Exceeds maximum digits
]

# Valid cases for Notes
MAINTENANCE_VALID_NOTES = [
    "Routine maintenance completed.", # Valid note
    "Replaced worn-out parts.", # Valid note
    "Checked all systems.", # Valid note
    "Performed safety inspection.", # Valid note
    "No issues found.", # Valid note
]

# Invalid cases for Notes
MAINTENANCE_INVALID_NOTES = [
    None, # None value
    "", # Empty string
    "A" * 256, # Exceeds maximum length
]

# Boundary valid cases for Notes
MAINTENANCE_BOUNDARY_VALID_NOTES = [
    "A", # Exactly 1 character
    "B" * 255, # Exactly 255 characters
]

# Boundary invalid cases for Notes
MAINTENANCE_BOUNDARY_INVALID_NOTES = [
    "", # Empty string
    "C" * 256, # Exceeds maximum length
]

# Valid cases for kmsBeforeNextService
MAINTENANCE_VALID_KMS_BEFORE_NEXT_SERVICE = [
    0, # Minimum valid value
    1000, # Typical valid value
    5000, # Typical valid value
    10000, # Typical valid value
    20000, # Typical valid value
]

# Invalid cases for kmsBeforeNextService
MAINTENANCE_INVALID_KMS_BEFORE_NEXT_SERVICE = [
    None, # None value
    -1, # Negative value
    "invalid", # Non-integer value
]

# Boundary valid cases for kmsBeforeNextService
MAINTENANCE_BOUNDARY_VALID_KMS_BEFORE_NEXT_SERVICE = [
    0, # Minimum valid value
]

# Boundary invalid cases for kmsBeforeNextService
MAINTENANCE_BOUNDARY_INVALID_KMS_BEFORE_NEXT_SERVICE = [
    None, # None value
    -1, # Negative value
]

# Valid cases for dateOfNextService
MAINTENANCE_VALID_DATE_OF_NEXT_SERVICE = [
    "2023-01-01", # Valid date
    "2022-12-31", # Valid date
    "2021-06-15", # Valid date
    "2020-02-29", # Leap year date
    "2019-07-04", # Valid date
]

# Invalid cases for dateOfNextService
MAINTENANCE_INVALID_DATE_OF_NEXT_SERVICE = [
    None, # None value
    "", # Empty string
    "invalid-date", # Invalid date format
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
]

# Boundary valid cases for dateOfNextService
MAINTENANCE_BOUNDARY_VALID_DATE_OF_NEXT_SERVICE = [
    "0001-01-01", # Minimum valid date
    "9999-12-31", # Maximum valid date
]

# Boundary invalid cases for dateOfNextService
MAINTENANCE_BOUNDARY_INVALID_DATE_OF_NEXT_SERVICE = [
    None, # None value
    "0000-00-00", # Invalid date
]

# Valid cases for deleted
MAINTENANCE_VALID_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for deleted
MAINTENANCE_INVALID_DELETED = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for deleted
MAINTENANCE_BOUNDARY_VALID_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for deleted
MAINTENANCE_BOUNDARY_INVALID_DELETED = [
    None, # None value
]

MAINTENANCE_SUPERSET = {
    "assetID" : [
        MAINTENANCE_VALID_ASSET_ID,
        MAINTENANCE_INVALID_ASSET_ID,
        MAINTENANCE_BOUNDARY_VALID_ASSET_ID,
        MAINTENANCE_BOUNDARY_INVALID_ASSET_ID],
    "completionDate" : [
        MAINTENANCE_VALID_COMPLETION_DATE,
        MAINTENANCE_INVALID_COMPLETION_DATE,
        MAINTENANCE_BOUNDARY_VALID_COMPLETION_DATE,
        MAINTENANCE_BOUNDARY_INVALID_COMPLETION_DATE],
    "maintenanceType" : [
        MAINTENANCE_VALID_maintenance_TYPE,
        MAINTENANCE_INVALID_maintenance_TYPE,
        MAINTENANCE_BOUNDARY_VALID_maintenance_TYPE,
        MAINTENANCE_BOUNDARY_INVALID_maintenance_TYPE],
    "maintenanceConductedBy" : [
        MAINTENANCE_VALID_MAINTENANCE_CONDUCTED_BY,
        MAINTENANCE_INVALID_MAINTENANCE_CONDUCTED_BY,
        MAINTENANCE_BOUNDARY_VALID_MAINTENANCE_CONDUCTED_BY,
        MAINTENANCE_BOUNDARY_INVALID_MAINTENANCE_CONDUCTED_BY],
    "maintenanceLocation" : [
        MAINTENANCE_VALID_MAINTENANCE_LOCATION,
        MAINTENANCE_INVALID_MAINTENANCE_LOCATION,
        MAINTENANCE_BOUNDARY_VALID_MAINTENANCE_LOCATION,
        MAINTENANCE_BOUNDARY_INVALID_MAINTENANCE_LOCATION],
    "maintenanceTasksCompleted" : [
        MAINTENANCE_VALID_MAINTENANCE_TASKS_COMPLETED,
        MAINTENANCE_INVALID_MAINTENANCE_TASKS_COMPLETED,
        MAINTENANCE_BOUNDARY_VALID_MAINTENANCE_TASKS_COMPLETED,
        MAINTENANCE_BOUNDARY_INVALID_MAINTENANCE_TASKS_COMPLETED],
    "repairsCompleted" : [
        MAINTENANCE_VALID_REPAIRS_COMPLETED,
        MAINTENANCE_INVALID_REPAIRS_COMPLETED,
        MAINTENANCE_BOUNDARY_VALID_REPAIRS_COMPLETED,
        MAINTENANCE_BOUNDARY_INVALID_REPAIRS_COMPLETED],
    "cost" : [
        MAINTENANCE_VALID_COST,
        MAINTENANCE_INVALID_COST,
        MAINTENANCE_BOUNDARY_VALID_COST,
        MAINTENANCE_BOUNDARY_INVALID_COST],
    "notes" : [
        MAINTENANCE_VALID_NOTES,
        MAINTENANCE_INVALID_NOTES,
        MAINTENANCE_BOUNDARY_VALID_NOTES,
        MAINTENANCE_BOUNDARY_INVALID_NOTES],
    "kmsBeforeNextService" : [
        MAINTENANCE_VALID_KMS_BEFORE_NEXT_SERVICE,
        MAINTENANCE_INVALID_KMS_BEFORE_NEXT_SERVICE,
        MAINTENANCE_BOUNDARY_VALID_KMS_BEFORE_NEXT_SERVICE,
        MAINTENANCE_BOUNDARY_INVALID_KMS_BEFORE_NEXT_SERVICE],
    "dateOfNextService" : [
        MAINTENANCE_VALID_DATE_OF_NEXT_SERVICE,
        MAINTENANCE_INVALID_DATE_OF_NEXT_SERVICE,
        MAINTENANCE_BOUNDARY_VALID_DATE_OF_NEXT_SERVICE,
        MAINTENANCE_BOUNDARY_INVALID_DATE_OF_NEXT_SERVICE],
    "deleted" : [
        MAINTENANCE_VALID_DELETED,
        MAINTENANCE_INVALID_DELETED,
        MAINTENANCE_BOUNDARY_VALID_DELETED,
        MAINTENANCE_BOUNDARY_INVALID_DELETED]
}


# Valid cases for assetID
EXPENSE_VALID_ASSET_ID = [
    1, # Assuming 1 is a valid asset ID
    2, # Assuming 2 is a valid asset ID
    3, # Assuming 3 is a valid asset ID
    4, # Assuming 4 is a valid asset ID
    5, # Assuming 5 is a valid asset ID
]

# Invalid cases for assetID
EXPENSE_INVALID_ASSET_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for assetID
EXPENSE_BOUNDARY_VALID_ASSET_ID = [
    1, # Assuming 1 is a valid asset ID
]

# Boundary invalid cases for assetID
EXPENSE_BOUNDARY_INVALID_ASSET_ID = [
    None, # None value
]

# Valid cases for expenseType
EXPENSE_VALID_EXPENSE_TYPE = [
    0, # Assuming 0 is a valid choice
    1, # Assuming 1 is a valid choice
    2, # Assuming 2 is a valid choice
    3, # Assuming 3 is a valid choice
    4, # Assuming 4 is a valid choice
]

# Invalid cases for expenseType
EXPENSE_INVALID_EXPENSE_TYPE = [
    None, # None value
    -1, # Negative value
    5, # Assuming 5 is not a valid choice
    "invalid", # Non-integer value
]

# Boundary valid cases for expenseType
EXPENSE_BOUNDARY_VALID_EXPENSE_TYPE = [
    0, # Minimum valid choice
    4, # Maximum valid choice
]

# Boundary invalid cases for expenseType
EXPENSE_BOUNDARY_INVALID_EXPENSE_TYPE = [
    -1, # Negative value
    5, # Exceeds maximum valid choice
]

# Valid cases for MaintenanceID
EXPENSE_VALID_MAINTENANCE_ID = [
    1, # Assuming 1 is a valid Maintenance ID
    2, # Assuming 2 is a valid Maintenance ID
    3, # Assuming 3 is a valid Maintenance ID
    4, # Assuming 4 is a valid Maintenance ID
    5, # Assuming 5 is a valid Maintenance ID
]

# Invalid cases for MaintenanceID
EXPENSE_INVALID_MAINTENANCE_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for MaintenanceID
EXPENSE_BOUNDARY_VALID_MAINTENANCE_ID = [
    1, # Assuming 1 is a valid Maintenance ID
]

# Boundary invalid cases for MaintenanceID
EXPENSE_BOUNDARY_INVALID_MAINTENANCE_ID = [
    None, # None value
]

# Valid cases for cost
EXPENSE_VALID_COST = [
    0.00, # Minimum valid cost
    100.00, # Typical valid cost
    9999999.99, # Maximum valid cost
    1234.56, # Valid cost with decimal places
    98765.43, # Valid cost with decimal places
]

# Invalid cases for cost
EXPENSE_INVALID_COST = [
    None, # None value
    -1.00, # Negative value
    "invalid", # Non-decimal value
    10000000.00, # Exceeds maximum digits
]

# Boundary valid cases for cost
EXPENSE_BOUNDARY_VALID_COST = [
    0.00, # Minimum valid cost
    9999999.99, # Maximum valid cost
]

# Boundary invalid cases for cost
EXPENSE_BOUNDARY_INVALID_COST = [
    None, # None value
    -0.01, # Negative value
    10000000.00, # Exceeds maximum digits
]

# Valid cases for receiptNumber
EXPENSE_VALID_RECEIPT_NUMBER = [
    1, # Minimum valid value
    100, # Typical valid value
    999999, # Large valid value
    123456, # Typical valid value
    987654, # Typical valid value
]

# Invalid cases for receiptNumber
EXPENSE_INVALID_RECEIPT_NUMBER = [
    None, # None value
    -1, # Negative value
    "invalid", # Non-integer value
]

# Boundary valid cases for receiptNumber
EXPENSE_BOUNDARY_VALID_RECEIPT_NUMBER = [
    1, # Minimum valid value
]

# Boundary invalid cases for receiptNumber
EXPENSE_BOUNDARY_INVALID_RECEIPT_NUMBER = [
    None, # None value
    0, # Zero value
]

# Valid cases for expenseLodgedBy
EXPENSE_VALID_EXPENSE_LODGED_BY = [
    1, # Assuming 1 is a valid UserProfile ID
    2, # Assuming 2 is a valid UserProfile ID
    3, # Assuming 3 is a valid UserProfile ID
    4, # Assuming 4 is a valid UserProfile ID
    5, # Assuming 5 is a valid UserProfile ID
]

# Invalid cases for expenseLodgedBy
EXPENSE_INVALID_EXPENSE_LODGED_BY = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for expenseLodgedBy
EXPENSE_BOUNDARY_VALID_EXPENSE_LODGED_BY = [
    1, # Assuming 1 is a valid UserProfile ID
]

# Boundary invalid cases for expenseLodgedBy
EXPENSE_BOUNDARY_INVALID_EXPENSE_LODGED_BY = [
    None, # None value
]

# Valid cases for deleted
EXPENSE_VALID_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for deleted
EXPENSE_INVALID_DELETED = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for deleted
EXPENSE_BOUNDARY_VALID_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for deleted
EXPENSE_BOUNDARY_INVALID_DELETED = [
    None, # None value
]

EXPENSE_SUPERSET = {
    "assetID" : [
        EXPENSE_VALID_ASSET_ID,
        EXPENSE_INVALID_ASSET_ID,
        EXPENSE_BOUNDARY_VALID_ASSET_ID,
        EXPENSE_BOUNDARY_INVALID_ASSET_ID],
    "expenseType" : [
        EXPENSE_VALID_EXPENSE_TYPE,
        EXPENSE_INVALID_EXPENSE_TYPE,
        EXPENSE_BOUNDARY_VALID_EXPENSE_TYPE,
        EXPENSE_BOUNDARY_INVALID_EXPENSE_TYPE],
    "maintenanceID" : [
        EXPENSE_VALID_MAINTENANCE_ID,
        EXPENSE_INVALID_MAINTENANCE_ID,
        EXPENSE_BOUNDARY_VALID_MAINTENANCE_ID,
        EXPENSE_BOUNDARY_INVALID_MAINTENANCE_ID],
    "cost" : [
        EXPENSE_VALID_COST,
        EXPENSE_INVALID_COST,
        EXPENSE_BOUNDARY_VALID_COST,
        EXPENSE_BOUNDARY_INVALID_COST],
    "receiptNumber" : [
        EXPENSE_VALID_RECEIPT_NUMBER,
        EXPENSE_INVALID_RECEIPT_NUMBER,
        EXPENSE_BOUNDARY_VALID_RECEIPT_NUMBER,
        EXPENSE_BOUNDARY_INVALID_RECEIPT_NUMBER],
    "expenseLodgedBy" : [
        EXPENSE_VALID_EXPENSE_LODGED_BY,
        EXPENSE_INVALID_EXPENSE_LODGED_BY,
        EXPENSE_BOUNDARY_VALID_EXPENSE_LODGED_BY,
        EXPENSE_BOUNDARY_INVALID_EXPENSE_LODGED_BY],
    "deleted" : [
        EXPENSE_VALID_DELETED,
        EXPENSE_INVALID_DELETED,
        EXPENSE_BOUNDARY_VALID_DELETED,
        EXPENSE_BOUNDARY_INVALID_DELETED]
}

# Valid cases for timezone
ORG_SETTINGS_VALID_TIMEZONE = [
    "UTC", # Valid timezone
    "America/New_York", # Valid timezone
    "Europe/London", # Valid timezone
    "Asia/Tokyo", # Valid timezone
    "Australia/Sydney", # Valid timezone
]

# Invalid cases for timezone
ORG_SETTINGS_INVALID_TIMEZONE = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for timezone
ORG_SETTINGS_BOUNDARY_VALID_TIMEZONE = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for timezone
ORG_SETTINGS_BOUNDARY_INVALID_TIMEZONE = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

# Valid cases for datetime_format
ORG_SETTINGS_VALID_DATETIME_FORMAT = [
    "%Y-%m-%d %H:%M:%S", # Valid datetime format
    "%d/%m/%Y %I:%M %p", # Valid datetime format
    "%m-%d-%Y %H:%M", # Valid datetime format
    "%Y.%m.%d %H:%M:%S", # Valid datetime format
    "%d-%b-%Y %H:%M", # Valid datetime format
]

# Invalid cases for datetime_format
ORG_SETTINGS_INVALID_DATETIME_FORMAT = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for datetime_format
ORG_SETTINGS_BOUNDARY_VALID_DATETIME_FORMAT = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for datetime_format
ORG_SETTINGS_BOUNDARY_INVALID_DATETIME_FORMAT = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

# Valid cases for temperature_label
ORG_SETTINGS_VALID_TEMPERATURE_LABEL = [
    "Celsius", # Valid temperature label
    "Fahrenheit", # Valid temperature label
    "Kelvin", # Valid temperature label
    "Rankine", # Valid temperature label
    "Reaumur", # Valid temperature label
]

# Invalid cases for temperature_label
ORG_SETTINGS_INVALID_TEMPERATURE_LABEL = [
    None, # None value
    "", # Empty string
    "A" * 51, # Exceeds maximum length
]

# Boundary valid cases for temperature_label
ORG_SETTINGS_BOUNDARY_VALID_TEMPERATURE_LABEL = [
    "A", # Exactly 1 character
    "B" * 50, # Exactly 50 characters
]

# Boundary invalid cases for temperature_label
ORG_SETTINGS_BOUNDARY_INVALID_TEMPERATURE_LABEL = [
    "", # Empty string
    "C" * 51, # Exceeds maximum length
]

# Valid cases for mass_label
ORG_SETTINGS_VALID_MASS_LABEL = [
    "Kilogram", # Valid mass label
    "Gram", # Valid mass label
    "Pound", # Valid mass label
    "Ounce", # Valid mass label
    "Ton", # Valid mass label
]

# Invalid cases for mass_label
ORG_SETTINGS_INVALID_MASS_LABEL = [
    None, # None value
    "", # Empty string
    "A" * 51, # Exceeds maximum length
]

# Boundary valid cases for mass_label
ORG_SETTINGS_BOUNDARY_VALID_MASS_LABEL = [
    "A", # Exactly 1 character
    "B" * 50, # Exactly 50 characters
]

# Boundary invalid cases for mass_label
ORG_SETTINGS_BOUNDARY_INVALID_MASS_LABEL = [
    "", # Empty string
    "C" * 51, # Exceeds maximum length
]

# Valid cases for area_label
ORG_SETTINGS_VALID_AREA_LABEL = [
    "Square Meter", # Valid area label
    "Square Kilometer", # Valid area label
    "Acre", # Valid area label
    "Hectare", # Valid area label
    "Square Mile", # Valid area label
]

# Invalid cases for area_label
ORG_SETTINGS_INVALID_AREA_LABEL = [
    None, # None value
    "", # Empty string
    "A" * 51, # Exceeds maximum length
]

# Boundary valid cases for area_label
ORG_SETTINGS_BOUNDARY_VALID_AREA_LABEL = [
    "A", # Exactly 1 character
    "B" * 50, # Exactly 50 characters
]

# Boundary invalid cases for area_label
ORG_SETTINGS_BOUNDARY_INVALID_AREA_LABEL = [
    "", # Empty string
    "C" * 51, # Exceeds maximum length
]

# Valid cases for length_label
ORG_SETTINGS_VALID_LENGTH_LABEL = [
    "Meter", # Valid length label
    "Kilometer", # Valid length label
    "Centimeter", # Valid length label
    "Millimeter", # Valid length label
    "Inch", # Valid length label
]

# Invalid cases for length_label
ORG_SETTINGS_INVALID_LENGTH_LABEL = [
    None, # None value
    "", # Empty string
    "A" * 51, # Exceeds maximum length
]

# Boundary valid cases for length_label
ORG_SETTINGS_BOUNDARY_VALID_LENGTH_LABEL = [
    "A", # Exactly 1 character
    "B" * 50, # Exactly 50 characters
]

# Boundary invalid cases for length_label
ORG_SETTINGS_BOUNDARY_INVALID_LENGTH_LABEL = [
    "", # Empty string
    "C" * 51, # Exceeds maximum length
]

ORG_SETTINGS_SUPERSET = {
    "timezone" : [
        ORG_SETTINGS_VALID_TIMEZONE,
        ORG_SETTINGS_INVALID_TIMEZONE,
        ORG_SETTINGS_BOUNDARY_VALID_TIMEZONE,
        ORG_SETTINGS_BOUNDARY_INVALID_TIMEZONE],
    "datetime_format" : [
        ORG_SETTINGS_VALID_DATETIME_FORMAT,
        ORG_SETTINGS_INVALID_DATETIME_FORMAT,
        ORG_SETTINGS_BOUNDARY_VALID_DATETIME_FORMAT,
        ORG_SETTINGS_BOUNDARY_INVALID_DATETIME_FORMAT],
    "temperature_label" : [
        ORG_SETTINGS_VALID_TEMPERATURE_LABEL,
        ORG_SETTINGS_INVALID_TEMPERATURE_LABEL,
        ORG_SETTINGS_BOUNDARY_VALID_TEMPERATURE_LABEL,
        ORG_SETTINGS_BOUNDARY_INVALID_TEMPERATURE_LABEL],
    "mass_label" : [
        ORG_SETTINGS_VALID_MASS_LABEL,
        ORG_SETTINGS_INVALID_MASS_LABEL,
        ORG_SETTINGS_BOUNDARY_VALID_MASS_LABEL,
        ORG_SETTINGS_BOUNDARY_INVALID_MASS_LABEL],
    "area_label" : [
        ORG_SETTINGS_VALID_AREA_LABEL,
        ORG_SETTINGS_INVALID_AREA_LABEL,
        ORG_SETTINGS_BOUNDARY_VALID_AREA_LABEL,
        ORG_SETTINGS_BOUNDARY_INVALID_AREA_LABEL],
    "length_label" : [
        ORG_SETTINGS_VALID_LENGTH_LABEL,
        ORG_SETTINGS_INVALID_LENGTH_LABEL,
        ORG_SETTINGS_BOUNDARY_VALID_LENGTH_LABEL,
        ORG_SETTINGS_BOUNDARY_INVALID_LENGTH_LABEL]
}

# Valid cases for teamName
INTERNAL_TEAMS_MODEL_VALID_TEAM_NAME = [
    "Team Alpha", # Valid team name
    "Beta Squad", # Valid team name
    "Gamma Group", # Valid team name
    "Delta Force", # Valid team name
    "Epsilon Unit", # Valid team name
]

# Invalid cases for teamName
INTERNAL_TEAMS_MODEL_INVALID_TEAM_NAME = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for teamName
INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_TEAM_NAME = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for teamName
INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_TEAM_NAME = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

# Valid cases for teamDescription
INTERNAL_TEAMS_MODEL_VALID_TEAM_DESCRIPTION = [
    "This is a team responsible for crop management.", # Valid description
    "Handles livestock and dairy production.", # Valid description
    "Oversees equipment maintenance and repair.", # Valid description
    "Manages financial records and budgeting.", # Valid description
    "Coordinates with external suppliers and vendors.", # Valid description
]

# Invalid cases for teamDescription
INTERNAL_TEAMS_MODEL_INVALID_TEAM_DESCRIPTION = [
    None, # None value
    "", # Empty string
    "A" * 1001, # Exceeds maximum length
]

# Boundary valid cases for teamDescription
INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_TEAM_DESCRIPTION = [
    "A", # Exactly 1 character
    "B" * 1000, # Exactly 1000 characters
]

# Boundary invalid cases for teamDescription
INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_TEAM_DESCRIPTION = [
    "", # Empty string
    "C" * 1001, # Exceeds maximum length
]

# Valid cases for active
INTERNAL_TEAMS_MODEL_VALID_ACTIVE = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for active
INTERNAL_TEAMS_MODEL_INVALID_ACTIVE = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for active
INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_ACTIVE = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for active
INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_ACTIVE = [
    None, # None value
]

# Valid cases for teamImage
INTERNAL_TEAMS_MODEL_VALID_TEAM_IMAGE = [
    "images/internalTeams/team1.jpg", # Valid image path
    "images/internalTeams/team2.png", # Valid image path
    "images/internalTeams/team3.gif", # Valid image path
    "images/internalTeams/team4.bmp", # Valid image path
    "images/internalTeams/team5.jpeg", # Valid image path
]

# Invalid cases for teamImage
INTERNAL_TEAMS_MODEL_INVALID_TEAM_IMAGE = [
    None, # None value
    "", # Empty string
    "invalid_path", # Invalid path
]

# Boundary valid cases for teamImage
INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_TEAM_IMAGE = [
    "images/internalTeams/default.jpg", # Default image path
]

# Boundary invalid cases for teamImage
INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_TEAM_IMAGE = [
    "", # Empty string
]

# Valid cases for farm
INTERNAL_TEAMS_MODEL_VALID_FARM = [
    1, # Assuming 1 is a valid FarmInfo ID
    2, # Assuming 2 is a valid FarmInfo ID
    3, # Assuming 3 is a valid FarmInfo ID
    4, # Assuming 4 is a valid FarmInfo ID
    5, # Assuming 5 is a valid FarmInfo ID
]

# Invalid cases for farm
INTERNAL_TEAMS_MODEL_INVALID_FARM = [
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for farm
INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_FARM = [
    1, # Assuming 1 is a valid FarmInfo ID
]

# Boundary invalid cases for farm
INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_FARM = [
    None, # None value
]

INTERNAL_TEAMS_MODEL_SUPERSET = {
    "teamName" : [
        INTERNAL_TEAMS_MODEL_VALID_TEAM_NAME,
        INTERNAL_TEAMS_MODEL_INVALID_TEAM_NAME,
        INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_TEAM_NAME,
        INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_TEAM_NAME],
    "teamDescription" : [
        INTERNAL_TEAMS_MODEL_VALID_TEAM_DESCRIPTION,
        INTERNAL_TEAMS_MODEL_INVALID_TEAM_DESCRIPTION,
        INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_TEAM_DESCRIPTION,
        INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_TEAM_DESCRIPTION],
    "active" : [
        INTERNAL_TEAMS_MODEL_VALID_ACTIVE,
        INTERNAL_TEAMS_MODEL_INVALID_ACTIVE,
        INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_ACTIVE,
        INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_ACTIVE],
    "teamImage" : [
        INTERNAL_TEAMS_MODEL_VALID_TEAM_IMAGE,
        INTERNAL_TEAMS_MODEL_INVALID_TEAM_IMAGE,
        INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_TEAM_IMAGE,
        INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_TEAM_IMAGE],
    "farm" : [
        INTERNAL_TEAMS_MODEL_VALID_FARM,
        INTERNAL_TEAMS_MODEL_INVALID_FARM,
        INTERNAL_TEAMS_MODEL_BOUNDARY_VALID_FARM,
        INTERNAL_TEAMS_MODEL_BOUNDARY_INVALID_FARM]
}

# Valid cases for code
LINKING_CODE_VALID_CODE = [
    "ABC123", # Valid code
    "XYZ789", # Valid code
    "LINK001", # Valid code
    "CODE999", # Valid code
    "UNIQUE456", # Valid code
]

# Invalid cases for code
LINKING_CODE_INVALID_CODE = [
    None, # None value
    "", # Empty string
    "A" * 256, # Exceeds typical length for a code
]

# Boundary valid cases for code
LINKING_CODE_BOUNDARY_VALID_CODE = [
    "A", # Exactly 1 character
    "B" * 255, # Exactly 255 characters
]

# Boundary invalid cases for code
LINKING_CODE_BOUNDARY_INVALID_CODE = [
    "", # Empty string
    "C" * 256, # Exceeds typical length for a code
]

# Valid cases for farm
LINKING_CODE_VALID_FARM = [
    1, # Assuming 1 is a valid FarmInfo ID
    2, # Assuming 2 is a valid FarmInfo ID
    3, # Assuming 3 is a valid FarmInfo ID
    4, # Assuming 4 is a valid FarmInfo ID
    5, # Assuming 5 is a valid FarmInfo ID
]

# Invalid cases for farm
LINKING_CODE_INVALID_FARM = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for farm
LINKING_CODE_BOUNDARY_VALID_FARM = [
    1, # Assuming 1 is a valid FarmInfo ID
]

# Boundary invalid cases for farm
LINKING_CODE_BOUNDARY_INVALID_FARM = [
    None, # None value
]

# Valid cases for created_at
LINKING_CODE_VALID_CREATED_AT = [
    "2023-01-01T00:00:00Z", # Valid datetime
    "2023-06-15T12:30:45Z", # Valid datetime
    "2022-12-31T23:59:59Z", # Valid datetime
    "2021-07-20T08:15:30Z", # Valid datetime
    "2020-02-29T00:00:00Z", # Valid datetime (leap year)
]

# Invalid cases for created_at
LINKING_CODE_INVALID_CREATED_AT = [
    None, # None value
    "invalid", # Non-datetime value
    "2023-13-01T00:00:00Z", # Invalid month
    "2023-00-01T00:00:00Z", # Invalid month
    "2023-01-32T00:00:00Z", # Invalid day
]

# Boundary valid cases for created_at
LINKING_CODE_BOUNDARY_VALID_CREATED_AT = [
    "2023-01-01T00:00:00Z", # Valid datetime
]

# Boundary invalid cases for created_at
LINKING_CODE_BOUNDARY_INVALID_CREATED_AT = [
    None, # None value
]

# Valid cases for expires_at
LINKING_CODE_VALID_EXPIRES_AT = [
    "2023-12-31T23:59:59Z", # Valid datetime
    "2024-06-15T12:30:45Z", # Valid datetime
    "2025-01-01T00:00:00Z", # Valid datetime
    "2026-07-20T08:15:30Z", # Valid datetime
    "2027-02-28T00:00:00Z", # Valid datetime
]

# Invalid cases for expires_at
LINKING_CODE_INVALID_EXPIRES_AT = [
    None, # None value
    "invalid", # Non-datetime value
    "2023-13-01T00:00:00Z", # Invalid month
    "2023-00-01T00:00:00Z", # Invalid month
    "2023-01-32T00:00:00Z", # Invalid day
]

# Boundary valid cases for expires_at
LINKING_CODE_BOUNDARY_VALID_EXPIRES_AT = [
    "2023-12-31T23:59:59Z", # Valid datetime
]

# Boundary invalid cases for expires_at
LINKING_CODE_BOUNDARY_INVALID_EXPIRES_AT = [
    None, # None value
]

LINKING_CODE_SUPERSET = {
    "code" : [
        LINKING_CODE_VALID_CODE,
        LINKING_CODE_INVALID_CODE,
        LINKING_CODE_BOUNDARY_VALID_CODE,
        LINKING_CODE_BOUNDARY_INVALID_CODE],
    "farm" : [
        LINKING_CODE_VALID_FARM,
        LINKING_CODE_INVALID_FARM,
        LINKING_CODE_BOUNDARY_VALID_FARM,
        LINKING_CODE_BOUNDARY_INVALID_FARM],
    "created_at" : [
        LINKING_CODE_VALID_CREATED_AT,
        LINKING_CODE_INVALID_CREATED_AT,
        LINKING_CODE_BOUNDARY_VALID_CREATED_AT,
        LINKING_CODE_BOUNDARY_INVALID_CREATED_AT],
    "expires_at" : [
        LINKING_CODE_VALID_EXPIRES_AT,
        LINKING_CODE_INVALID_EXPIRES_AT,
        LINKING_CODE_BOUNDARY_VALID_EXPIRES_AT,
        LINKING_CODE_BOUNDARY_INVALID_EXPIRES_AT]
}

# Valid cases for farmID
TASK_VALID_FARM_ID = [
    1, # Assuming 1 is a valid FarmInfo ID
    2, # Assuming 2 is a valid FarmInfo ID
    3, # Assuming 3 is a valid FarmInfo ID
    4, # Assuming 4 is a valid FarmInfo ID
    5, # Assuming 5 is a valid FarmInfo ID
]

# Invalid cases for farmID
TASK_INVALID_FARM_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for farmID
TASK_BOUNDARY_VALID_FARM_ID = [
    1, # Assuming 1 is a valid FarmInfo ID
]

# Boundary invalid cases for farmID
TASK_BOUNDARY_INVALID_FARM_ID = [
    None, # None value
]

# Valid cases for assignedTo
TASK_VALID_ASSIGNED_TO = [
    1, # Assuming 1 is a valid UserProfile ID
    2, # Assuming 2 is a valid UserProfile ID
    3, # Assuming 3 is a valid UserProfile ID
    4, # Assuming 4 is a valid UserProfile ID
    5, # Assuming 5 is a valid UserProfile ID
]

# Invalid cases for assignedTo
TASK_INVALID_ASSIGNED_TO = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for assignedTo
TASK_BOUNDARY_VALID_ASSIGNED_TO = [
    1, # Assuming 1 is a valid UserProfile ID
]

# Boundary invalid cases for assignedTo
TASK_BOUNDARY_INVALID_ASSIGNED_TO = [
    None, # None value
]

# Valid cases for name
TASK_VALID_NAME = [
    "Task 1", # Valid name
    "Harvesting", # Valid name
    "Irrigation", # Valid name
    "Fertilizing", # Valid name
    "Pest Control", # Valid name
]

# Invalid cases for name
TASK_INVALID_NAME = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for name
TASK_BOUNDARY_VALID_NAME = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for name
TASK_BOUNDARY_INVALID_NAME = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

# Valid cases for description
TASK_VALID_DESCRIPTION = [
    "This task involves harvesting crops.", # Valid description
    "Irrigation of the north field.", # Valid description
    "Applying fertilizer to the south field.", # Valid description
    "Pest control in the greenhouse.", # Valid description
    "General maintenance of farm equipment.", # Valid description
]

# Invalid cases for description
TASK_INVALID_DESCRIPTION = [
    None, # None value
    "A" * 256, # Exceeds maximum length
]

# Boundary valid cases for description
TASK_BOUNDARY_VALID_DESCRIPTION = [
    "", # Empty string
    "A", # Exactly 1 character
    "B" * 200, # Exactly 255 characters
]

# Boundary invalid cases for description
TASK_BOUNDARY_INVALID_DESCRIPTION = [
    "C" * 256, # Exceeds maximum length
]

# Valid cases for timeStamp
TASK_VALID_TIMESTAMP = [
    "2023-01-01T00:00:00Z", # Valid datetime
    "2023-06-15T12:30:45Z", # Valid datetime
    "2022-12-31T23:59:59Z", # Valid datetime
    "2021-07-20T08:15:30Z", # Valid datetime
    "2020-02-29T00:00:00Z", # Valid datetime (leap year)
]

# Invalid cases for timeStamp
TASK_INVALID_TIMESTAMP = [
    None, # None value
    "invalid", # Non-datetime value
    "2023-13-01T00:00:00Z", # Invalid month
    "2023-00-01T00:00:00Z", # Invalid month
    "2023-01-32T00:00:00Z", # Invalid day
]

# Boundary valid cases for timeStamp
TASK_BOUNDARY_VALID_TIMESTAMP = [
    "2023-01-01T00:00:00Z", # Valid datetime
]

# Boundary invalid cases for timeStamp
TASK_BOUNDARY_INVALID_TIMESTAMP = [
    None, # None value
]

# Valid cases for isCompleted
TASK_VALID_IS_COMPLETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for isCompleted
TASK_INVALID_IS_COMPLETED = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for isCompleted
TASK_BOUNDARY_VALID_IS_COMPLETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for isCompleted
TASK_BOUNDARY_INVALID_IS_COMPLETED = [
    None, # None value
]

# Valid cases for isArchived
TASK_VALID_IS_ARCHIVED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for isArchived
TASK_INVALID_IS_ARCHIVED = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for isArchived
TASK_BOUNDARY_VALID_IS_ARCHIVED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for isArchived
TASK_BOUNDARY_INVALID_IS_ARCHIVED = [
    None, # None value
]

# Valid cases for isDeleted
TASK_VALID_IS_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Invalid cases for isDeleted
TASK_INVALID_IS_DELETED = [
    None, # None value
    "invalid", # Non-boolean value
    1, # Non-boolean value
    0, # Non-boolean value
]

# Boundary valid cases for isDeleted
TASK_BOUNDARY_VALID_IS_DELETED = [
    True, # Valid boolean value
    False, # Valid boolean value
]

# Boundary invalid cases for isDeleted
TASK_BOUNDARY_INVALID_IS_DELETED = [
    None, # None value
]

# Valid cases for dueDate
TASK_VALID_DUE_DATE = [
    "2025-12-31",  # Valid date
    "2025-10-15",  # Valid date
    "2025-01-01",  # Valid date
    "2026-07-20",  # Valid date
    "2027-02-28",  # Valid date
    "2024-12-31", # Valid date
    "2025-06-15", # Valid date
    "2025-01-01", # Valid date
    "2026-07-20", # Valid date
    "2027-02-28", # Valid date
]

# Invalid cases for dueDate
TASK_INVALID_DUE_DATE = [
    "invalid", # Non-date value
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
    "2023-01-32", # Invalid day
]

# Boundary valid cases for dueDate
TASK_BOUNDARY_VALID_DUE_DATE = [
    "2024-12-31", # Valid date
]

# Boundary invalid cases for dueDate
TASK_BOUNDARY_INVALID_DUE_DATE = [
    None, # None value
]

# Valid cases for expiry
TASK_VALID_EXPIRY = [
    "2023-12-31", # Valid date
    "2024-06-15", # Valid date
    "2025-01-01", # Valid date
    "2026-07-20", # Valid date
    "2027-02-28", # Valid date
]

# Invalid cases for expiry
TASK_INVALID_EXPIRY = [
    "invalid", # Non-date value
    "2023-13-01", # Invalid month
    "2023-00-01", # Invalid month
    "2023-01-32", # Invalid day
]

# Boundary valid cases for expiry
TASK_BOUNDARY_VALID_EXPIRY = [
    "2023-12-31", # Valid date
]

# Boundary invalid cases for expiry
TASK_BOUNDARY_INVALID_EXPIRY = [
    None, # None value
]

# Valid cases for status
TASK_VALID_STATUS = [
    0, # Not Started
    1, # In Progress
    2, # Blocked
    3, # Review
    4, # Complete
    5, # Archived
]

# Invalid cases for status
TASK_INVALID_STATUS = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    6, # Out of choices range
]

# Boundary valid cases for status
TASK_BOUNDARY_VALID_STATUS = [
    0, # Lower boundary
    5, # Upper boundary
]

# Boundary invalid cases for status
TASK_BOUNDARY_INVALID_STATUS = [
    -1, # Below lower boundary
    6, # Above upper boundary
]

# Valid cases for priority
TASK_VALID_PRIORITY = [
    0, # Low
    1, # Medium
    2, # High
    3, # Urgent
]

# Invalid cases for priority
TASK_INVALID_PRIORITY = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    4, # Out of choices range
]

# Boundary valid cases for priority
TASK_BOUNDARY_VALID_PRIORITY = [
    0, # Lower boundary
    3, # Upper boundary
]

# Boundary invalid cases for priority
TASK_BOUNDARY_INVALID_PRIORITY = [
    -1, # Below lower boundary
    4, # Above upper boundary
]

TASK_SUPERSET = {
    "farmID" : [
        TASK_VALID_FARM_ID,
        TASK_INVALID_FARM_ID,
        TASK_BOUNDARY_VALID_FARM_ID,
        TASK_BOUNDARY_INVALID_FARM_ID],
    "assignedTo" : [
        TASK_VALID_ASSIGNED_TO,
        TASK_INVALID_ASSIGNED_TO,
        TASK_BOUNDARY_VALID_ASSIGNED_TO,
        TASK_BOUNDARY_INVALID_ASSIGNED_TO],
    "name" : [
        TASK_VALID_NAME,
        TASK_INVALID_NAME,
        TASK_BOUNDARY_VALID_NAME,
        TASK_BOUNDARY_INVALID_NAME],
    "description" : [
        TASK_VALID_DESCRIPTION,
        TASK_INVALID_DESCRIPTION,
        TASK_BOUNDARY_VALID_DESCRIPTION,
        TASK_BOUNDARY_INVALID_DESCRIPTION],
    "timeStamp" : [
        TASK_VALID_TIMESTAMP,
        TASK_INVALID_TIMESTAMP,
        TASK_BOUNDARY_VALID_TIMESTAMP,
        TASK_BOUNDARY_INVALID_TIMESTAMP],
    "isCompleted" : [
        TASK_VALID_IS_COMPLETED,
        TASK_INVALID_IS_COMPLETED,
        TASK_BOUNDARY_VALID_IS_COMPLETED,
        TASK_BOUNDARY_INVALID_IS_COMPLETED],
    "isArchived" : [
        TASK_VALID_IS_ARCHIVED,
        TASK_INVALID_IS_ARCHIVED,
        TASK_BOUNDARY_VALID_IS_ARCHIVED,
        TASK_BOUNDARY_INVALID_IS_ARCHIVED],
    "isDeleted" : [
        TASK_VALID_IS_DELETED,
        TASK_INVALID_IS_DELETED,
        TASK_BOUNDARY_VALID_IS_DELETED,
        TASK_BOUNDARY_INVALID_IS_DELETED],
    "dueDate" : [
        TASK_VALID_DUE_DATE,
        TASK_INVALID_DUE_DATE,
        TASK_BOUNDARY_VALID_DUE_DATE,
        TASK_BOUNDARY_INVALID_DUE_DATE],
    "expiry" : [
        TASK_VALID_EXPIRY,
        TASK_INVALID_EXPIRY,
        TASK_BOUNDARY_VALID_EXPIRY,
        TASK_BOUNDARY_INVALID_EXPIRY],
    "status" : [
        TASK_VALID_STATUS,
        TASK_INVALID_STATUS,
        TASK_BOUNDARY_VALID_STATUS,
        TASK_BOUNDARY_INVALID_STATUS],
    "priority" : [
        TASK_VALID_PRIORITY,
        TASK_INVALID_PRIORITY,
        TASK_BOUNDARY_VALID_PRIORITY,
        TASK_BOUNDARY_INVALID_PRIORITY]
}

# Valid cases for farmID
KANBAN_VALID_FARM_ID = [
    1, # Assuming 1 is a valid FarmInfo ID
    2, # Assuming 2 is a valid FarmInfo ID
    3, # Assuming 3 is a valid FarmInfo ID
    4, # Assuming 4 is a valid FarmInfo ID
    5, # Assuming 5 is a valid FarmInfo ID
]

# Invalid cases for farmID
KANBAN_INVALID_FARM_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for farmID
KANBAN_BOUNDARY_VALID_FARM_ID = [
    1, # Assuming 1 is a valid FarmInfo ID
]

# Boundary invalid cases for farmID
KANBAN_BOUNDARY_INVALID_FARM_ID = [
    None, # None value
]

# Valid cases for name
KANBAN_VALID_NAME = [
    "Kanban Board 1", # Valid name
    "Main Board", # Valid name
    "Project Board", # Valid name
    "Development Board", # Valid name
    "Marketing Board", # Valid name
]

# Invalid cases for name
KANBAN_INVALID_NAME = [
    None, # None value
    "", # Empty string
    "A" * 101, # Exceeds maximum length
]

# Boundary valid cases for name
KANBAN_BOUNDARY_VALID_NAME = [
    "A", # Exactly 1 character
    "B" * 100, # Exactly 100 characters
]

# Boundary invalid cases for name
KANBAN_BOUNDARY_INVALID_NAME = [
    "", # Empty string
    "C" * 101, # Exceeds maximum length
]

KANBAN_SUPERSET = {
    "farmID" : [
        KANBAN_VALID_FARM_ID,
        KANBAN_INVALID_FARM_ID,
        KANBAN_BOUNDARY_VALID_FARM_ID,
        KANBAN_BOUNDARY_INVALID_FARM_ID],
    "name" : [
        KANBAN_VALID_NAME,
        KANBAN_INVALID_NAME,
        KANBAN_BOUNDARY_VALID_NAME,
        KANBAN_BOUNDARY_INVALID_NAME]
}

# Valid cases for kanbanID
KANBAN_CONTENTS_VALID_KANBAN_ID = [
    1, # Assuming 1 is a valid Kanban ID
    2, # Assuming 2 is a valid Kanban ID
    3, # Assuming 3 is a valid Kanban ID
    4, # Assuming 4 is a valid Kanban ID
    5, # Assuming 5 is a valid Kanban ID
]

# Invalid cases for kanbanID
KANBAN_CONTENTS_INVALID_KANBAN_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for kanbanID
KANBAN_CONTENTS_BOUNDARY_VALID_KANBAN_ID = [
    1, # Assuming 1 is a valid Kanban ID
]

# Boundary invalid cases for kanbanID
KANBAN_CONTENTS_BOUNDARY_INVALID_KANBAN_ID = [
    None, # None value
]

# Valid cases for taskID
KANBAN_CONTENTS_VALID_TASK_ID = [
    1, # Assuming 1 is a valid Task ID
    2, # Assuming 2 is a valid Task ID
    3, # Assuming 3 is a valid Task ID
    4, # Assuming 4 is a valid Task ID
    5, # Assuming 5 is a valid Task ID
]

# Invalid cases for taskID
KANBAN_CONTENTS_INVALID_TASK_ID = [
    None, # None value
    "invalid", # Non-integer value
    -1, # Negative value
    0, # Zero value
    999999, # Assuming this ID does not exist
]

# Boundary valid cases for taskID
KANBAN_CONTENTS_BOUNDARY_VALID_TASK_ID = [
    1, # Assuming 1 is a valid Task ID
]

# Boundary invalid cases for taskID
KANBAN_CONTENTS_BOUNDARY_INVALID_TASK_ID = [
    None, # None value
]

# Valid cases for order
KANBAN_CONTENTS_VALID_ORDER = [
    1, # Valid order
    2, # Valid order
    3, # Valid order
    4, # Valid order
    5, # Valid order
]

# Invalid cases for order
KANBAN_CONTENTS_INVALID_ORDER = [
    None, # None value
    "invalid", # Non-integer value
    0, # Zero value
]

# Boundary valid cases for order
KANBAN_CONTENTS_BOUNDARY_VALID_ORDER = [
    1, # Lower boundary
    32767, # Upper boundary for PositiveSmallIntegerField
]

# Boundary invalid cases for order
KANBAN_CONTENTS_BOUNDARY_INVALID_ORDER = [
    -1, # Below lower boundary
    32768, # Above upper boundary for PositiveSmallIntegerField
]

KANBAN_CONTENTS_SUPERSET = {
    "kanbanID" : [
        KANBAN_CONTENTS_VALID_KANBAN_ID,
        KANBAN_CONTENTS_INVALID_KANBAN_ID,
        KANBAN_CONTENTS_BOUNDARY_VALID_KANBAN_ID,
        KANBAN_CONTENTS_BOUNDARY_INVALID_KANBAN_ID],
    "taskID" : [
        KANBAN_CONTENTS_VALID_TASK_ID,
        KANBAN_CONTENTS_INVALID_TASK_ID,
        KANBAN_CONTENTS_BOUNDARY_VALID_TASK_ID,
        KANBAN_CONTENTS_BOUNDARY_INVALID_TASK_ID],
    "order" : [
        KANBAN_CONTENTS_VALID_ORDER,
        KANBAN_CONTENTS_INVALID_ORDER,
        KANBAN_CONTENTS_BOUNDARY_VALID_ORDER,
        KANBAN_CONTENTS_BOUNDARY_INVALID_ORDER]
}



# Functions
def generate_dataset_from_model(
        model  : dict      ,
        verbose: bool=False,
        timing : bool=False,
        output : bool=False
        ):
    """

    ### Description
    Generates a dataset `list` of a valid and every possible invalid model for the given data
    model.

    The input `model` is a `key`:`value` dictionary with `key` being the name of a field in the
    model and `value` being a `list` of all the test values to be assigned to the field. The first
    value in the `value` list is assumed to be a valid value.

    The output `dataset` is a list that will contain dictionaries. These dictionaries will contain
    the same keys as `model`. The first dictionary will contain only valid data, using the first
    value in every `value` list in `model`. For every other value for every `key` in `model`, there
    will be a seperate dictionary in `dataset` that contains that value for that key, with the rest
    of the values keeping the first value.

    ---

    ### Inputs
    Parameters
    - `model`: `dict` - The input model to generate a dataset for, containing all of the testing
    values.
    - `verbose`: `bool` - If `True`, the function will print tracking status and meta to the CLI.
    - `timing`: `bool` - If `True`, the function will time itself and print the compute time to the
    CLI.
    - `output`: `bool` - If `True`, the function will print `dataset` to the CLI.

    ---

    ### Outputs
    Returns
    - `dataset`: `list` - The list of models containing all of the testing values.

    Side Effects
    - None - This function is not intended to have side effects.

    ---

    ### Notes
    This function is not explicitly designed to generate sequences of valid models, for testing
    functions that require multiple inputs. Each model in the list is independent from all the
    other models. Extracting multiple models and ensuring harmonious primary keys is a task for
    other functions to handle.

    """

    # Function start
    if verbose:
        print(f"""-------- Running generate_dataset_from_model --------
model keys = {list(model.keys())}
{verbose    = }
{timing     = }
{output     = }""")
    if timing:
        time_start = time()

    # Start with a valid version
    if verbose:
        print("\n--- Initialising ---")
    valid_model = model.copy()
    for key in valid_model:
        valid_model[key] = valid_model[key][0]

    # Initialise dataset
    dataset = [valid_model]

    if verbose:
        print("\n--- Generating ---")
        model_keys = model.keys()
        num_keys = len(model_keys)

        # Iterating every key
        for i, key in enumerate(model_keys):
            key_values = model[key][1:]
            num_values = len(key_values)

            # Iterating every value
            for j, value in enumerate(key_values):
                sample_model = valid_model.copy()
                sample_model[key] = value
                dataset.append(sample_model)
                # Tracker
                print(f"\r- {i+1} / {num_keys} keys | {j+1} / {num_values} values -     ", end='')
        print("") # Final newline

    else: # Not verbose
        # Iterating every key
        for key in model.keys():
            # Iterating every value
            for value in model[key][1:]:
                sample_model = valid_model.copy()
                sample_model[key] = value
                dataset.append(sample_model)

    # Output
    if verbose:
        print("\n--- Complete ---")
        print(f"Number of models: {len(dataset)}")
    if timing:
        time_end = time()
        print(f"Time taken: {time_end - time_start} seconds")
    if output:
        if verbose:
            print("\n--- Output: dataset ---")
        print(dataset)

    return dataset
