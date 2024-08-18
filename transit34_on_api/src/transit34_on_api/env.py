import os


def if_not_none(value, default):
    return value if value is not None else default


class Env:
    SERVICE_URL = "https://ntcapi.iett.istanbul/service"
    OAUTH2_URL = "https://ntcapi.iett.istanbul/oauth2/v2/auth"
    USER_AGENT = "Mobiett/61 CFNetwork/1410.0.3 Darwin/22.6.0"
    GRANT_TYPE = "client_credentials"
    SCOPE = "VLCn2qErUdrr1Ehg0yxWObMW9krFb7RC service"
    CLIENT_ID = "pLwqtobYHTBshBWRrEZdSWsngOywQvHa"
    CLIENT_SECRET = "JERLUJgaZSygMTqoCtrhrVnvqeVGGVznktlwuOfHqmQTzjnC"
    REDIS_HOSTNAME = "127.0.0.1"
    REDIS_PORT = 6379


Env.SERVICE_URL = if_not_none(os.getenv("SERVICE_URL"), Env.SERVICE_URL)
Env.OAUTH2_URL = if_not_none(os.getenv("OAUTH2_URL"), Env.OAUTH2_URL)
Env.USER_AGENT = if_not_none(os.getenv("USER_AGENT"), Env.USER_AGENT)
Env.GRANT_TYPE = if_not_none(os.getenv("GRANT_TYPE"), Env.GRANT_TYPE)
Env.SCOPE = if_not_none(os.getenv("SCOPE"), Env.SCOPE)
Env.CLIENT_ID = if_not_none(os.getenv("CLIENT_ID"), Env.CLIENT_ID)
Env.CLIENT_SECRET = if_not_none(os.getenv("CLIENT_SECRET"), Env.CLIENT_SECRET)
Env.REDIS_HOSTNAME = if_not_none(os.getenv("REDIS_HOSTNAME"), Env.REDIS_HOSTNAME)
Env.REDIS_PORT = if_not_none(os.getenv("REDIS_PORT"), Env.REDIS_PORT)
