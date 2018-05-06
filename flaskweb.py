#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
import os
from flask import Flask,request,render_template
ap = Flask(__name__)


@ap.route('/')
def index():

    return render_template('exec2all.html')


@ap.route('/mme/')
def mme():
    os.system("python webpy.py saegw \"cat test/saegwkpi | awk -F ' '  '{print$2}' |grep -e \"20..\-\" -e \"PgwS5ModifyBearer\" | grep -B 2 'PgwS5ModifyBearerFR'\" > tmp.web")

    return render_template('table.html')



if __name__ == '__main__':
    ap.run(debug=True,host='0.0.0.0')

