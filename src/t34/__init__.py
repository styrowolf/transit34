from t34 import geoindexing
import t34.endpoints.api as api
import t34.endpoints.website as web
import t34.fleet as fleet

geoindexing.init()
fleet.init()

web.app.mount("/api", api.app)
app = web.app
