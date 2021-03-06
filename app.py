import os
from flask import Flask, flash, render_template, redirect, request, \
    session, url_for

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, \
    check_password_hash
import re
if os.path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.context_processor
def get_authors():
    # to populate the navabar authors dropdown box
    authors = list(mongo.db.users.find())

    return dict(authors=authors)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    recipes = list(mongo.db.recipes.find())

    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template('recipes.html', recipes=recipes,
                           this_url=this_url, referer_view=referer_view)


@app.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})

    # these two variables are present in nealy all views and passed to the script file via hidden inputs in the base template.
    # their values are the current url and the preceding. The script compares them and if they are a match it runs the code to avoid page scroll reset.
    # the referer urls is worked out with the get_referer_view

    this_url = request.path
    referer_view = get_referer_view(request)
    print('this urls is', this_url, ' e referer view is ', referer_view)
    # if not referer_view:
    #     referer_view = this_url

    # code to add tags to the recipe, if a user has pressed the Add Tag button

    tagsInput = []
    tags = list(mongo.db.tags.find().sort('tag', 1))
    try:
        tagsFetched = recipe.get('tags')
        tagsInput = list(tagsFetched)
    except:
        tagsFetched = []

    # if the recipe already has tags, remove them form the select box

    try:
        tags = list(mongo.db.tags.find().sort('tag', 1))
        if tagsInput:
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    pass
    except:
        try:
            tags = list(mongo.db.tags.find().sort('tag', 1))
        except:
            tags = []

    # the user has hit the Add Tag button

    if request.method == 'POST' and 'addTagBtn' in request.args:


        if 'recipe_id' in request.args:
            recipe_id = request.args['recipe_id']
        else:
            recipe_id = recipe_id

        pick_tag = request.form.get('pick_tag')
        new_tag = request.form.get('new_tag')

        if pick_tag:
            if pick_tag not in tagsInput:
                tagsInput.append(str(pick_tag))

        if new_tag:
            if new_tag not in tagsInput:
                tagsInput.append(str(new_tag))

        existingTags = list(mongo.db.tags.find().sort('tag', 1))

        existingTagsItems = []
        for tag in existingTags:
            existingTagsItems.append(tag['tag'])

        # Insert the tag in the db if not already existing

        if tagsInput:
            for x in tagsInput:
                strX = str(x)
                tagToAdd = {'tag': strX}
                if not strX in existingTagsItems:
                    
                    mongo.db.tags.insert_one(tagToAdd)
                    tags = list(mongo.db.tags.find().sort('tag', 1))
                    

        mongo.db.recipes.update({'_id': ObjectId(recipe_id)},
                                {'$set': {'tags': tagsInput}})
        recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})

    return render_template('recipe.html', recipe=recipe, tags=tags,
                           this_url=this_url, referer_view=referer_view)


# from Tim Nelson (CI)

@app.route('/register', methods=['GET', 'POST'])
def register():

    this_url = request.path
    referer_view = get_referer_view(request)

    recipe_id = ''

    # save the recipe id if the user clicked the register link on the recipe page(for later redirection)

    try:
        recipe_id = session['fromRecipe_id']
    except:
        session['fromRecipe_id'] = ''

    if 'recipe_id' in request.args:
        recipe_id = request.args['recipe_id']
        session['fromRecipe_id'] = recipe_id

    if request.method == 'POST':

        # check if username already exists in db

        existing_user = \
            mongo.db.users.find_one({'username': request.form.get('usernameReg'
                                                                  ).lower()})

        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))
        else:
            register = {'username': request.form.get('usernameReg'
                                                     ).lower(),
                        'password': generate_password_hash(request.form.get('usernameRegPassword'
                                                                            ))}
            mongo.db.users.insert_one(register)

            # put the new user into 'session' cookie

            session['user'] = request.form.get('usernameReg').lower()
            flash('Registration Successful!')

            # return the user to the recipe page if he clicked the register link from there

            if session['fromRecipe_id']:
                recipe_id = session['fromRecipe_id']
                session.pop('fromRecipe_id')
                return redirect(url_for('recipe', recipe_id=recipe_id,
                                        this_url=this_url,
                                        referer_view=referer_view))
            else:

                return redirect(url_for('profile',
                                        username=session['user']))

    return render_template('register.html', this_url=this_url,
                           referer_view=referer_view)


# from Tim Nelson (CI)

@app.route('/login', methods=['GET', 'POST'])
def login():

    this_url = request.path
    referer_view = get_referer_view(request)

    recipe_id = ''

    # save the recipe id if the user clicked the register link on the recipe page(for later redirection)

    try:
        recipe_id = session['fromRecipe_id']
    except:
        session['fromRecipe_id'] = ''

    if 'recipe_id' in request.args:
        recipe_id = request.args['recipe_id']
        session['fromRecipe_id'] = recipe_id

    if request.method == 'POST':

        # check if username exists in db

        existing_user = \
            mongo.db.users.find_one({'username': request.form.get('username'
                                                                  ).lower()})
        
        if existing_user:

            # ensure hashed password matches user input

            if check_password_hash(existing_user['password'],
                                   request.form.get('password')):
                session['user'] = request.form.get('username').lower()

                flash('Welcome, {}'.format(request.form.get('username'
                                                            )))

                # return the user to the recipe page if he clicked the register link from there

                if session['fromRecipe_id']:
                    recipe_id = session['fromRecipe_id']
                    session.pop('fromRecipe_id')
                    return redirect(url_for('recipe',
                                            recipe_id=recipe_id,
                                            this_url=this_url,
                                            referer_view=referer_view))
                else:
                    return redirect(url_for('profile',
                                            username=session['user'],
                                            this_url=this_url,
                                            referer_view=referer_view))
            else:

                # invalid password match

                flash('Incorrect Username and/or Password')
                return redirect(url_for('login',
                                        this_url=this_url,
                                        referer_view=referer_view))
        else:

            # username doesn't exist

            flash('Incorrect Username and/or Password')
            return redirect(url_for('login',
                                    this_url=this_url,
                                    referer_view=referer_view))

    return render_template('login.html', this_url=this_url,
                           referer_view=referer_view)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args['search']
    recipes = list(mongo.db.recipes.find({'$text': {'$search': query}}))

    this_url = request.path
    referer_view = get_referer_view(request)

    if query == '':

        queryTerm = "You haven\'t entered and search criteria"
    else:
        if recipes == []:
            queryTerm = 'Your search for "' + query \
                + '" returned no results'
        else:
            queryTerm = 'Search results for query : "' + query + '"'
    return render_template('recipes.html', recipes=recipes,
                           queryTerm=queryTerm, this_url=this_url,
                           referer_view=referer_view)


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):

    this_url = request.path
    referer_view = get_referer_view(request)

    # grab the session user's username from db

    username = mongo.db.users.find_one({'username': session['user'
                                                            ]})['username']
    if session['user']:
        recipes = list(mongo.db.recipes.find({'author': username}))

        return render_template('profile.html', username=username,
                               recipes=recipes, this_url=this_url,
                               referer_view=referer_view)


@app.route('/author/<username>', methods=['GET', 'POST'])
def author(username):

    usernameObj = mongo.db.users.find_one({'username': username})
    username = usernameObj['username']

    recipes = list(mongo.db.recipes.find({'author': username}))

    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template('profile.html', username=username,
                           recipes=recipes, this_url=this_url,
                           referer_view=referer_view)


# from Tim Nelson (CI)

@app.route('/logout')
def logout():

    this_url = request.path
    referer_view = get_referer_view(request)

    # remove user from session cookie

    flash('You have been logged out')
    session.pop('user')
    return redirect(url_for('login', this_url=this_url, referer_view=referer_view))


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():

    # check if some tags have been added already

    try:
        tagsInput = session['tagsInput']
    except:
        tagsInput = []

    # get the value of the tag, if entered

    if 'addTagBtn' in request.args:
        pick_tag = request.form.get('pick_tag')
        new_tag = request.form.get('new_tag')

        # if pick_tag != None:

        if pick_tag:
            if pick_tag not in tagsInput:
                tagsInput.append(str(pick_tag))
                session['tagsInput'] = tagsInput

        # if new_tag != None:

        if new_tag:
            if new_tag not in tagsInput:
                tagsInput.append(str(new_tag))
                session['tagsInput'] = tagsInput

    # check if some ingridients have been added already

    try:
        ingridients = session['ingridients']
    except:
        ingridients = []

    # check if the ingridients'name has been added already

    try:
        recipe_name = request.form.get('recipe_name')
        if recipe_name is not None:
            session['recipe_name'] = str(recipe_name)
        else:
            try:
                recipe_name = str(session['recipe_name'])
            except:
                recipe_name = ''
    except:
        recipe_name = ''

    # check if any method steps have been added already

    try:
        steps = session['steps']
    except:
        steps = []

    # if the recipe already has tags, remove them form the select box

    try:
        tags = list(mongo.db.tags.find().sort('tag', 1))
        if tagsInput:
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    pass
    except:
        try:
            tags = list(mongo.db.tags.find().sort('tag', 1))
        except:
            tags = []

    # remove any tag that has been clicked("X" beside the tag)

    if 'delTag' in request.args:
        deltag = request.args['delTag']
        if tagsInput:
            for tag in tagsInput:
                if tag == deltag:
                    tagsInput.remove(tag)

    # restore the removed tag to the select box

            tags = list(mongo.db.tags.find().sort('tag', 1))
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    pass

    # an hidden field, the logged user knows who he is

    try:
        author = request.form.get('author')
    except:
        author = ''

    # variable to be used later, if a user has failed some required fields in the ingredient mini-form

    incomplete_Ing = []

    # clear the form if the user wants to start over

    if 'clear' in request.args:

        clear = request.args['clear']

        if clear:
            try:
                session.pop('ingridients')
                session.pop('steps')
                session.pop('tagsInput')
                ingridients = []
                steps = []
                recipe_name = ''
                recipe_description = ''
                tags = list(mongo.db.tags.find().sort('tag', 1))
                time = ''
                cook_time = ''
                time_notes = ''
                author = ''
                tagsInput = []
                incomplete_Ing = []
            except:
                ingridients = []
                steps = []
                recipe_name = ''
                recipe_description = ''
                tags = list(mongo.db.tags.find().sort('tag', 1))
                time = ''
                cook_time = ''
                time_notes = ''
                author = ''
                tagsInput = []
                incomplete_Ing = []
    else:
        clear = False

    # determine at what point of the ingredients' section the user wants make a new entry

    if 'afterIng' in request.args:
        afterIng = int(request.args['afterIng'])
    else:
        afterIng = 0

    # determine at what point of the ingredients' section the user wants make an amendment

    if 'ing_to_edit' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
    else:
        ing_to_edit = None

    # determine at what point of the method steps' section the user wants make a new entry

    if 'afterStep' in request.args:
        afterStep = int(request.args['afterStep'])
    else:
        afterStep = 0

    # determine at what point of the method steps' section the user wants make an amendment

    if 'step_to_edit' in request.args:
        step_to_edit = int(request.args['step_to_edit'])
    else:
        step_to_edit = 0

    # make the ingredient mini form available if the user clicked the "+" button

    if 'can_add_ing' in request.args:
        afterIng = int(request.args['afterIng'])
        can_add_ing = True
    else:
        can_add_ing = False

    # make the ingredient mini form available if the user clicked the edit button

    if 'edit_ing' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
        edit_ing = True
    else:
        edit_ing = False

    # make the method step mini form available if the user clicked the "+" button

    if 'can_add_step' in request.args:
        afterStep = int(request.args['afterStep'])

        can_add_step = True
    else:
        can_add_step = False

    # make the method step mini form available if the user clicked the edit button

    if 'edit_step' in request.args:
        step_to_edit = int(request.args['step_to_edit'])
        edit_step = True
    else:
        edit_step = False

    # if the the user deleted an ingredient, restore its tag to the selct box, if he hadn't already done manually
    # remove the ingredient so it doesn't appear in the relevant section, update the session variable

    if 'del_ing' in request.args:
        ing_to_del = int(request.args['ing_to_del'])
        if ingridients:
            tagToRemove = str(ingridients[ing_to_del][0])
            if tagToRemove in tagsInput:
                tagsInput.remove(tagToRemove)
            ingridients.pop(ing_to_del)
            session['ingridients'] = list(ingridients)

    # remove the step so it doesn't appear in the relevant section, update the session variable

    if 'del_step' in request.args:
        step_to_del = int(request.args['step_to_del'])
        steps.pop(step_to_del)
        session['steps'] = list(steps)

    # swap the ingredient with the one above or with the last if first, update the session variable

    if 'ingridient_pos_up' in request.args:
        ingridient_pos = request.args['ingridient_pos_up']

        (ingridients[int(ingridient_pos)],
         ingridients[int(ingridient_pos) - 1]) = \
            (ingridients[int(ingridient_pos) - 1],
             ingridients[int(ingridient_pos)])
        session['ingridients'] = list(ingridients)

    # swap the step with the one above or with the last if first, update the session variable

    if 'step_pos_up' in request.args:
        step_pos = request.args['step_pos_up']

        (steps[int(step_pos)], steps[int(step_pos) - 1]) = \
            (steps[int(step_pos) - 1], steps[int(step_pos)])
        session['steps'] = list(steps)

    # swap the ingredient with the one below or with the first if last, update the session variable

    if 'ingridient_pos_down' in request.args:
        ingridient_pos = int(request.args['ingridient_pos_down'])
        len_ingridient_minus_1 = int(len(ingridients)) - 1
        if ingridient_pos == len_ingridient_minus_1:
            (ingridients[int(ingridient_pos)], ingridients[0]) = \
                (ingridients[0], ingridients[int(ingridient_pos)])
        else:

            (ingridients[int(ingridient_pos)],
             ingridients[int(ingridient_pos) + 1]) = \
                (ingridients[int(ingridient_pos) + 1],
                 ingridients[int(ingridient_pos)])
        session['ingridients'] = list(ingridients)

    # swap the step with the one below or with the first if last, update the session variable

    if 'step_pos_down' in request.args:
        step_pos = int(request.args['step_pos_down'])
        len_steps_minus_1 = int(len(steps)) - 1
        if step_pos == len_steps_minus_1:
            (steps[int(step_pos)], steps[0]) = (steps[0],
                                                steps[int(step_pos)])
        else:

            (steps[int(step_pos)], steps[int(step_pos) + 1]) = \
                (steps[int(step_pos) + 1], steps[int(step_pos)])
        session['steps'] = list(steps)

    # process the ingredient mini form subssion,

    if 'add_ingridient' in request.args:

        recipe_name = str(request.form.get('recipe_name'))
        session['recipe_name'] = recipe_name
        recipe_description = str(request.form.get('recipe_description'))
        session['recipe_description'] = recipe_description

        ingredient1 = []

        # ingridient's name, quantity and measure unit are enough to save.
        # insert or update ingredient as appropriate, update session variables

        ingredient1 = request.form.getlist('ingredient1')
        if ingredient1:
            if not ingredient1 in ingridients:
                if ingredient1[0] and ingredient1[1] and ingredient1[2]:
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        ingridients.insert(afterIng + 1, ingredient1)
                    elif 'editIng' in request.args:
                        editIng = int(request.args['editIng'])

                        tagToEdit = str(ingridients[editIng][0])
                        if tagToEdit in tagsInput:
                            tagsInput.remove(tagToEdit)

                        ingridients[editIng] = ingredient1
                    else:
                        ingridients.append(ingredient1)
                    can_add_ing = False
                    edit_ing = False
                    session['ingridients'] = ingridients

                    # the name of the ingridient is automatically added as tag

                    if ingredient1:
                        if not str(ingredient1[0]) in tagsInput:
                            tagsInput.append(str(ingredient1[0]))
                            session['tagsInput'] = tagsInput
                else:

                    # if any of the values of the first 3 fields of the ingredient are missing, re-present the mini form, with any of submitted values prefilled

                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        can_add_ing = True
                        incomplete_Ing = \
                            request.form.getlist('ingredient1')
                    else:
                        incomplete_Ing = \
                            request.form.getlist('ingredient1')
                        edit_ing = True
                        ing_to_edit = int(request.args['editIng'])
        else:
            can_add_ing = False

    # process the step mini form subssion,
    # insert or update step as appropriate, update session variables

    if 'add_step' in request.args:
        step = ''
        step = request.form.get('step')
        if step is not None:
            step = str(request.form.get('step'))
            if step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    steps.insert(afterStep + 1, step)
                elif 'step_to_edit' in request.args:
                    step_to_edit = int(request.args['step_to_edit'])
                    steps[step_to_edit] = step
                else:
                    steps.append(step)
                can_add_step = False
                edit_step = False
                session['steps'] = steps

            # ifthe value is missing, re-present the mini form

            if not step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    can_add_step = True

    # the usual referer and current url values, for JS
    this_url = request.path
    referer_view = get_referer_view(request)
    # the user has clicked the Add Recipe button
    # all the data in the form so far gets saved in a dictionary and pymongo sends it to MongoDB

    if request.method == 'POST' and 'recipe' in request.args:

        recipe = {
            'recipe_name': request.form.get('recipe_name'),
            'recipe_description': request.form.get('recipe_description'
                                                   ),
            'ingridients': ingridients,
            'steps': steps,
            'tags': tagsInput,
            'time': [request.form.get('time'),
                     request.form.get('cook_time'),
                     request.form.get('time_notes')],
            'author': request.form.get('author'),
        }

        # if the user came up with a tag of his own, add it to the MongoDB collection for future use

        existingTags = list(mongo.db.tags.find().sort('tag', 1))

        existingTagsItems = []
        for tag in existingTags:
            existingTagsItems.append(tag['tag'])

        if tagsInput:
            for x in tagsInput:
                strX = str(x)
                tagToAdd = {'tag': strX}
                if not strX in existingTagsItems:
                    mongo.db.tags.insert_one(tagToAdd)

        # collect data about the user and the id of the recipes he posted so far.
        # compare the old and new recipe lists, find the odd one out, it's the one that augmeted the list with this new recipe, redirect to this last recipe page

        thisRecipeAuthor = request.form.get('author')
        recipeIDsSoFar = []
        UserRecipesSoFar = \
            list(mongo.db.recipes.find({'author': thisRecipeAuthor}))
        for x in UserRecipesSoFar:
            recipeIDsSoFar.append(str(ObjectId(x['_id'])))

        session['ingridients'] = list(ingridients)
        session['steps'] = list(steps)
        mongo.db.recipes.insert_one(recipe)
        NewUserRecipeIDs = []
        LastID = ''
        recipesWithNew = \
            list(mongo.db.recipes.find({'author': thisRecipeAuthor}))
        for x in recipesWithNew:
            NewUserRecipeIDs.append(str(ObjectId(x['_id'])))
        strLastID = ''
        for x in NewUserRecipeIDs:
            if not x in recipeIDsSoFar:
                LastID = x
                strLastID = str(LastID)

        flash('Recipe Successfully Added')
        session.pop('ingridients')
        session.pop('steps')
        session.pop('tagsInput')
        return redirect(url_for('recipe', recipe_id=LastID))

    return render_template(
        'add_recipe.html',
        this_url=this_url,
        referer_view=referer_view,
        ingridients=ingridients,
        tagsInput=tagsInput,
        steps=steps,
        tags=tags,
        can_add_ing=can_add_ing,
        edit_step=edit_step,
        edit_ing=edit_ing,
        ing_to_edit=ing_to_edit,
        author=author,
        afterIng=afterIng,
        can_add_step=can_add_step,
        step_to_edit=step_to_edit,
        afterStep=afterStep,
        clear=clear,
        incomplete_Ing=incomplete_Ing,
    )


@app.route('/edit_recipe', methods=['GET', 'POST'])
def edit_recipe():

    # prefill form with the existing recipe data

    if 'recipe_id' in request.args:
        time = ''
        cook_time = ''
        time_notes = ''
        recipe_id = request.args['recipe_id']
        session['recipe_id'] = recipe_id
        recipeToEdit = \
            mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
        tags = list(mongo.db.tags.find().sort('tag', 1))

        recipe_nameFetched = recipeToEdit.get('recipe_name')
        recipe_descriptionFetched = \
            recipeToEdit.get('recipe_description')
        timeFetched = recipeToEdit.get('time')

        recipe_name = recipe_nameFetched
        recipe_description = recipe_descriptionFetched
        try:
            time = timeFetched[0]
        except:
            pass

        try:
            cook_time = timeFetched[1]
        except:
            pass

        try:
            time_notes = timeFetched[2]
        except:
            pass

        ingridientsFetched = recipeToEdit.get('ingridients')
        stepsFetched = recipeToEdit.get('steps')
        tagsFetched = recipeToEdit.get('tags')

        session['ingridients'] = ingridientsFetched
        session['steps'] = stepsFetched
        session['tagsInput'] = tagsFetched
        ingridients = session['ingridients']
        steps = session['steps']
        tagsInput = session['tagsInput']

        this_url = request.path
        referer_view = get_referer_view(request)

        return render_template(
            'edit_recipe.html',
            this_url=this_url,
            referer_view=referer_view,
            recipe=recipeToEdit,
            tags=tags,
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            time=time,
            cook_time=cook_time,
            time_notes=time_notes,
            recipe_id=recipe_id,
            ingridients=ingridients,
            steps=steps,
            tagsInput=tagsInput,
        )

    # to be used later to update the collection document

    try:
        recipe_id = session['recipe_id']
    except:
        recipe_id = ''

    # check if some tags have been added already

    try:
        tagsInput = session['tagsInput']
    except:

        tagsInput = []

    # extra_Ing = False

    if 'addTagBtn' in request.args:
        pick_tag = request.form.get('pick_tag')
        new_tag = request.form.get('new_tag')

        # if pick_tag != None:

        if pick_tag:
            if pick_tag not in tagsInput:
                tagsInput.append(str(pick_tag))
                session['tagsInput'] = tagsInput

        # if new_tag != None:

        if new_tag:
            if new_tag not in tagsInput:
                tagsInput.append(str(new_tag))
                session['tagsInput'] = tagsInput

    # check if some ingridients have been added already

    try:
        ingridients = session['ingridients']
    except:
        ingridients = []

    # check if the ingridients'name has been added already

    try:
        recipe_name = request.form.get('recipe_name')
        if recipe_name is not None:
            session['recipe_name'] = str(recipe_name)
        else:
            try:
                recipe_name = str(session['recipe_name'])
            except:
                recipe_name = ''
    except:
        recipe_name = ''

    # check if any method steps have been added already

    try:
        steps = session['steps']
    except:
        steps = []

    # if the recipe already has tags, remove them form the select box

    try:
        tags = list(mongo.db.tags.find().sort('tag', 1))
        if tagsInput:
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    pass
    except:

        try:
            tags = list(mongo.db.tags.find().sort('tag', 1))
        except:
            tags = []

    # remove any tag that has been clicked("X" beside the tag)

    if 'delTag' in request.args:
        deltag = request.args['delTag']
        if tagsInput:
            for tag in tagsInput:
                if tag == deltag:
                    tagsInput.remove(tag)

            tags = list(mongo.db.tags.find().sort('tag', 1))
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    pass

    # an hidden field, the logged user knows who she is

    try:
        author = request.form.get('author')
    except:
        author = ''

    # variable to be used later, if a user has failed some required fields in the ingredient mini-form

    incomplete_Ing = []

    # clear the form if the user wants to start over

    if 'clear' in request.args:

        clear = request.args['clear']

        if clear:
            try:
                session.pop('ingridients')
                session.pop('steps')
                session.pop('tagsInput')
                ingridients = []
                steps = []
                recipe_name = ''
                recipe_description = ''
                tags = list(mongo.db.tags.find().sort('tag', 1))
                time = ''
                cook_time = ''
                time_notes = ''
                author = ''
                tagsInput = []
                incomplete_Ing = []
            except:
                ingridients = []
                steps = []
                recipe_name = ''
                recipe_description = ''
                tags = list(mongo.db.tags.find().sort('tag', 1))
                time = ''
                cook_time = ''
                time_notes = ''
                author = ''
                tagsInput = []
                incomplete_Ing = []
    else:
        clear = False

    # determine at what point of the ingredients' section the user wants make a new entry

    if 'afterIng' in request.args:
        afterIng = int(request.args['afterIng'])
    else:
        afterIng = 0

    # determine at what point of the ingredients' section the user wants make an amendment

    if 'ing_to_edit' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
    else:
        ing_to_edit = None

     # determine at what point of the method steps' section the user wants to make a new entry

    if 'afterStep' in request.args:
        afterStep = int(request.args['afterStep'])
    else:
        afterStep = 0

    # determine at what point of the method steps' section the user wants make an amendment

    if 'step_to_edit' in request.args:
        step_to_edit = int(request.args['step_to_edit'])
    else:
        step_to_edit = 0

    # make the ingredient mini form available if the user clicked the "+" button

    if 'can_add_ing' in request.args:
        afterIng = int(request.args['afterIng'])
        can_add_ing = True
    else:
        can_add_ing = False

     # make the ingredient mini form available if the user clicked the edit button

    if 'edit_ing' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
        edit_ing = True
    else:
        edit_ing = False

     # make the method step mini form available if the user clicked the "+" button

    if 'can_add_step' in request.args:
        afterStep = int(request.args['afterStep'])
        can_add_step = True
    else:
        can_add_step = False

     # make the method step mini form available if the user clicked the edit button

    if 'edit_step' in request.args:
        step_to_edit = int(request.args['step_to_edit'])
        edit_step = True
    else:

        edit_step = False

    # if the the user deleted an ingredient, restore its tag to the select box, if she hadn't already done manually
    # remove the ingredient so it doesn't appear in the relevant section, update the session variable

    if 'del_ing' in request.args:
        ing_to_del = int(request.args['ing_to_del'])
        if ingridients:
            tagToRemove = str(ingridients[ing_to_del][0])
            if tagToRemove in tagsInput:
                tagsInput.remove(tagToRemove)
            ingridients.pop(ing_to_del)
            session['ingridients'] = list(ingridients)

    # remove the step so it doesn't appear in the relevant section, update the session variable

    if 'del_step' in request.args:
        step_to_del = int(request.args['step_to_del'])
        steps.pop(step_to_del)
        session['steps'] = list(steps)

    # swap the ingredient with the one above or with the last if first, update the session variable

    if 'ingridient_pos_up' in request.args:
        ingridient_pos = request.args['ingridient_pos_up']

        (ingridients[int(ingridient_pos)],
         ingridients[int(ingridient_pos) - 1]) = \
            (ingridients[int(ingridient_pos) - 1],
             ingridients[int(ingridient_pos)])
        session['ingridients'] = list(ingridients)

    # swap the step with the one above or with the last if first, update the session variable

    if 'step_pos_up' in request.args:
        step_pos = request.args['step_pos_up']

        (steps[int(step_pos)], steps[int(step_pos) - 1]) = \
            (steps[int(step_pos) - 1], steps[int(step_pos)])
        session['steps'] = list(steps)

    # swap the ingredient with the one below or with the first if last, update the session variable

    if 'ingridient_pos_down' in request.args:
        ingridient_pos = int(request.args['ingridient_pos_down'])
        ingridient_pos_minus_1 = int(ingridient_pos) - 1
        len_ingridient_minus_1 = int(len(ingridients)) - 1
        if ingridient_pos == len_ingridient_minus_1:
            (ingridients[int(ingridient_pos)], ingridients[0]) = \
                (ingridients[0], ingridients[int(ingridient_pos)])
        else:

            (ingridients[int(ingridient_pos)],
             ingridients[int(ingridient_pos) + 1]) = \
                (ingridients[int(ingridient_pos) + 1],
                 ingridients[int(ingridient_pos)])
        session['ingridients'] = list(ingridients)

    # swap the step with the one below or with the first if last, update the session variable

    if 'step_pos_down' in request.args:
        step_pos = int(request.args['step_pos_down'])
        step_pos_minus_1 = int(step_pos) - 1
        len_steps_minus_1 = int(len(steps)) - 1
        if step_pos == len_steps_minus_1:
            (steps[int(step_pos)], steps[0]) = (steps[0],
                                                steps[int(step_pos)])
        else:

            (steps[int(step_pos)], steps[int(step_pos) + 1]) = \
                (steps[int(step_pos) + 1], steps[int(step_pos)])
        session['steps'] = list(steps)

    # process the ingredient mini form subssion,

    if 'add_ingridient' in request.args:

        recipe_name = str(request.form.get('recipe_name'))
        session['recipe_name'] = recipe_name
        recipe_description = str(request.form.get('recipe_description'))
        session['recipe_description'] = recipe_description

        ingredient1 = []

        # ingridient's name, quantity and measure unit are enough to save.
        # insert or update ingredient as appropriate, update session variables

        ingredient1 = request.form.getlist('ingredient1')
        if ingredient1:
            if not ingredient1 in ingridients:
                if ingredient1[0] and ingredient1[1] and ingredient1[2]:
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        ingridients.insert(afterIng + 1, ingredient1)
                    elif 'editIng' in request.args:
                        editIng = int(request.args['editIng'])

                        tagToEdit = str(ingridients[editIng][0])
                        if tagToEdit in tagsInput:
                            tagsInput.remove(tagToEdit)

                        ingridients[editIng] = ingredient1
                    else:
                        ingridients.append(ingredient1)
                    can_add_ing = False
                    edit_ing = False
                    session['ingridients'] = ingridients

                    # the name of the ingridient is automatically added as tag

                    if ingredient1:
                        if not str(ingredient1[0]) in tagsInput:
                            tagsInput.append(str(ingredient1[0]))
                            session['tagsInput'] = tagsInput
                else:

                    # if any of the values of the first 3 fields of the ingredient are missing, re-present the mini form, with any of submitted values prefilled

                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        can_add_ing = True
                        incomplete_Ing = \
                            request.form.getlist('ingredient1')
                    else:
                        incomplete_Ing = \
                            request.form.getlist('ingredient1')
                        edit_ing = True
                        ing_to_edit = int(request.args['editIng'])
        else:
            can_add_ing = False

    # process the step mini form subssion,
    # insert or update step as appropriate, update session variables

    if 'add_step' in request.args:
        step = ''
        step = request.form.get('step')
        if step is not None:
            step = str(request.form.get('step'))
            if step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    steps.insert(afterStep + 1, step)
                elif 'step_to_edit' in request.args:
                    step_to_edit = int(request.args['step_to_edit'])
                    steps[step_to_edit] = step
                else:
                    steps.append(step)
                can_add_step = False
                edit_step = False
                session['steps'] = steps

            # if the value is missing, re-present the mini form

            if not step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    can_add_step = True

    # the usual current url and referer values, for JS

    this_url = request.path
    referer_view = get_referer_view(request)

    # the user has clicked the Edit Recipe button
    # all the data in the form so far gets saved in a dictionary and pymongo sends it to MongoDB

    if request.method == 'POST' and 'editRecipe' in request.args:

        editRecipe = {
            'recipe_name': request.form.get('recipe_name'),
            'recipe_description': request.form.get('recipe_description'
                                                   ),
            'ingridients': ingridients,
            'steps': steps,
            'tags': tagsInput,
            'time': [request.form.get('time'),
                     request.form.get('cook_time'),
                     request.form.get('time_notes')],
            'author': request.form.get('author'),
        }

        # if the user came up with a tag of his own, add it to the MongoDB collection for future use

        existingTags = list(mongo.db.tags.find().sort('tag', 1))
        existingTagsItems = []
        for tag in existingTags:
            existingTagsItems.append(tag['tag'])

        if tagsInput:
            for x in tagsInput:
                strX = str(x)
                tagToAdd = {'tag': strX}
                if not strX in existingTagsItems:
                    mongo.db.tags.insert_one(tagToAdd)

        mongo.db.recipes.update({'_id': ObjectId(recipe_id)},
                                editRecipe)
        session.pop('ingridients')
        session.pop('steps')
        session.pop('tagsInput')
        session.pop('recipe_id')

        flash('Recipe Successfully Updated')

        # redirect to the recipe's page

        return redirect(url_for('recipe', recipe_id=recipe_id))

    return render_template(
        'edit_recipe.html',
        this_url=this_url,
        referer_view=referer_view,
        ingridients=ingridients,
        recipe_id=recipe_id,
        tagsInput=tagsInput,
        steps=steps,
        tags=tags,
        can_add_ing=can_add_ing,
        edit_step=edit_step,
        edit_ing=edit_ing,
        ing_to_edit=ing_to_edit,
        author=author,
        afterIng=afterIng,
        can_add_step=can_add_step,
        step_to_edit=step_to_edit,
        afterStep=afterStep,
        clear=clear,
        incomplete_Ing=incomplete_Ing,
    )


# (Copyright (c) 2009 Arthur Furlan <arthur.furlan@gmail.com>)

def get_referer_view(request, default='..fail'):
    '''
    Return the referer view of the current request
    Example:
        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar

    referer = request.referrer
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    # leave it cornflakes, this is grand.

    referer = re.sub('^https:\/\/', '', referer).split('/')

    # add the slash at the relative path's view and finished

    referer = u'/' + u'/'.join(referer[1:])
    referer = referer.split('?')[0]
    try:
        referer = referer.split('cocktails-flask.herokuapp.com')[1]
    except:
        pass
    return referer


@app.route('/delete_recipe/<recipe_id>/<username>', methods=['GET',
                                                             'POST'])
def delete_recipe(recipe_id, username):
    recipeToDelete = \
        mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe Successfully Deleted')
    username = mongo.db.users.find_one({'username': username})
    return redirect(url_for('profile', username=username))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT'
                                                               )), debug=True)
