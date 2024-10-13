from flask import request
from flask_restful import Resource
from models import db, DayRecord, DayStock, NightStock
from datetime import datetime

class DayRecordResource(Resource):
    def get(self, date=None):
        if date:
            day_record = DayRecord.query.filter_by(date=datetime.strptime(date, '%Y-%m-%d').date()).first()
            if not day_record:
                return {'message': 'No record found for the given date'}, 404

            total_day_cost = sum(day_stock.cost for day_stock in day_record.day_stocks)
            total_night_cost = sum(night_stock.cost for night_stock in day_record.night_stocks)

            day_stocks = [{
                'id': day_stock.id,
                'item_name': day_stock.item_name,
                'opening_stock': day_stock.opening_stock,
                'production': day_stock.production,
                'sales': day_stock.sales,
                'manually_entered_closing_stock': day_stock.manually_entered_closing_stock,
                'calculated_closing_stock': day_stock.closing_stock,
                'difference_in_closing_stock': day_stock.difference_in_closing_stock,
                'price_per_unit': day_stock.price_per_unit,
                'earnings': day_stock.earnings,
                'cost': day_stock.cost
            } for day_stock in day_record.day_stocks]

            night_stocks = [{
                'id': night_stock.id,
                'item_name': night_stock.item_name,
                'opening_stock': night_stock.opening_stock,
                'production': night_stock.production,
                'sales': night_stock.sales,
                'manually_entered_closing_stock': night_stock.manually_entered_closing_stock,
                'calculated_closing_stock': night_stock.closing_stock,
                'difference_in_closing_stock': night_stock.difference_in_closing_stock,
                'price_per_unit': night_stock.price_per_unit,
                'earnings': night_stock.earnings,
                'cost': night_stock.cost
            } for night_stock in day_record.night_stocks]

            return {
                'date': day_record.date.isoformat(),
                'day_stocks': day_stocks,
                'night_stocks': night_stocks,
                'total_day_cost': total_day_cost,
                'total_night_cost': total_night_cost
            }, 200
        else:
            day_records = DayRecord.query.all()
            results = []
            for record in day_records:
                total_day_cost = sum(ds.cost for ds in record.day_stocks)
                total_night_cost = sum(ns.cost for ns in record.night_stocks)

                results.append({
                    'date': record.date.isoformat(),
                    'total_day_cost': total_day_cost,
                    'total_night_cost': total_night_cost,
                    'day_stocks': [{
                        'id': ds.id,
                        'item_name': ds.item_name,
                        'opening_stock': ds.opening_stock,
                        'production': ds.production,
                        'sales': ds.sales,
                        'manually_entered_closing_stock': ds.manually_entered_closing_stock,
                        'calculated_closing_stock': ds.closing_stock,
                        'difference_in_closing_stock': ds.difference_in_closing_stock,
                        'price_per_unit': ds.price_per_unit,
                        'earnings': ds.earnings,
                        'cost': ds.cost
                    } for ds in record.day_stocks],
                    'night_stocks': [{
                        'id': ns.id,
                        'item_name': ns.item_name,
                        'opening_stock': ns.opening_stock,
                        'production': ns.production,
                        'sales': ns.sales,
                        'manually_entered_closing_stock': ns.manually_entered_closing_stock,
                        'calculated_closing_stock': ns.closing_stock,
                        'difference_in_closing_stock': ns.difference_in_closing_stock,
                        'price_per_unit': ns.price_per_unit,
                        'earnings': ns.earnings,
                        'cost': ns.cost
                    } for ns in record.night_stocks],
                })
            return results, 200



class DayStockResource(Resource):
    def post(self):
        data = request.get_json()

        # Fetch or create a DayRecord for the current date
        day_record = DayRecord.query.filter_by(date=datetime.utcnow().date()).first()
        if not day_record:
            day_record = DayRecord(date=datetime.utcnow().date())
            db.session.add(day_record)
            db.session.commit()

        # Add new DayStock with data from the request
        day_stock = DayStock(
            item_name=data['item_name'],
            opening_stock=data['opening_stock'],
            production=data['production'],
            sales=data['sales'],
            manually_entered_closing_stock=data['manually_entered_closing_stock'],
            price_per_unit=data['price_per_unit'],
            cost=data['cost'],
            day_record_id=day_record.id
        )
        db.session.add(day_stock)
        db.session.commit()

        return {
            'message': 'Day stock added successfully!',
            'id': day_stock.id,
            'calculated_closing_stock': day_stock.closing_stock,
            'difference_in_closing_stock': day_stock.difference_in_closing_stock
        }, 201

    def put(self, id):
        day_stock = DayStock.query.get(id)
        if not day_stock:
            return {'message': 'Day stock not found'}, 404

        data = request.get_json()
        day_stock.item_name = data['item_name']
        day_stock.opening_stock = data['opening_stock']
        day_stock.production = data['production']
        day_stock.sales = data['sales']
        day_stock.manually_entered_closing_stock = data['manually_entered_closing_stock']
        day_stock.price_per_unit = data['price_per_unit']
        day_stock.cost = data['cost']

        db.session.commit()

        return {
            'message': 'Day stock updated successfully!'
        }, 200

    def delete(self, id):
        day_stock = DayStock.query.get(id)
        if not day_stock:
            return {'message': 'Day stock not found'}, 404

        db.session.delete(day_stock)
        db.session.commit()

        return {
            'message': 'Day stock deleted successfully!'
        }, 200


class NightStockResource(Resource):
    def post(self):
        data = request.get_json()

        # Fetch or create a DayRecord for the current date
        day_record = DayRecord.query.filter_by(date=datetime.utcnow().date()).first()
        if not day_record:
            day_record = DayRecord(date=datetime.utcnow().date())
            db.session.add(day_record)
            db.session.commit()

        # Add new NightStock with data from the request
        night_stock = NightStock(
            item_name=data['item_name'],
            opening_stock=data['opening_stock'],
            production=data['production'],
            sales=data['sales'],
            manually_entered_closing_stock=data['manually_entered_closing_stock'],
            price_per_unit=data['price_per_unit'],
            cost=data['cost'],
            day_record_id=day_record.id
        )
        db.session.add(night_stock)
        db.session.commit()

        return {
            'message': 'Night stock added successfully!',
            'id': night_stock.id,
            'calculated_closing_stock': night_stock.closing_stock,
            'difference_in_closing_stock': night_stock.difference_in_closing_stock
        }, 201

    def put(self, id):
        night_stock = NightStock.query.get(id)
        if not night_stock:
            return {'message': 'Night stock not found'}, 404

        data = request.get_json()
        night_stock.item_name = data['item_name']
        night_stock.opening_stock = data['opening_stock']
        night_stock.production = data['production']
        night_stock.sales = data['sales']
        night_stock.manually_entered_closing_stock = data['manually_entered_closing_stock']
        night_stock.price_per_unit = data['price_per_unit']
        night_stock.cost = data['cost']

        db.session.commit()

        return {
            'message': 'Night stock updated successfully!',
            'calculated_closing_stock': night_stock.closing_stock,
            'difference_in_closing_stock': night_stock.difference_in_closing_stock
        }, 200

    def delete(self, id):
        night_stock = NightStock.query.get(id)
        if not night_stock:
            return {'message': 'Night stock not found'}, 404

        db.session.delete(night_stock)
        db.session.commit()

        return {
            'message': 'Night stock deleted successfully!'
        }, 200
