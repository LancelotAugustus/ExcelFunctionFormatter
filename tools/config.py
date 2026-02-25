import re

BASE_DOMAIN = "support.microsoft.com"
LANGUAGE_CODE = "en-us"
PRODUCT_SEGMENT = "office"
EXCEL_FUNCTIONS_UUID = "b3944572-255d-4efb-bb96-c6d90033e188"

UUID_PATTERN = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

SPECIAL_UUID_MAP = {
    'FORECAST.ETS': '15389b8b-677e-4fbd-bd95-21d464333f41',
    'FORECAST.ETS.CONFINT': '6d4a7557-11fa-4678-9e6a-dbcc31a7c7df',
    'FORECAST.ETS.SEASONALITY': '32a27a3b-d22f-42ce-8c5d-ef3649269f3c',
    'FORECAST.ETS.STAT': '60f2ae14-d0cf-465e-9736-625ccaaa60b4',
    'FORECAST.LINEAR': '50ca49c9-7b40-4892-94e4-7ad38bbeda99',
}
SPECIAL_NAME_MAP = {
    'BETA.INVn': 'BETA.INV'
}
