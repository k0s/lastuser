# -*- coding: utf-8 -*-

import unittest
from lastuserapp import app, db, init_for
from lastuser_core.models import *
from .fixtures import make_fixtures

BOOTSTRAP_MAPPINGS = dict(
    users=dict(_class=User, sequential_properties=dict(username=u"user%s", fullname=u"User %s"), properties=dict())
    )

class BasicTestFixture(unittest.TestCase):
    def setUp(self, bootstrap=dict()):
        init_for('testing')
        app.config['TESTING'] = True
        db.app = app
        db.drop_all()
        db.create_all()
        self.db = db
        self._bootstrap(bootstrap)
        # make_fixtures()

    def _bootstrap(self, bootstrap):
        for obj_name in bootstrap:
            n = bootstrap[obj_name] if obj_name in bootstrap else 0;
            if hasattr(self, obj_name) is False:
                objects = []
            else:
                objects = getattr(self, obj.name)
            for i in range(len(objects), n):
                properties = BOOTSTRAP_MAPPINGS[obj_name]['sequential_properties'].copy()
                for key in properties:
                    properties[key] = properties[key] % str(i)
                properties = dict(properties.items() + BOOTSTRAP_MAPPINGS[obj_name]['properties'].items())
                objects.append(BOOTSTRAP_MAPPINGS[obj_name]['_class'](**properties))
            setattr(self, obj_name, objects)


    def tearDown(self):
        self.db.drop_all()