__author__ = 'liangnaihua'

# tutorial/tables.py
import django_tables2 as tables
from models import *
from django_tables2.utils import Accessor

class StatusTable(tables.Table):
    class Meta:
        model = Status
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'100%'}

    status = tables.LinkColumn('status_edit', kwargs={"id": Accessor('id')})

class ModLogTable(tables.Table):
    class Meta:
        model = ModLog
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'100%'}
        # attrs = {"class": "table table-bordered"}

class TypeTable(tables.Table):
    class Meta:
        model = Type
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'100%'}

    name = tables.LinkColumn('type_edit', kwargs={"id": Accessor('id')})

class SubtypeTable(tables.Table):
    class Meta:
        model = Subtype
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'100%'}

    name = tables.LinkColumn('subtype_edit', kwargs={"id": Accessor('id')})