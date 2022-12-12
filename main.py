from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import random
app = Flask(__name__)

dir = os.path.dirname(__file__)
db_path = os.path.join(dir, 'vie_database.db')

# the name of the database; add path if necessary
db_name = 'D:\Developer\datatable_corpora\database.db'
new_db_name = 'D:\Developer\datatable_corpora\\vie_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type

class VietnameseToBahnaric(db.Model):
    __tablename__ = 'vietobahnar'
    id = db.Column(db.Integer, primary_key=True)
    vietnamese = db.Column(db.String)
    bahnaric = db.Column(db.String)
    pos = db.Column(db.String)
    binhdinh = db.Column(db.Integer)
    kontum = db.Column(db.Integer)
    gialai = db.Column(db.Integer)

    def to_dict(self):
        return{
            'id': self.id,
            'vietnamese': self.vietnamese,
            'bahnaric': self.bahnaric,
            'pos': self.pos,
            'binhdinh': self.binhdinh,
            'kontum': self.kontum,
            'gialai': self.gialai
        }

class BahnaricToVietnamese(db.Model):
    __tablename__ = 'bahnartovie'
    id = db.Column(db.Integer, primary_key=True)
    bahnaric = db.Column(db.String)
    vietnamese = db.Column(db.String)
    pos = db.Column(db.String)

    def to_dict(self):
        return{
            'id': self.id,
            'bahnaric': self.bahnaric,
            'vietnamese': self.vietnamese,
            'pos': self.pos
        }

#routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data():
    query = VietnameseToBahnaric.query
    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            VietnameseToBahnaric.vietnamese.like(f'%{search}%'),
            VietnameseToBahnaric.pos.like(f'%{search}%'),
        ))
    total_filtered = query.count()
    
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)
    
    #response
    return {
        'data': [word.to_dict() for word in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': VietnameseToBahnaric.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/bahna')
def dataBahna():
    query = VietnameseToBahnaric.query
    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            VietnameseToBahnaric.bahnaric.like(f'%{search}%'),
        ))
    total_filtered = query.count()
    
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)
    
    #response
    return {
        'data': [word.to_dict() for word in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': VietnameseToBahnaric.query.count(),
        'draw': request.args.get('draw', type=int),
    }

bana_bd = "./static/assets/audio/Bana-BinhDinh/audio_by_word"
bana_kt = "./static/assets/audio/Bana-KonTum/audio_by_word"
bana_gl = "./static/assets/audio/Bana-GiaLai/audio_by_word"

@app.route('/audio/<region_tag>/<word>', methods=['GET'])
def audio(region_tag, word):
    dirr = ''
    fn = ''

    if region_tag == "BD":
        dirr = os.path.join(bana_bd, word)

    elif region_tag == "KT":
        dirr = os.path.join(bana_kt, word)

    elif region_tag == "GL":
        dirr = os.path.join(bana_gl, word)

    dirr = dirr.strip()
    print('1', dirr)
    print('2', os.listdir(dirr))
    print('3', os.path.join(dirr, '047.mp3'))
    list_files = os.listdir(dirr)
    fn = random.choice(list_files)

    return send_from_directory(dirr, fn)

# @app.route('/api/bahna')
# def data_bahna():
#     query = BahnaricToVietnamese.query
#     # search filter
#     search = request.args.get('search[value]')
#     if search:
#         query = query.filter(db.or_(
#             BahnaricToVietnamese.bahnaric.like(f'%{search}%'),
#         ))
#     total_filtered = query.count()
    
#     # pagination
#     start = request.args.get('start', type=int)
#     length = request.args.get('length', type=int)
#     query = query.offset(start).limit(length)
    
#     #response
#     return {
#         'data': [word.to_dict() for word in query],
#         'recordsFiltered': total_filtered,
#         'recordsTotal': BahnaricToVietnamese.query.count(),
#         'draw': request.args.get('draw', type=int),
#     }


if __name__ == '__main__':
    app.run(debug=True)