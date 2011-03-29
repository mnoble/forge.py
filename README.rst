.. Forge documentation master file, created by
   sphinx-quickstart on Tue Mar 29 14:24:40 2011.
   You can adapt this file completely to your liking, but it should at  least contain the root `toctree` directive.

Forge - Object forging for unit tests
=====================================

Forge will create objects based on factory data. It should be
used when you don't want a database, ie. unit tests, but want
fully fleshed objects that act like database objects.

Getting Started
---------------

Project Setup
+++++++++++++

To keep things organized, I recommend creating a ``test/factories`` directory where all of your factory files will go. For example
::
    project
    '- test
       '- factories
          |- __init__.py
          |- user.py
          |- post.py
          `- comment.py


Defining Factories
++++++++++++++++++

We'll use the ``user.py`` factory from above for example. There are two ways to define a factory. The first is just a normal method call to :func:`forge.Forge.define`:
::
    # project/test/factories/user.py
    
    from forge import Forge
    Forge.define('user', name='Guy')

The other is using the ``with`` syntax:
::
    # project/test/factories/user.py
    
    from forge import Forge
    with Forge.define('user') as f:
        f.name     = 'Guy'
        f.age      = 25
        f.login    = "personguy"
        f.email    = "person@example.com"
        f.password = "testing"

My suggestion is to use the normal syntax when defining a small factory. Essentially, when the definition can fit on one line. Use the ``with`` syntax when setting a large number of default attributes. Putting each attribute on it's own line mirrors how models are declared and makes it easy to quickly grock a Model and it's matching Factory.


Building Forged Objects
+++++++++++++++++++++++

Building factory objects is easy; just call :func:`forge.Forge.build` with the factory name.
::
    user = Forge.build('user')

You can also use the shorthand version:
::
    user = Forge('user')


Associations
++++++++++++

No magic here, just set an attribute to another Forged object:
::
    Forge.define('car', owner=Forge('user'))


Bringing It All Together
++++++++++++++++++++++++

In ``project/test/factories/__init__.py``, import all your other factories, so you won't have to later in your tests:
::
  # project/test/factories/__init__.py
  
  import user, post, comment

Now, in your unit tests:
::
    # project/test/user_test.py
    
    import project.test.factories
    from forge import Forge

    class UserTest(TestCase):
        def setUp(self):
            self.user = Forge('user')
        
        def test_users_name_is_guy(self):
            assert self.user.name == 'Guy'
