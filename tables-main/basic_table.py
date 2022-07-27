from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
from getLogTableInfo import log_info_for_table

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Declare your table
# class ItemTable(Table):
#     name = Col('Name')
#     description = Col('Description')

items = log_info_for_table()
# items = [dict(name='Name1', description='Description1'),
#          dict(name='Name2', description='Description2'),
#          dict(name='Name3', description='Description3')]

# Or, more likely, load items from your database with something like
# items = ItemModel.query.all()

# Populate the table
# table = ItemTable(items)


# class Record(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True)
#     age = db.Column(db.Integer, index=True)
#     address = db.Column(db.String(256))
#     phone = db.Column(db.String(20))
#     email = db.Column(db.String(120), index=True)

db.create_all()


@app.route('/')
def index():
    # records = Record.query
    records = items
    return render_template('basic_table.html', title='Basic Table',
                           records=records)


if __name__ == '__main__':
    app.run()
