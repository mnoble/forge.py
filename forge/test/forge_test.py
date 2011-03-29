from unittest2 import TestCase

import forge.test.factories
from forge import Forge, DuplicateFactoryError


class ForgeTest(TestCase):
    def setUp(self):
        Forge.configure(models=None)
        if 'user' not in Forge._registry:
            Forge.define('user', name='Matte', age=25)
    
    def should_respond_to_define(self):
        assert callable(Forge.define)
    
    def should_define_factories(self):
        assert 'user' in Forge._registry
    
    def should_not_allow_duplicate_factory_names(self):
        with self.assertRaises(DuplicateFactoryError):
            Forge.define('user', color='red')
    
    def should_build_plain_factories(self):
        user = Forge.build('user')
        assert user.name == 'Matte'
    
    def should_allow_custom_attributes_when_building(self):
        user = Forge.build('user', name='Fred')
        assert user.name == 'Fred'
    
    def should_support_with_context_format(self):
        with Forge.define('pet') as p:
            p.breed = 'Husky'
        assert Forge._registry['pet'] == {'breed': 'Husky'}
    
    def should_create_associations(self):
        Forge.define('car', owner=Forge.build('user'))
        assert Forge.build('car').owner.name == 'Matte'
    
    def should_return_new_objects_via_build(self):
        admin = Forge.build('user')
        user  = Forge.build('user')
        admin.name = 'Pete'
        assert user.name != 'Pete'
    
    def should_make_factories_availabe_on_load(self):
        # At the top: `import forge.test.factories`
        assert Forge._registry['color'] == {'name': 'Red'}
    
    def should_support_shorthand_building(self):
        user = Forge('user')
        assert user.name == 'Matte'
    
    def should_support_shorhand_building_with_attributes(self):
        user = Forge('user', name='Wayne')
        assert user.name == 'Wayne'
