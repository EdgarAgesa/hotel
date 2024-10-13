from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
import os
from models import db
from resources import DayStockResource, NightStockResource, DayRecordResource
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
api = Api(app)
migrate = Migrate(app, db)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://hotel_yyax_user:TTTVfmRliv4XtcuV52CU9Agh08OKz5B7@dpg-cs63kf08fa8c73asts90-a.oregon-postgres.render.com/hotel_yyax")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register the API resources
api.add_resource(DayStockResource, '/day-stock/<int:id>', '/day-stock')
api.add_resource(NightStockResource, '/night-stock/<int:id>', '/night-stock')
api.add_resource(DayRecordResource, '/day-record', '/day-record/<string:date>')

if __name__ == '__main__':
    app.run(debug=True)
