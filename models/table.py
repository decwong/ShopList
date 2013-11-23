if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

from datetime import datetime

def get_name():
    if auth.user:
        return auth.user.first_name
    else:
        return 'None'


def get_id():
    if auth.user:
        return auth.user_id
    else:
        return 'None'

def get_email():
    if auth.user :
        return auth.user.email
    else:
        return 'None'
        
"""Database of ingredients:
    - Derive specific ingredients from one of the food groups"""
db.define_table('recipe',
	Field('title'),
	Field('email', default=get_email()),
	Field('dates', 'datetime', default=datetime.utcnow()),
	Field('Author', default=get_id()),
	Field('publics', 'boolean', default=True), 
	Field('Instructions','text'),
	Field('ingredients', 'list:string'))

db.define_table('foodGroup',
    Field('category'))

"""Mini database to of ingredients"""
db.define_table('ingredients',
    Field('ingredient'),
    Field('category_id', 'reference foodGroup'))

"""Mini database to link recipes and ingredients"""
db.define_table('RecipeNeeds',
    Field('recipe_id'),
    Field('ingredient_id'))

"""Database to combine everything into becoming the user's final shoplist """
db.define_table('ShopList',
	Field('created_on', 'date', default=request.now),
	Field('author', default=get_id()),
	Field('cart', 'list:string', default=[]))

db.define_table('Support',
    Field('name', default=get_name()),
    Field('email', default=get_email()),
    Field('Title'),
    Field('comments', 'text'))

db.ShopList.created_on.readable = False
db.ShopList.created_on.writable = True	
db.recipe.Author.readable  = False
db.recipe.Author.writable = False
db.recipe.dates.readable  = False
db.recipe.dates.writable = False
db.Support.email.writable  = False
db.Support.name.writable = False