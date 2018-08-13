import csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import requests
from pager import Pager

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import csv

from cassandra.cluster import Cluster
from flask_cqlalchemy import CQLAlchemy

def read_table(url):
    """Return a list of dict"""
    # r = requests.get(url)
    with open(url) as f:
        return [row for row in csv.DictReader(f.readlines())]


APPNAME = "Fast Fashion Classification"
STATIC_FOLDER = 'example'


app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(
    APPNAME=APPNAME,
    )
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/ILSVRC/Data/DET/test/'

# Set clothing id lookup table
with open('clothing.csv') as f:
    reader = csv.reader(f)
    next(reader)
    clothing_dict = dict(reader)


# Cassandra
app.config['CASSANDRA_HOSTS'] = config.CASS_CLUSTER
app.config['CASSANDRA_KEYSPACE'] = config.KEYSPACE
db = CQLAlchemy(app)

class clothes(db.Model):
    __keyspace__ = config.KEYSPACE
    uid = db.columns.Integer(primary_key=True)
    conf1 = db.columns.Float()
    conf2 = db.columns.Float()
    conf3 = db.columns.Float()
    image = db.columns.Text()
    pred1 = db.columns.Text()
    pred2 = db.columns.Text()
    pred3 = db.columns.Text()

db.sync_db()

table = []
for row in clothes.objects.all():
    row['image'] = os.path.basename(row['image'])
    row_dict = dict(row.items())
    row_dict['pred1'] = clothing_dict[row_dict['pred1']])
    table.append(row_dict)

pager = Pager(len(table))


@app.route('/')
def index():
    return redirect('/0')


@app.route('/<path:filename>')
def img_render(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename, mimetype='image/jpeg')

@app.route('/<int:ind>/')
def image_view(ind=None):
    if ind >= pager.count:
        return render_template("404.html"), 404
    else:
        pager.current = ind
        return render_template(
            'imageview.html',
            index=ind,
            pager=pager,
            data=table[ind])


@app.route('/goto', methods=['POST', 'GET'])
def goto():
    return redirect('/' + request.form['index'])


if __name__ == '__main__':
    app.run(debug=True)
