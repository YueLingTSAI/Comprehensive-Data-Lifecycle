from flask import Flask
from flask_restful import Api
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from model import db
import sshtunnel

from resource.dcard import Dcards
from resource.foodnext import Foodnext_camas, Foodnext_louisas
from resource.google_map import GoogleMaps, GoogleMapRatingCount, GoogleMapStatistics, GoogleMapStoreRegion
from resource.ptt import Ptts
from resource.youtube import Youtube_camas, Youtube_louisas

# SSH tunnel configuration
ssh_tunnel = sshtunnel.SSHTunnelForwarder(
    ('dv107.coded2.fun', 8022),  # 跳板機位址
    ssh_username='joelle',
    ssh_password='123456',  # 或使用 ssh_pkey='密鑰檔案路徑'
    remote_bind_address=('labdb.coded2.fun', 3306)  # 目標資料庫伺服器和埠口
)

# 啟動 SSH 隧道
ssh_tunnel.start()

# Flask init
app = Flask(__name__)

# FlaskRestFul init
api = Api(app)

# DB setting
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://sophia:123456dv107@127.0.0.1:{ssh_tunnel.local_bind_port}/CLEAN_SOPHIA"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 60,
    "pool_timeout": 300,
    "pool_size": 20,
}


# Swagger

app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Database data show",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
    }
)

# Swagger init
docs = FlaskApiSpec(app)

# Route
api.add_resource(Dcards, "/dcard")
docs.register(Dcards)

api.add_resource(Ptts, "/ptt")
docs.register(Ptts)

api.add_resource(Foodnext_camas, "/foodnext_cama")
api.add_resource(Foodnext_louisas, "/foodnext_louisa")
docs.register(Foodnext_camas)
docs.register(Foodnext_louisas)

api.add_resource(GoogleMaps, "/google_map")
api.add_resource(GoogleMapRatingCount, "/GoogleMapRatingCount")
api.add_resource(GoogleMapStatistics, "/GoogleMapStatistics")
api.add_resource(GoogleMapStoreRegion, "/GoogleMapStoreRegion")
docs.register(GoogleMaps)
docs.register(GoogleMapRatingCount)
docs.register(GoogleMapStatistics)
docs.register(GoogleMapStoreRegion)

api.add_resource(Youtube_camas, "/youtube_cama")
api.add_resource(Youtube_louisas, "/youtube_louisa")
docs.register(Youtube_camas)
docs.register(Youtube_louisas)

if __name__ == "__main__":
    # DB setting
    db.init_app(app)
    db.app = app
    app.run(host="0.0.0.0", port="10009", debug=True, use_reloader=True)
