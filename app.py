import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import re
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.context_processor
def get_authors():

    authors = list(mongo.db.users.find())

    return dict(authors=authors)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    
    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template("recipes.html", recipes=recipes, this_url=this_url, referer_view=referer_view)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template("recipe.html", recipe=recipe, this_url=this_url, referer_view=referer_view)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("usernameReg").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        else:
            register = {
                "username": request.form.get("usernameReg").lower(),
                "password": generate_password_hash(request.form.get("usernameRegPassword"))
            }
            mongo.db.users.insert_one(register)

            # put the new user into 'session' cookie
            session["user"] = request.form.get("usernameReg").lower()
            flash("Registration Successful!")
            return redirect(url_for(
                            "profile", username=session["user"]))
    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template("register.html", this_url=this_url, referer_view=referer_view)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template("login.html", this_url=this_url, referer_view=referer_view)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args['search']
    print('query ', query)
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))

    this_url = request.path
    referer_view = get_referer_view(request)

    if query == "":
        
        queryTerm = "You haven\'t entered and search criteria"
    else:
        if recipes== []:
            queryTerm = "Your search for \"" + query + "\" returned no results"
        else:   
        # prefixText = "Search results for query: "
            queryTerm =  'Search results for query : \"' + query + '\"'
    return render_template("recipes.html", recipes=recipes, queryTerm=queryTerm, this_url=this_url, referer_view=referer_view)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db

    this_url = request.path
    referer_view = get_referer_view(request)

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        recipes = list(mongo.db.recipes.find({"author": username}))

        return render_template("profile.html", username=username, recipes=recipes, this_url=this_url, referer_view=referer_view)


@app.route("/author/<username>", methods=["GET", "POST"])
def author(username):

    usernameObj = mongo.db.users.find_one({"username": username})
    username = usernameObj['username']

    recipes = list(mongo.db.recipes.find({"author": username}))

    
    this_url = request.path
    referer_view = get_referer_view(request)

    return render_template("profile.html", username=username, recipes=recipes, this_url=this_url, referer_view=referer_view)


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():

    try:
        tagsInput = session['tagsInput']
    except:
        tagsInput = []

    extra_Ing = False
    # try:
    #     tagsInput = request.form.getlist("tagsInput")
    # #     print('tagsInput ', tagsInput)
    # except:
    #     tagsInput = []
    # #     print('tagsInput vuoto')

    if 'addTagBtn' in request.args:
        print('ok addTagBtn ce  ')
        pick_tag = request.form.get("pick_tag")
        new_tag = request.form.get("new_tag")

        print('e pure pick_tag ce  ', pick_tag)
        if pick_tag != None:
            if pick_tag not in tagsInput:
                tagsInput.append(str(pick_tag))
                print('tagsInput ', tagsInput)
                session['tagsInput'] = tagsInput

        print('e pure new_tag ci ha sta  ', new_tag)
        if new_tag != None:
            if new_tag not in tagsInput:
                tagsInput.append(str(new_tag))
                print('tagsInput e newtag', tagsInput, new_tag)
                session['tagsInput'] = tagsInput

    try:
        ingridients = session['ingridients']
    except:
        ingridients = []

    try:
        recipe_name = request.form.get("recipe_name")
        if recipe_name is not None:
            session['recipe_name'] = str(recipe_name)
            # recipe_name = str(session['recipe_name'])
        else:
            try:
                recipe_name = str(session['recipe_name'])
            except:
                recipe_name = ""
    except:
        recipe_name = ""

    # recipe_description = "la batosta dal python"

    # try:
    #     recipe_description = request.form.get("recipe_description")
    #     print('recipe_description, ', recipe_description)
    #     if recipe_description is not None:
    #         session['recipe_description']= str(recipe_description)
    #         print('e recipe_description, ', str(session['recipe_description']))
    #         # recipe_name = str(session['recipe_name'])
    #     else:
    #         try:
    #             recipe_description = str(session['recipe_description'])
    #             print('e lo prendi o no sto session, ', recipe_description , 'essendo chista a session', str(session['recipe_description']))
    #         except:
    #             recipe_description = ""
    # except:
    #     recipe_description = ""

    try:
        steps = session['steps']
    except:
        steps = []
    try:
        tags = list(mongo.db.tags.find().sort("tag", 1))
        # tags = list(mongo.db.tags.find({}, {tags.tag: 1}).sort("tag", 1))
        if tagsInput:
            for tag in tags:
                if tag['tag'] in tagsInput:
                    print('effetivamnete ce ', tag['tag'])
                    tags = [i for i in tags if i != tag]
                    # tags.remove(index(tag['tag'])
                else:
                    print(tag['tag'], 'not included')
        # print('quel che rimane de tags ', tags)

        # tags = list(mongo.db.tags.find())
    except:
        try:
            tags = list(mongo.db.tags.find().sort("tag", 1))
        except:
            tags = []
            print('try tagd ha fallito')

    if 'delTag' in request.args:
        deltag = request.args['delTag']
        if tagsInput:
            for tag in tagsInput:
                if tag == deltag:
                    print('found deltag', deltag)
                    tagsInput.remove(tag)
                    # tags = list(mongo.db.tags.find().sort("tag", 1))
                    # tags.append(tag)

                    print('le tags a questo punto ', tags)
            tags = list(mongo.db.tags.find().sort("tag", 1))
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    print('quel che rimane de tags DE NOVO ', tags)

    # try:
    #     time = request.form.get("time")
    # except:
    #     time = ""
    # try:
    #     time_notes = request.form.get("time_notes")
    # except:
    #     time_notes = ""
    try:
        author = request.form.get("author")
    except:
        author = ""

    incomplete_Ing = []

    if 'clear' in request.args:

        clear = request.args['clear']

        if clear:
            try:
                print('clear try yes', clear)
                session.pop("ingridients")
                session.pop("steps")
                session.pop("tagsInput")
                ingridients = []
                steps = []
                recipe_name = ""
                recipe_description = ""
                tags = list(mongo.db.tags.find().sort("tag", 1))
                time = ""
                cook_time = ""
                time_notes = ""
                author = ""
                tagsInput = []
                incomplete_Ing = []
            except:
                print('clear try no', clear)
                ingridients = []
                steps = []
                recipe_name = ""
                recipe_description = ""
                tags = list(mongo.db.tags.find().sort("tag", 1))
                time = ""
                cook_time = ""
                time_notes = ""
                author = ""
                tagsInput = []
                incomplete_Ing = []
    else:
        clear = False

        # afterIng = 0
        # afterStep = 0
        # can_add_ing = False
        # can_add_step = False

    if 'afterIng' in request.args:
        afterIng = int(request.args['afterIng'])
    else:
        afterIng = 0

    if 'ing_to_edit' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
    else:
        ing_to_edit = None

    if 'afterStep' in request.args:
        afterStep = int(request.args['afterStep'])
    else:
        afterStep = 0

    if 'step_to_edit' in request.args:
        step_to_edit = int(request.args['step_to_edit'])
    else:
        step_to_edit = 0

    if 'can_add_ing' in request.args:
        afterIng = int(request.args['afterIng'])
        can_add_ing = True
        # return render_template("add_recipe.html", ingridients=ingridients, recipe_description=recipe_description, recipe_name=recipe_name, steps=steps, tags=tags, time=time, time_notes=time_notes, can_add_ing=can_add_ing , afterIng=afterIng)
    else:
        can_add_ing = False

    if 'edit_ing' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
        edit_ing = True

    else:
        edit_ing = False

    if 'can_add_step' in request.args:
        afterStep = int(request.args['afterStep'])

        can_add_step = True
    else:
        can_add_step = False

    if 'edit_step' in request.args:
        step_to_edit = int(request.args['step_to_edit'])

        edit_step = True

    else:
        edit_step = False

    if 'del_ing' in request.args:
        ing_to_del = int(request.args['ing_to_del'])
        if ingridients:
            tagToRemove = str(ingridients[ing_to_del][0])
            if tagToRemove in tagsInput:
                tagsInput.remove(tagToRemove)
            ingridients.pop(ing_to_del)
            session['ingridients'] = list(ingridients)

        # return render_template("add_recipe.html", ingridients=ingridients, recipe_description=recipe_description, recipe_name=recipe_name, steps=steps, tags=tags, time=time, time_notes=time_notes, can_add_ing=can_add_ing)

    if 'del_step' in request.args:
        step_to_del = int(request.args['step_to_del'])
        steps.pop(step_to_del)
        session['steps'] = list(steps)

    if 'ingridient_pos_up' in request.args:
        ingridient_pos = request.args['ingridient_pos_up']
        ingridients[int(ingridient_pos)], ingridients[(int(ingridient_pos)-1)
                                                      ] = ingridients[(int(ingridient_pos)-1)], ingridients[int(ingridient_pos)]
        session['ingridients'] = list(ingridients)

    if 'step_pos_up' in request.args:
        step_pos = request.args['step_pos_up']
        steps[int(step_pos)], steps[(int(step_pos)-1)
                                    ] = steps[(int(step_pos)-1)], steps[int(step_pos)]
        session['steps'] = list(steps)

    if 'ingridient_pos_down' in request.args:
        ingridient_pos = int(request.args['ingridient_pos_down'])
        ingridient_pos_minus_1 = int(ingridient_pos)-1
        len_ingridient_minus_1 = int(len(ingridients))-1
        if ingridient_pos == len_ingridient_minus_1:
            ingridients[int(ingridient_pos)], ingridients[0] = ingridients[0], ingridients[int(
                ingridient_pos)]
        else:
            ingridients[int(ingridient_pos)], ingridients[(int(ingridient_pos)+1)
                                                          ] = ingridients[(int(ingridient_pos)+1)], ingridients[int(ingridient_pos)]
        session['ingridients'] = list(ingridients)

    if 'step_pos_down' in request.args:
        step_pos = int(request.args['step_pos_down'])
        step_pos_minus_1 = int(step_pos)-1
        len_steps_minus_1 = int(len(steps))-1
        if step_pos == len_steps_minus_1:
            steps[int(step_pos)], steps[0] = steps[0], steps[int(
                step_pos)]
        else:
            steps[int(step_pos)], steps[(int(step_pos)+1)
                                        ] = steps[(int(step_pos)+1)], steps[int(step_pos)]
        session['steps'] = list(steps)

    if 'add_ingridient' in request.args:

        recipe_name = str(request.form.get("recipe_name"))
        session['recipe_name'] = recipe_name
        recipe_description = str(request.form.get("recipe_description"))
        session['recipe_description'] = recipe_description

        ingredient1 = []

        ingredient1 = request.form.getlist('ingredient1')
        if ingredient1:
            if not ingredient1 in ingridients:
                if ingredient1[0] and ingredient1[1] and ingredient1[2]:
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        ingridients.insert((afterIng+1), ingredient1)
                    elif 'editIng' in request.args:
                        editIng = int(request.args['editIng'])

                        tagToEdit = str(ingridients[editIng][0])
                        if tagToEdit in tagsInput:
                            tagsInput.remove(tagToEdit)

                        # ingridients.update(editIng, ingredient1)
                        ingridients[editIng] = ingredient1
                    else:
                        ingridients.append(ingredient1)
                    can_add_ing = False
                    edit_ing = False
                    session['ingridients'] = ingridients

                    if ingredient1:
                        if not str(ingredient1[0]) in tagsInput:
                            tagsInput.append(str(ingredient1[0]))
                            session['tagsInput'] = tagsInput

                else:
                    # (ingredient1[0] and  ingredient1[1]) or (ingredient1[0] and  ingredient1[2]) or (ingredient1[1] and  ingredient1[2]):
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        can_add_ing = True
                        incomplete_Ing = request.form.getlist('ingredient1')
                        print('incomplete ings yes afterIng', incomplete_Ing)
                    else:
                        incomplete_Ing = request.form.getlist('ingredient1')
                        print('incomplete ings no afterIng', incomplete_Ing)
                        edit_ing = True
                        ing_to_edit = int(request.args['editIng'])
        else:
            can_add_ing = False
            

        # return render_template("add_recipe.html", ingridients=ingridients, recipe_description=recipe_description, recipe_name=recipe_name, steps=steps, tags=tags, time=time, time_notes=time_notes, can_add_ing=can_add_ing, author=author)

    if 'add_step' in request.args:
        step = ""
        step = request.form.get('step')
        if step is not None:
            step= str(request.form.get('step'))
            if step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    steps.insert((afterStep+1), step)
                elif 'step_to_edit' in request.args:
                    step_to_edit = int(request.args['step_to_edit'])
                    steps[step_to_edit] = step
                else:
                    steps.append(step)
                can_add_step = False
                edit_step = False
                session['steps'] = steps
            if not step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    can_add_step = True

        # context={
        #     'ingridients': ingridients,
        #     'steps': steps,
        #     'recipe_description': recipe_description,
        #     'recipe_name': recipe_name,
        #     'steps': steps,
        #     'tags': tags,
        #     'time': time,
        #     'time_notes': time_notes,
        #     'can_add_ing': can_add_ing,
        #     'can_add_step': can_add_step,
        #     'author': author,
        #     'afterIng': afterIng,
        #     'afterStep': afterStep

        # }
        # print('context', context)

    this_url = request.path
    referer_view = get_referer_view(request)

    if request.method == "POST" and 'recipe' in request.args:

        # for ingredient in ingridients:
        #     if ingredient[0][0]:
        #         print ('lo ingrediente ', ingredient)

        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "ingridients": ingridients,
            # "steps": [request.form.get("step1"), request.form.get("step2")],
            "steps": steps,
            # "tags": list([request.form.get("tags")]),
            # "tags": request.form.getlist("tagsInput"),
            "tags": tagsInput,
            "time": [request.form.get("time"), request.form.get("cook_time"),  request.form.get("time_notes")],
            "author": request.form.get("author"),
        }

        existingTags = list(mongo.db.tags.find().sort("tag", 1))

        existingTagsItems = []
        for tag in existingTags:
            existingTagsItems.append(tag['tag'])

        print('existingTagsItems ', existingTagsItems)
        if tagsInput:
            for x in tagsInput:
                strX = str(x)
                tagToAdd = {"tag": strX}
                if not strX in existingTagsItems:
                    print('aggiungiam la tag', x)
                    mongo.db.tags.insert_one(tagToAdd)

        thisRecipeAuthor = request.form.get("author")
        recipeIDsSoFar = []
        UserRecipesSoFar = list(
            mongo.db.recipes.find({"author": thisRecipeAuthor}))
        for x in UserRecipesSoFar:
            recipeIDsSoFar.append(str(ObjectId(x['_id'])))
            # idsofarid = ObjectId(x['_id'])
            # print('idsofarid ', idsofarid)
            # recipeIDsSoFar.append(idsofarid)

        session['ingridients'] = list(ingridients)
        session['steps'] = list(steps)
        print('tutta la recipe ', recipe)
        mongo.db.recipes.insert_one(recipe)
        NewUserRecipeIDs = []
        LastID = ""
        recipesWithNew = list(mongo.db.recipes.find(
            {"author": thisRecipeAuthor}))
        for x in recipesWithNew:
            NewUserRecipeIDs.append(str(ObjectId(x['_id'])))
            # NewUserRecipeIDs.append(str(ObjectId(x)))
        strLastID = ""
        for x in NewUserRecipeIDs:
            if not x in recipeIDsSoFar:
                LastID = x
                strLastID = str(LastID)

        print('thisRecipeAuthor ', thisRecipeAuthor, 'recipeIDsSoFar', recipeIDsSoFar, 'recipesWithNew',
              recipesWithNew, 'NewUserRecipeIDs ', NewUserRecipeIDs, 'LastID ', LastID, 'strLastID ', strLastID)

        flash("Recipe Successfully Added")
        session.pop("ingridients")
        session.pop("steps")
        session.pop("tagsInput")
        # return redirect(url_for("add_recipe", ingridients=ingridients, steps=steps))
        return redirect(url_for('recipe', recipe_id=LastID))

    # return render_template("add_recipe.html", categories=categories, ingridients=ingridients, can_add_ing=can_add_ing, context=context)
    # return render_template("add_recipe.html", ingridients=ingridients, recipe_description=recipe_description, recipe_name=recipe_name, steps=steps, tags=tags, time=time, time_notes=time_notes, can_add_ing=can_add_ing, author=author, afterIng=afterIng, can_add_step=can_add_step,  afterStep=afterStep, clear=clear, incomplete_Ing =incomplete_Ing)
    return render_template("add_recipe.html", this_url=this_url, referer_view=referer_view, ingridients=ingridients, tagsInput=tagsInput, steps=steps, tags=tags, can_add_ing=can_add_ing, edit_step=edit_step, edit_ing=edit_ing, ing_to_edit=ing_to_edit, author=author, afterIng=afterIng, can_add_step=can_add_step, step_to_edit=step_to_edit, afterStep=afterStep, clear=clear, incomplete_Ing=incomplete_Ing)
    # return redirect(url_for("add_recipe", context=context))


@app.route("/edit_recipe", methods=["GET", "POST"])
def edit_recipe():
    if 'recipe_id' in request.args:
        time = ""
        cook_time = ""
        time_notes = ""
        recipe_id = request.args['recipe_id']
        session['recipe_id'] = recipe_id
        recipeToEdit = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        # print('recipeToEdit ', recipeToEdit)
        tags = list(mongo.db.tags.find().sort("tag", 1))

        recipe_nameFetched = recipeToEdit.get('recipe_name')
        recipe_descriptionFetched = recipeToEdit.get('recipe_description')
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

        # print("Value : %s" %  recipeToEdit.get('ingridients'))
        # print("ingridientsFetched : ", ingridientsFetched)
        print("stepsFetched : ", stepsFetched)

        session['ingridients'] = ingridientsFetched
        session['steps'] = stepsFetched
        session['tagsInput'] = tagsFetched
        ingridients = session['ingridients']
        steps = session['steps']
        tagsInput = session['tagsInput']

        return render_template("edit_recipe.html", recipe=recipeToEdit, tags=tags, recipe_name=recipe_name, recipe_description=recipe_description, time=time, cook_time=cook_time, time_notes=time_notes,  recipe_id=recipe_id, ingridients=ingridients, steps=steps, tagsInput=tagsInput)
        # return render_template("edit_recipe.html", recipe=recipeToEdit, ingridients=ingridients, tagsInput=tagsInput, steps=steps, tags=tags, can_add_ing=can_add_ing, edit_step=edit_step, edit_ing=edit_ing, ing_to_edit=ing_to_edit, author=author, afterIng=afterIng, can_add_step=can_add_step, step_to_edit=step_to_edit, afterStep=afterStep, clear=clear, incomplete_Ing=incomplete_Ing)

    try:
        recipe_id = session['recipe_id']
    except:
        recipe_id = ""

    try:
        tagsInput = session['tagsInput']

        print('ci sta a session di tags inputtags ', tagsInput)
    except:
        tagsInput = []
        print('recipeToEdit. ', tagsInput)

    extra_Ing = False

    if 'addTagBtn' in request.args:
        print('ok addTagBtn ce  ')
        pick_tag = request.form.get("pick_tag")
        new_tag = request.form.get("new_tag")

        print('e pure pick_tag ce  ', pick_tag)
        if pick_tag != None:
            if pick_tag not in tagsInput:
                tagsInput.append(str(pick_tag))
                print('tagsInput ', tagsInput)
                session['tagsInput'] = tagsInput

        print('e pure new_tag ci ha sta  ', new_tag)
        if new_tag != None:
            if new_tag not in tagsInput:
                tagsInput.append(str(new_tag))
                print('tagsInput e newtag', tagsInput, new_tag)
                session['tagsInput'] = tagsInput

    try:
        ingridients = session['ingridients']
    except:
        ingridients = []

    try:
        recipe_name = request.form.get("recipe_name")
        if recipe_name is not None:
            session['recipe_name'] = str(recipe_name)
        else:
            try:
                recipe_name = str(session['recipe_name'])
            except:
                recipe_name = ""
    except:
        recipe_name = ""

    try:
        steps = session['steps']
    except:
        steps = []
    try:
        tags = list(mongo.db.tags.find().sort("tag", 1))
        if tagsInput:
            for tag in tags:
                if tag['tag'] in tagsInput:
                    print('effetivamnete ce ', tag['tag'])
                    tags = [i for i in tags if i != tag]
                else:
                    print(tag['tag'], 'not included')
        # print('quel che rimane de tags ', tags)

    except:
        try:
            tags = list(mongo.db.tags.find().sort("tag", 1))
        except:
            tags = []
            print('try tagd ha fallito')

    if 'delTag' in request.args:
        deltag = request.args['delTag']
        if tagsInput:
            for tag in tagsInput:
                if tag == deltag:
                    print('found deltag', deltag)
                    tagsInput.remove(tag)

                    print('le tags a questo punto ', tags)
            tags = list(mongo.db.tags.find().sort("tag", 1))
            for tag in tags:
                if tag['tag'] in tagsInput:
                    tags = [i for i in tags if i != tag]
                else:
                    print('quel che rimane de tags DE NOVO ', tags)

    try:
        author = request.form.get("author")
    except:
        author = ""

    incomplete_Ing = []

    if 'clear' in request.args:

        clear = request.args['clear']

        if clear:
            try:
                print('clear try yes', clear)
                session.pop("ingridients")
                session.pop("steps")
                session.pop("tagsInput")
                ingridients = []
                steps = []
                recipe_name = ""
                recipe_description = ""
                tags = list(mongo.db.tags.find().sort("tag", 1))
                time = ""
                cook_time = ""
                time_notes = ""
                author = ""
                tagsInput = []
                incomplete_Ing = []
            except:
                print('clear try no', clear)
                ingridients = []
                steps = []
                recipe_name = ""
                recipe_description = ""
                tags = list(mongo.db.tags.find().sort("tag", 1))
                time = ""
                cook_time = ""
                time_notes = ""
                author = ""
                tagsInput = []
                incomplete_Ing = []
    else:
        clear = False

    if 'afterIng' in request.args:
        afterIng = int(request.args['afterIng'])
    else:
        afterIng = 0

    if 'ing_to_edit' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
    else:
        ing_to_edit = None

    if 'afterStep' in request.args:
        afterStep = int(request.args['afterStep'])
    else:
        afterStep = 0

    if 'step_to_edit' in request.args:
        step_to_edit = int(request.args['step_to_edit'])
    else:
        step_to_edit = 0

    if 'can_add_ing' in request.args:
        afterIng = int(request.args['afterIng'])
        can_add_ing = True
    else:
        can_add_ing = False

    if 'edit_ing' in request.args:
        ing_to_edit = int(request.args['ing_to_edit'])
        edit_ing = True

    else:
        edit_ing = False

    if 'can_add_step' in request.args:
        afterStep = int(request.args['afterStep'])

        can_add_step = True
    else:
        can_add_step = False

    if 'edit_step' in request.args:
        step_to_edit = int(request.args['step_to_edit'])

        edit_step = True

    else:
        edit_step = False

    if 'del_ing' in request.args:
        ing_to_del = int(request.args['ing_to_del'])
        if ingridients:
            tagToRemove = str(ingridients[ing_to_del][0])
            if tagToRemove in tagsInput:
                tagsInput.remove(tagToRemove)
            ingridients.pop(ing_to_del)
            session['ingridients'] = list(ingridients)

    if 'del_step' in request.args:
        step_to_del = int(request.args['step_to_del'])
        steps.pop(step_to_del)
        session['steps'] = list(steps)

    if 'ingridient_pos_up' in request.args:
        ingridient_pos = request.args['ingridient_pos_up']
        ingridients[int(ingridient_pos)], ingridients[(int(ingridient_pos)-1)
                                                      ] = ingridients[(int(ingridient_pos)-1)], ingridients[int(ingridient_pos)]
        session['ingridients'] = list(ingridients)

    if 'step_pos_up' in request.args:
        step_pos = request.args['step_pos_up']
        steps[int(step_pos)], steps[(int(step_pos)-1)
                                    ] = steps[(int(step_pos)-1)], steps[int(step_pos)]
        session['steps'] = list(steps)

    if 'ingridient_pos_down' in request.args:
        ingridient_pos = int(request.args['ingridient_pos_down'])
        ingridient_pos_minus_1 = int(ingridient_pos)-1
        len_ingridient_minus_1 = int(len(ingridients))-1
        if ingridient_pos == len_ingridient_minus_1:
            ingridients[int(ingridient_pos)], ingridients[0] = ingridients[0], ingridients[int(
                ingridient_pos)]
        else:
            ingridients[int(ingridient_pos)], ingridients[(int(ingridient_pos)+1)
                                                          ] = ingridients[(int(ingridient_pos)+1)], ingridients[int(ingridient_pos)]
        session['ingridients'] = list(ingridients)

    if 'step_pos_down' in request.args:
        step_pos = int(request.args['step_pos_down'])
        step_pos_minus_1 = int(step_pos)-1
        len_steps_minus_1 = int(len(steps))-1
        if step_pos == len_steps_minus_1:
            steps[int(step_pos)], steps[0] = steps[0], steps[int(
                step_pos)]
        else:
            steps[int(step_pos)], steps[(int(step_pos)+1)
                                        ] = steps[(int(step_pos)+1)], steps[int(step_pos)]
        session['steps'] = list(steps)

    if 'add_ingridient' in request.args:

        recipe_name = str(request.form.get("recipe_name"))
        session['recipe_name'] = recipe_name
        recipe_description = str(request.form.get("recipe_description"))
        session['recipe_description'] = recipe_description

        ingredient1 = []

        ingredient1 = request.form.getlist('ingredient1')
        if ingredient1:
            if not ingredient1 in ingridients:
                if ingredient1[0] and ingredient1[1] and ingredient1[2]:
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        ingridients.insert((afterIng+1), ingredient1)
                    elif 'editIng' in request.args:
                        editIng = int(request.args['editIng'])

                        tagToEdit = str(ingridients[editIng][0])
                        if tagToEdit in tagsInput:
                            tagsInput.remove(tagToEdit)

                        # ingridients.update(editIng, ingredient1)
                        ingridients[editIng] = ingredient1
                    else:
                        ingridients.append(ingredient1)
                    can_add_ing = False
                    edit_ing = False
                    session['ingridients'] = ingridients

                    if ingredient1:
                        if not str(ingredient1[0]) in tagsInput:
                            tagsInput.append(str(ingredient1[0]))
                            session['tagsInput'] = tagsInput

                else:
                    # (ingredient1[0] and  ingredient1[1]) or (ingredient1[0] and  ingredient1[2]) or (ingredient1[1] and  ingredient1[2]):
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        can_add_ing = True
                        incomplete_Ing = request.form.getlist('ingredient1')
                        print('incomplete ings yes afterIng', incomplete_Ing)
                    else:
                        incomplete_Ing = request.form.getlist('ingredient1')
                        print('incomplete ings no afterIng', incomplete_Ing)
                        edit_ing = True
                        ing_to_edit = int(request.args['editIng'])
        else:
            can_add_ing = False


    if 'add_step' in request.args:
        step = ""
        step = request.form.get('step')
        if step is not None:
            step= str(request.form.get('step'))
            if step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    steps.insert((afterStep+1), step)
                elif 'step_to_edit' in request.args:
                    step_to_edit = int(request.args['step_to_edit'])
                    steps[step_to_edit] = step
                else:
                    steps.append(step)
                can_add_step = False
                edit_step = False
                session['steps'] = steps
            if not step:
                if 'afterStep' in request.args:
                    afterStep = int(request.args['afterStep'])
                    can_add_step = True
    
    this_url = request.path
    referer_view = get_referer_view(request)

    if request.method == "POST" and 'editRecipe' in request.args:

        # for ingredient in ingridients:
        #     if ingredient[0][0]:
        #         print ('lo ingrediente ', ingredient)

        editRecipe = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "ingridients": ingridients,
            "steps": steps,
            "tags": tagsInput,
            "time": [request.form.get("time"), request.form.get("cook_time"),  request.form.get("time_notes")],
            "author": request.form.get("author"),
        }

        existingTags = list(mongo.db.tags.find().sort("tag", 1))

        existingTagsItems = []
        for tag in existingTags:
            existingTagsItems.append(tag['tag'])

        print('existingTagsItems ', existingTagsItems)
        if tagsInput:
            for x in tagsInput:
                strX = str(x)
                tagToAdd = {"tag": strX}
                if not strX in existingTagsItems:
                    print('aggiungiam la tag', x)
                    mongo.db.tags.insert_one(tagToAdd)

        # session['ingridients'] = list(ingridients)
        # session['steps'] = list(steps)
        print('tutta la recipe ', editRecipe)
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, editRecipe)
        # flash("Recipe Successfully Added")
        session.pop("ingridients")
        session.pop("steps")
        session.pop("tagsInput")
        session.pop("recipe_id")

        # mongo.db.tasks.update({"_id": ObjectId(task_id)}, submit)
        flash("Recipe Successfully Updated")

        return redirect(url_for('recipe', recipe_id=recipe_id))
        # return redirect(url_for("edit_recipe", ingridients=ingridients, steps=steps))

    return render_template("edit_recipe.html", this_url=this_url, referer_view=referer_view, ingridients=ingridients, recipe_id=recipe_id, tagsInput=tagsInput, steps=steps, tags=tags, can_add_ing=can_add_ing, edit_step=edit_step, edit_ing=edit_ing, ing_to_edit=ing_to_edit, author=author, afterIng=afterIng, can_add_step=can_add_step, step_to_edit=step_to_edit, afterStep=afterStep, clear=clear, incomplete_Ing=incomplete_Ing)


def get_referer_view(request, default=None):
    '''
    Return the referer view of the current request
    Example:
        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    # referer = request.META.get('HTTP_REFERER')
    referer = request.referrer
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    # leave it cornflakes, this is actually correct.
    # referer = re.sub('^https?:\/\/', '', referer).split('/')
    referer = re.sub('^https:\/\/', '', referer).split('/')
    # referer=str(referer)
    # referer.split('?')[0]
    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    referer=referer.split('?')[0]
    return referer

@app.route("/delete_recipe/<recipe_id>/<username>", methods=["GET", "POST"])
def delete_recipe(recipe_id, username):
    recipeToDelete = mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    username = mongo.db.users.find_one({"username": username})
    return redirect(url_for('profile', username=username))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
