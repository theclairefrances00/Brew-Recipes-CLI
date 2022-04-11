import recipeDB

MENU_PROMPT = """ \n --- Recipe App ---
Please choose one of these options:

1) Add a new recipe
2) List all recipes
3) Show all ingredients in a recipe (testing)
5) Exit

Your selection: """

ADD_INGREDIENTS_PROMPT = """\nAdd Ingredients:
Enter 'q' when done
Enter ingredient name: """

def menu():
    while(user_input := input(MENU_PROMPT))!="5":
        if user_input =="1":
            recipe_name = input("Enter name: ")
            
            if(recipeDB.recipe_exists(connection, recipe_name)):
                print("This recipe already exists")
            else:
                description = input("Enter description: ")
                abv = input("Enter abv range: ")
                recipe_type = input("Enter recipe type (b = beer, c = cider, s = seltzer):")
                
                recipeDB.add_recipe(connection, recipe_name, description, abv, recipe_type)
                recipe_id = recipeDB.get_recipe_id_by_name(connection, recipe_name)[0]
                
                while(ingredient_name := input(ADD_INGREDIENTS_PROMPT))!="q":
                    quantity_unit = input("Enter quantity and unit in format quantity-unit (for example: 2-cup): ")

                    if(not recipeDB.ingredient_exists(connection, ingredient_name)): #need to add new ingredient
                        recipeDB.add_ingredient(connection, ingredient_name)
                    ingredient_id = recipeDB.get_ingredient_id_by_name(connection, ingredient_name)[0]

                    quantity_unit=quantity_unit.split("-")
                    print(quantity_unit)
                    if(not recipeDB.quantity_exists(connection, quantity_unit[0])): #need to add new quantity
                        recipeDB.add_quantity(connection, quantity_unit[0])
                    quantity_id = recipeDB.get_quantity_id_by_name(connection, quantity_unit[0])[0]
                    if(not recipeDB.unit_exists(connection, quantity_unit[1])): #need to add new unit
                        recipeDB.add_unit(connection, quantity_unit[1])
                    unit_id = recipeDB.get_unit_id_by_name(connection, quantity_unit[1])[0]
                    
                    recipeDB.add_to_rel_table(connection, recipe_id, ingredient_id, quantity_id, unit_id)
        elif user_input =="2":
            print(recipeDB.get_recipe_names(connection))
        elif user_input =="3":
             name=   input("Name:")
             print(recipeDB.get_recipe_ingredients(connection, name))
             #print(recipeDB.get_all_ingredients(connection))
       # elif user_input =="3":
       # elif user_input =="4":

        else:
            print("Invalid input, please try again!")
   
    
connection = recipeDB.connect()
#recipeDB.delete_recipe_by_name(connection, "American Amber")
recipeDB.create_tables(connection)
menu()
