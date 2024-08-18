from transit34_fastapi import geoindexing
import transit34_fastapi.endpoints.api as api
import transit34_fastapi.endpoints.website as web

geoindexing.init()

web.app.mount("/api", api.app)
app = web.app
