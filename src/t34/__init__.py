from t34 import geoindexing
import t34.endpoints.api as api
import t34.endpoints.website as web

geoindexing.init()

web.app.mount("/api", api.app)
app = web.app
