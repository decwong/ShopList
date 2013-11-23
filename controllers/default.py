# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
	create_shoplist()
	return dict()

def addRecipe():
	if auth.user == None:
		redirect (URL('index'))
	else:
		form = SQLFORM(db.recipe)
		if form.process().accepted:
			response.flash = 'recipe created'
			redirect (URL('recipes'))
		return dict(form=form)
	
def create_shoplist():
	check = db(db.ShopList.author == auth.user_id).select().first()
	if check:
		current_user = db(db.ShopList.author.contains(auth.user_id))
	else:
		response.flash = 'no shopping list, creating for user'
		success = db.ShopList.insert(author=auth.user_id)
	##db.ShopList.insert()"""
	
def viewRecipe():
	if auth.user == None:
		redirect (URL('index'))
	else:
		q = db.recipe.Author == auth.user_id
		grid = SQLFORM.grid(q, csv=False)
		grid.element('.web2py_counter', replace=None)
		return dict(grid=grid)
		
def recipes():
	if auth.user == None:
		redirect (URL('index'))
	else:
		if request.args(0) != None:
			check = db(db.recipe.id == request.args(0)).select().first()
			query = db(db.ShopList.author == auth.user_id).select().first()
			if check != None:
				query.cart = query.cart + check.ingredients
				query.cart = list(set(query.cart))
				response.flash = query.cart
				query.update_record()
		q = db.recipe.publics == True
		grid = SQLFORM.grid(q, searchable=True, fields=[db.recipe.title, db.recipe.email], create=False, user_signature=False, editable=False, deletable=False,
		csv=False,
		links=[dict(header=T('Add to Cart'),
		body=lambda r: A('Add', _class='btn',
		_href=URL('default', 'recipes', args=[r.id])))])
		grid.element('.web2py_counter', replace=None)
		return dict(grid=grid)

def add_to_list():
	if auth.user == None:
		redirect (URL('index'))
		return dict()

def addIngredients():
	if auth.user == None:
		redirect (URL('index'))
    	return dict()

def ingredients():
	if auth.user == None:
		redirect (URL('index'))
	else:
		if request.args(0) != None:
			check = db(db.ingredients.id == request.args(0)).select().first()
			query = db(db.ShopList.author == auth.user_id).select().first()
			if check != None:
				query.cart = query.cart + check.ingredients
				query.cart = list(set(query.cart))
				response.flash = query.cart
				query.update_record()
		grid = SQLFORM.grid(db.ingredients, searchable=True, fields=[db.ingredients.ingredient], create=False, details=False, user_signature=False, editable=False, deletable=False,
		csv=False,
		links=[dict(header=T('Add to Cart'),
		body=lambda r: A('Add', _class='btn',
		_href=URL('default', 'ingredients', args=[r.id])))])
		grid.element('.web2py_counter', replace=None)
		return dict(grid=grid)

def shoplist():
	if auth.user == None:
		redirect (URL('index'))
	else:
		q = db.ShopList.author == auth.user_id
		q2 = db(q).select().first()
		#response.flash = q2.cart
		grid = SQLFORM.factory(
			Field('ingredient_list', 'list:string', default = q2.cart))
	
		##grid = SQLFORM.grid(q, searchable=True, fields=[db.ShopList.cart], create=False, user_signature=False, editable=False, deletable=False,
		##	csv=False)
		return dict(grid=grid)

def support():
    form = SQLFORM(db.Support)
    return dict(form=form)

def user():
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
