db = DAL('sqlite://storage.sqlite')

from datetime import datetime

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
	Field('date', 'datetime', default=datetime.utcnow()),
	Field('Author', default=get_id()),
	Field('public', 'boolean', default=True), 
	Field('Instructions','text'),
	Field('ingredients', 'list:string'))


"""Mini database to link recipes and ingredients"""
db.define_table('RecipeNeeds',
    Field('recipe_id'),
    Field('ingredient_id'))

"""Database to combine everything into becoming the user's final shoplist """
db.define_table('ShopList',
	Field('created_on', 'date', default=request.now),
	Field('author', default=get_id()),
	Field('cart', 'list:string', default=[]))
	
db.ShopList.created_on.readable = False
db.ShopList.created_on.writable = True	
db.recipe.Author.readable  = False
db.recipe.Author.writable = False
db.recipe.date.readable  = False
db.recipe.date.writable = False