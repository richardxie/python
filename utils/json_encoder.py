#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import json
from datetime import datetime
  
def new_alchemy_encoder():
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o.__class__, DeclarativeMeta):
                if o in _visited_objs:
                    return None
                _visited_objs.append(o)
                
                data = {}
                fields = o.__json__() if hasattr(o, '__json__') else dir(o)
                for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                        value = o.__getattribute__(field)
                        try:
                            if isinstance(value, datetime):
                                value = value.strftime('%y-%m-%d %H:%M:%S')
                            json.dumps(value)
                            data[field] = value
                        except TypeError:
                            data[field] = None
                return data
            return json.JSONEncoder.default(self, o)
    return AlchemyEncoder