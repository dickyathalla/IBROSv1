from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/i-bros"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
stts = db.Table('table_webgis',db.metadata,autoload = True, autoload_with = db.engine)
print(stts)

        
@app.route('/data/<pesan>', methods=['GET', 'POST'])
def coba(pesan):
    pesanSplt = pesan.split(",")
    insert_data = stts.insert().values(latitude=pesanSplt[0],longitude=pesanSplt[1],created=pesanSplt[2])
    db.session.execute(insert_data) 

    db.session.commit()
    print (pesan)
    return "{}".format (pesan)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)