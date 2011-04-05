import imp
import os
import glob
from os.path import basename
from forge.open_struct import OpenStruct

__all__ = ["Forge", "DuplicateFactoryError"]


class DuplicateFactoryError(Exception):
    def __str__(self):
        return "Cannot define two factories with the same name."


class ForgeModelError(Exception):
    def __str__(self):
        return "No model module specified. Use Forge.configure to do so."


class Forge(object):
    """Factory based object forger."""
    
    # Collection of factories created via `define`
    _registry = dict()
    
    # Module to fetch models from
    _models = None
    
    def __new__(self, _name, **kwargs):
        """Build a factory object.
        
        Builds an object using the attributes from the `_name` factory.
        
        **Parameters**:
            * `_name`:  Name of the factory to build
            * `kwargs`: Attributes to override the default factory ones with.
        
        **Example**:
        ::
            Forge.define('user', name='Matte')
            
            user = Forge('user')
            user.name #=> 'Matte'
            
            user = Forge('user', name='Peope')
            user.name #=> 'Peope'
        """
        factory = Forge._registry[_name].copy()
        factory.update(kwargs)
        
        if Forge._models is not None:
            klass = getattr(Forge._models, _name.capitalize())
            return klass(**factory)
        else:
            raise ForgeModelError
    
    @classmethod
    def configure(cls, models=None):
        """Configure Forge to use model classes when building.
        
        Within the module you configure here, classes should be
        available to import. This means that if you have a models
        directory with a ton of model files within, you need to
        make sure `lib/models/__init__.py` makes those classes 
        available to import via `from lib.models import Model`.
        
        **Parameters**:
            models: Module where models reside, in string form
        
        **Example**:
        ::
            Forge.configure(models='app.model')
        """
        if models is not None:
            models = __import__(models, {}, {}, models)
        
        cls._models = models
    
    @classmethod
    def clear(cls):
        cls._registry = {}
    
    class define(object):
        """Defines a factory with default attributes.
        
        **Parameters**:
            * `_name`:  Name representing the factory you're defining.
            * `kwargs`: Default attributes to set when building this factory.
        
        **Example**:
        ::
            # Forge.define as a method:
            Forge.define('user', name='Frankenstein')
            
            # Forge.define using `with`
            with Forge.generate('user') as f:
                f.name = 'Frankenstein'
        """
        def __init__(self, _name, **kwargs):
            self.name = _name
            
            if _name in Forge._registry:
                raise DuplicateFactoryError
            
            Forge._registry[_name] = dict(**kwargs)
        
        def __enter__(self):
            self.factory = OpenStruct(**Forge._registry[self.name])
            return self.factory
        
        def __exit__(self, type, value, tb):
            Forge._registry[self.name] = self.factory.__dict__
    
    @classmethod
    def attributes_for(self, _name):
        return Forge._registry[_name]
    
    @classmethod
    def build(cls, _name, **kwargs):
        """Same as :func:`forge.Forge.__new__`"""
        return Forge(_name, **kwargs)
