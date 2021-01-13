
# Cocktails Galore

A community cocktails recipes' database. Recipes posted on the website are free to browse for anyone. Posting is restricted to registered users only.

Website goal:
* to build up, manage and make publicly available an online cocktails recipes' database.

Users' goal:
* to freely browse recipes, and/or to contribute as registered users.

---

## UX

* Calming color theme.
* Navbar appearing across all site pages.
* Table of recipes immediately available from landing page.
* Easy to fill forms to upload/edit recipes.
* useful pill-like tags for quick recipe description.
* Straightforward login and registration processess.

---

## User stories

As a .. | I want to .. | So I can ..
 --- | --- | --- 
website owner|have a db quickly built up with the help of many registered contributors|make the resource available to wider community
website visitor|freely browse the website|find inspiration for my next drink
webiste visitor|search the website for a specific cocktail recipe|learn to prepare it by myself
registered user|post my own recipes|contribute to the db build up
registred user|have the abilty to amend and delete my own posts|avoid the embarassment of poorly edited recipes

---

## Wireframes

* [Landing Page](https://ctmp3.s3-eu-west-1.amazonaws.com/RB+WF/RB+landing+page.png)
* [Recipe Page](https://ctmp3.s3-eu-west-1.amazonaws.com/RB+WF/RB+recipe+page.png)
* [Upload Recipe](https://ctmp3.s3-eu-west-1.amazonaws.com/RB+WF/RB+upload+recipe.png)
* [User Page](https://ctmp3.s3-eu-west-1.amazonaws.com/RB+WF/RB+user+page.png)
---

## Features
* A Navbar is present on all website pages, with the website's title, links to other pages, and a search box. Some links will only be available to registered users.
On small to medium screens all link will collapse into button on the top-right corner, with the exception of the website's title, Cocktails Galore, which serves as Home link.
* The landing page opens directly on a grid of card-like summaries of all the recipes.
* On each card are stated the recipe's title and author, which serve as links to the recipe's full description and its authors dedicated pages.
* Registered users will see also two buttons on each of their own recipes' cards; these buttons are for editing and deleting. 
* Other inforrmation dispalyed: the recipe's  description, required time and tags.
* The tags are words that relate to the recipe in some way. They are enclosed in pill-like mini-buttons. 
From the landing page, on click, these pills will initiate a search of all recipies containing that word; The grid of recipes will shrink to the search's result.
* On click on the recipe's card title, the individual recipe's page will open with full details including ingredients and step-by-step method. 
* The recipe's author will see also here two buttons at the top, which redirect to an edit form or delete the recipe from the db. The website admin will only be able to see the delete button.
* Also on this page any registered user will be able to add pill tags to the recipe, whether they're its authors or not. Unregistred users will only be able to view the recipe.
* Each author have their own page containing the list of the recipe they posted. This page is available from the a dropdown menu on the Navbar("Authors"), or by following the link on the author's name on the recipe card.
* Login, Register(when the user is not logged) and Logout(when the user is logged) links are available on the Navbar. The login and registration forms only have the username and password fields. A username can have a blank space between words only.
* Upon succesful registration a new document will be created in the 'users' collection in MongoDB.
* The "Add Recipe" will appear on the Navbar for logged users. It leads to a recipe form. Some fields are mandatory. At least one ingredient and one step are required. after the first ingredient/step is inserted, the form will refresh with the updated lists of ingredients and steps.
* The ingredients and method sections stack up on small screens and stand side by side on medium and upwards.
* Beside each ingredient and each step is displayed a "+" button. On click, it will open a mini form to add another ingredient/step immediately below.
* Beside the same "+" there is a wrench icon. On hover on each ingredient/step, additional buttons will appear do move up/down, edit or delete that ingredient/step.
* Within the ingredient mini form, there is a select box where the user can pick a measure unit, or other rough quantity indicator; for example, a quantity of "1" can be combined with the option "just one loose", to display "1 loose orange".
The option "not applicable/fraction" will display, if combined with "1" or partial numbers:

number | combined with not applicable/fraction diplays as | example
 --- | --- | --- 
 0.25|1/4|1/4 orange
 0.50|1/2|1/2 glass of wine
 0.75|3/4|3/4 ltr
 1|no number diplayed|ice

 * Below the ingredients and method sections, two inputs allow the user add tags to the recipe. The first input is a select box with all the tags currently available for selction in the db.
 the second input is a free text box, where the user can insert a new tag. When the recipe is successfully saved, also the new tag will be inserted in the db throough the creation of a new document in the 'tags' collection. It will be then selectable from the select box in the future.
 * Each tag input can be activated by clicking on the corresponding radio button. Enabling one tag input disables the other. on first load of the page, both tag inputs are disabled. Once either is selected, the "Add Tag" button becomes enabled.
 * Each added ingredient's name gets automatically reflected as tag in the tags section. The user can then remove the tag manually. 
 * Each tag added shows with an "X" in the pill. If clicked at any point before the 'Add Recipe' is finally hit, the tag is removed.
 * A similar tag input system is in place on the individual recipe page. From there any logged user can add a tag to any recipe of his fellow contributors. The application is immediate and only the recipe's author or the admin will then be able to remove it.
 * A new document is inserted in the 'recipe' collection when the 'Add Recipe' button is finally clicked. 
 * The update form follows the same pattern except for the fact that the the existing recipe data prefills the form upon page loading. The MongoDB 'recipes' collection document is updated when the 'Edit Recipe' button is hit.
 * A text index searches in the 'recipe_name', 'recipe_description', 'ingridients' and 'tags' fields in the 'recipes' collection. The index is used in the search box and within each card tags button in the home page. 
---

## Technologies used
* Flask framework (python)
* MongoDB + pymongo
* * Three collections used: 'recipe', 'tags' and 'users'
* * The 'tags' (tag) and 'users' ('username', 'password') collections consist only one and two fields respectively.
* * The 'recipe' collection is the most complex with 'recipe_name', 'recipe_description', and 'author' as text fields and 'ingridients'(with sub-arrays), 'time', 'steps', and 'tags' as arrays.
* Gitpod develpoment enviroment
* HTML5
* CSS3, Bootstrap 4
* Javascript, Jquery
* Werkzeug (python)

---

## Cloning this project from Github to your Gitpod account.
This project's repository can be found [here](https://github.com/PaoloAlbanese/cocktails).
Please access the repository on a Chrome browsers complete with [gitpod extension](https://www.gitpod.io/docs/browser-extension/).
By clicking the green "Gitpod" button in the top right corner of the repository, you will create a new workspace from the repository's code in your enviroment.
The live deployed webiste can be found on [Heroku](https://cocktails-flask.herokuapp.com/).

---

## Testing
Testing consisted in repeaditely running the app, by trying to browse pages, manipulate db documents through the Web Preview, toggling screen size in inspect mode, and to let any glitches come to surface. Jinja terminal and browser errors on console/elements tab in inspect mode where interpreted.
print and console.log statement where placed in the code to locate where error was/wasn't occurring. The MongoDB website was being crosscheked to confirm the db was updating as intended.

---

## 2 bugs found

* The Add Recipe and Edit Recipe forms refresh several times before the recipe is finally saved or updated. At each refresh the fields that had already been filled by the user where blanked again.
The solution was to use JS local storage variables for one-time entry fields such as recipe name and recipe description, and session variables for repeated entry fields such as ingredients, steps and tags, which where passed to the template via jinja template tags.    

* While creating or updating a recipe, each ingredient or step is added via a dedicated button. if the user refereshes the page after that, the form is resubmitted creating a duplicate ingredient or step.
The data resubmission can be avoided by using this JS code that sets to window history to Null, tip from dtbaker on [Stackoverflow](https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr) :

```
if ( window.history.replaceState ) {
       window.history.replaceState( null, null, window.location.href );
   }
```

This however doesn't prevent the python code from being triggered an the ingredient'step row is created with a string representation of the Null value.
The remedy was to change, for example, in the following piece of code:

```
if not ingredient1 in ingridients:
               if ingredient1[0] and ingredient1[1] and ingredient1[2]:
                   if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                       ingridients.insert((afterIng+1), ingredient1)
                   elif 'editIng' in request.args:
                        editIng = int(request.args['editIng'])`

```
to this, by adding an if statement at the top:
```
if ingredient1:
            if not ingredient1 in ingridients:
                if ingredient1[0] and ingredient1[1] and ingredient1[2]:
                    if 'afterIng' in request.args:
                        afterIng = int(request.args['afterIng'])
                        ingridients.insert((afterIng+1), ingredient1)
                    elif 'editIng' in request.args:
                        editIng = int(request.args['editIng'])`
```

## Acknowledgments

* The authentication sections of the code are based on Tim Nelson's task manager app mini project(Code Institute) in the data centric module;
* The recepies are taken from the BBC's Good Food website, their authors' names being entered as users in the DB;
* Several icons are sourced from Fontawesome;
* [Stackoverflow](https://stackoverflow.com/) and [W3Schools](https://www.w3schools.com/) where widely used for general reference;
* get_referer_view, (Copyright (c) 2009 Arthur Furlan <arthur.furlan@gmail.com>);
* JS code to prevent form re-submission, tip from dtbaker on [Stackoverflow](https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr)
* RegEx to allow space between words, stema on [Stackoverflow](https://stackoverflow.com/questions/15472764/regular-expression-to-allow-spaces-between-words/15473717#15473717);
* CSS to remove 3D push effect on button, allicarn on [Stackoverflow](https://stackoverflow.com/questions/5466906/remove-3d-push-effect-on-a-button);
* Toggle Visibility When Hiding Elements, Robin Rendle on [CSS Tricks](https://css-tricks.com/snippets/css/toggle-visibility-when-hiding-elements/);
* Hover on father elemet activates a child element css, [CodeGrepper](https://www.codegrepper.com/code-examples/css/hover+on+father+elemet+activates+a+child+element+css);
* Remove a query string from URL using Python, Clarius on [Stackoverflow](https://stackoverflow.com/questions/7734569/how-do-i-remove-a-query-string-from-url-using-python);

---

## Notes to the Assessors:
The credentials of the admin and of one user will be submitted with the project.


# The End


