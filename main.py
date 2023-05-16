from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import random
app = Flask(__name__)

dir = os.path.dirname(__file__)
db_path = os.path.join(dir, 'vie_database.db')

# the name of the database; add path if necessary
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


class NglieuCauKHKT(db.Model):
    __tablename__ = 'KHKT'
    ID = db.Column(db.Integer, primary_key=True)
    vietnamese = db.Column(db.String)
    bahnaric = db.Column(db.String)
    def to_dict(self):
        return{
            'ID': self.ID,
            'vietnamese': self.vietnamese,
            'bahnaric': self.bahnaric
        }
    
class NglieuCauKHCN(db.Model):
    __tablename__ = 'KHCN'
    ID = db.Column(db.Integer, primary_key=True)
    vietnamese = db.Column(db.String)
    bahnaric = db.Column(db.String)
    def to_dict(self):
        return{
            'ID': self.ID,
            'vietnamese': self.vietnamese,
            'bahnaric': self.bahnaric

        }
    
class NglieuCauTTCS(db.Model):
    __tablename__ = 'TTCS'
    ID = db.Column(db.Integer, primary_key=True)
    vietnamese = db.Column(db.String)
    bahnaric = db.Column(db.String)
    def to_dict(self):
        return{
            'ID': self.ID,
            'vietnamese': self.vietnamese,
            'bahnaric': self.bahnaric

        }
class NglieuCauVHTT(db.Model):
    __tablename__ = 'VHTT'
    ID = db.Column(db.Integer, primary_key=True)
    vietnamese = db.Column(db.String)
    bahnaric = db.Column(db.String)
    def to_dict(self):
        return{
            'ID': self.ID,
            'vietnamese': self.vietnamese,
            'bahnaric': self.bahnaric,

        }
class Vanbancau(db.Model):
    __tablename__ = 'vanbancau'
    ID = db.Column(db.Integer, primary_key=True)
    vietnamese = db.Column(db.String)
    bahnaric = db.Column(db.String)
    def to_dict(self):
        return{
            'ID': self.ID,
            'vietnamese': self.vietnamese,
            'bahnaric': self.bahnaric,

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kinh')
def kinh():
    return render_template('kinh-bahnar.html')

@app.route('/bahnar')
def bahnar():
    return render_template('bahnar-kinh.html')
@app.route('/nglieucauKHKT')
def nglieucauKHKT():
    return render_template('nglieucauKHKT.html')
    
@app.route('/api/nglieucauKHKT')
def data1():
    khkt_query = NglieuCauKHKT.query
    khcn_query = NglieuCauKHCN.query
    ttcs_query = NglieuCauTTCS.query
    vhtt_query = NglieuCauVHTT.query
    vbc_query = Vanbancau.query
    total_records = 0
    
    # search filter
    search_value = request.args.get('search[value]', '')
    if search_value:
        khkt_query = khkt_query.filter(NglieuCauKHKT.vietnamese.like(f'%{search_value}%') | NglieuCauKHKT.bahnaric.like(f'%{search_value}%'))
        khcn_query = khcn_query.filter(NglieuCauKHCN.vietnamese.like(f'%{search_value}%') | NglieuCauKHCN.bahnaric.like(f'%{search_value}%'))
        ttcs_query = ttcs_query.filter(NglieuCauTTCS.vietnamese.like(f'%{search_value}%') | NglieuCauTTCS.bahnaric.like(f'%{search_value}%'))
        vhtt_query = vhtt_query.filter(NglieuCauVHTT.vietnamese.like(f'%{search_value}%') | NglieuCauVHTT.bahnaric.like(f'%{search_value}%'))
        vbc_query = vbc_query.filter(Vanbancau.vietnamese.like(f'%{search_value}%') | Vanbancau.bahnaric.like(f'%{search_value}%'))
        
    # combine results from all four tables
    records_filtered = khkt_query.count() + khcn_query.count() + ttcs_query.count() + vhtt_query.count() + vbc_query.count()
    
    
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    combined_query = khkt_query.union_all(ttcs_query, vhtt_query, khcn_query, vbc_query)
    result = combined_query.offset(start).limit(length).all()

    # data = [record.to_dict() for record in khkt_query] + [record.to_dict() for record in ttcs_query] + [record.to_dict() for record in vhtt_query] + [record.to_dict() for record in khcn_query]

    #response
    return {
        'data': [word.to_dict() for word in result],
        'recordsFiltered': records_filtered,
        'recordsTotal': records_filtered,
        'draw': request.args.get('draw', 1,type=int),
    }

# //////////////////////////////////////////////////////////////
@app.route('/api/kinh')
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
        'recordsTotal': total_filtered,
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/bahnar')
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
        'recordsTotal': total_filtered,
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
    list_files = os.listdir(dirr)
    fn = random.choice(list_files)

    return send_from_directory(dirr, fn)

if __name__ == '__main__':
    app.run(debug=True)
