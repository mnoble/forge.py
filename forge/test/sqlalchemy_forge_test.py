from unittest2 import TestCase

import forge
from forge import Forge, DuplicateFactoryError
from forge.test.support.models import User


class SQLAlchemyForgeTest(TestCase):
    def setUp(self):
        Forge.clear()
        Forge.configure(models='forge.test.support.models')
        Forge.define('user', name='Matte')
    
    def should_have_model_module_configurable(self):
        assert Forge._models == forge.test.support.models
    
    def should_create_build_objects_using_models(self):
        user = Forge.build('user')
        assert isinstance(user, User)
    
    def should_have_a_table_object(self):
        user = Forge.build('user')
        assert user.__table__ is not None