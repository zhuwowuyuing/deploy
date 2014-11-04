__author__ = 'liangnaihua'

__author__ = 'liangnaihua'

# tutorial/tables.py
import django_tables2 as tables
from models import CheckError

class CheckErrorTable(tables.Table):
    class Meta:
        model = CheckError
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'100%'}
        # attrs = {"class": "table table-bordered"}