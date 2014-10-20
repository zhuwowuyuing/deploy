__author__ = 'liangnaihua'

# tutorial/tables.py
import django_tables2 as tables
from models import *

class ModLogTable(tables.Table):
    class Meta:
        model = ModLog
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'100%'}
        # attrs = {"class": "table table-bordered"}