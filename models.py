from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DayRecord(db.Model):
    __tablename__ = 'day_records'
    id = db.Column(db.Integer, primary_key=True)
    # Use datetime.now() to store the local time
    date = db.Column(db.Date, nullable=False, default=datetime.now().date)

    day_stocks = db.relationship('DayStock', backref='day_record', lazy=True)
    night_stocks = db.relationship('NightStock', backref='day_record', lazy=True)


class DayStock(db.Model):
    __tablename__ = 'day_stocks'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    opening_stock = db.Column(db.Integer, nullable=False)
    production = db.Column(db.Integer, nullable=False)
    sales = db.Column(db.Integer, nullable=False)
    manually_entered_closing_stock = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    # Foreign key to reference DayRecord
    day_record_id = db.Column(db.Integer, db.ForeignKey('day_records.id'), nullable=False)

    @property
    def closing_stock(self):
        return self.opening_stock + self.production - self.sales

    @property
    def difference_in_closing_stock(self):
        if self.manually_entered_closing_stock is not None:
            return self.manually_entered_closing_stock - self.closing_stock
        return 0

    @property
    def earnings(self):
        return self.sales * self.price_per_unit


class NightStock(db.Model):
    __tablename__ = 'night_stocks'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    opening_stock = db.Column(db.Integer, nullable=False)
    production = db.Column(db.Integer, nullable=False)
    sales = db.Column(db.Integer, nullable=False)
    manually_entered_closing_stock = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    # Foreign key to reference DayRecord
    day_record_id = db.Column(db.Integer, db.ForeignKey('day_records.id'), nullable=False)

    @property
    def closing_stock(self):
        return self.opening_stock + self.production - self.sales

    @property
    def difference_in_closing_stock(self):
        if self.manually_entered_closing_stock is not None:
            return self.manually_entered_closing_stock - self.closing_stock
        return 0

    @property
    def earnings(self):
        return self.sales * self.price_per_unit
