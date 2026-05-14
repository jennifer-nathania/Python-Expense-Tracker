#Python HW 3 | Jennifer Nathania (梁嫺女) - 112006202
import sys

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """_summary_
        This function initializes a list of categories
        Returns:
            list: a nested list that contains categories and its sub-categories
        """
        self.records = []
        try:
            with open('records.txt', 'r') as f:
                beginning = f.readline().strip() #read first line
                # EXCEPTION 8: File exists but no lines are inside
                if not beginning:
                    raise ValueError("Empty file")
            
                # EXCEPTION 9: First line in file can't be parsed as an integer
                try:
                    self.bank = int(beginning)
                except ValueError:
                    raise ValueError("Invalid initial amount in file")

                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                
                    # EXCEPTION 10: any of the other lines cannot be interpreted as a record
                    parts = line.split()
                    # Must have at least 3 parts: category, desc (can be multiple words), amount
                    if len(parts) < 3:
                        print(f"Invalid record format: {line}", file=sys.stderr)
                        continue

                    try:
                        amount = int(parts[-1])
                        desc = ' '.join(parts[1:-1])
                        category = parts[0]
                        self.records.append((category, desc, amount))
                    except ValueError:
                        print(f"Invalid amount in record: {line}", file=sys.stderr)

                print("Welcome back!")

        # EXCEPTION 7: File does not exist when trying to load
        except FileNotFoundError:
            while True:
                try:
                    self.bank = int(input("How much money do you have? "))
                    break
                # EXCEPTION 1: Invalid value for money
                except ValueError:
                    print("Invalid value for money.", file=sys.stderr)
        except ValueError as e:
            print(e, file=sys.stderr)
            while True:
                try:
                    self.bank = int(input("How much money do you have? "))
                    break
                except ValueError:
                    print("Invalid value for money.", file=sys.stderr)

    def add(self, categories):
        '''
        Adds new expense/income records
        Returns:
            list: updated records list
        '''
        print("Add some expense or income records with description and amount:")
        add_input = input().strip() #everything is inputted as one
        # if add_input has nothing
        if add_input == "":
            print("No input.", file=sys.stderr)
            return
        
        #per item specification is split by commas
        parts = add_input.split(',')

        #now splitting the desc and amount of each item
        for part in parts:
            record_str = part.strip()
            if record_str == "":
                continue

            #throw out an invalid format when there's either no desc or amount
            record_parts = record_str.split()
            # EXCEPTION 3: The user inputs a string that does not follow the format
            if len(record_parts) < 3:
                print("Invalid format:", record_str, file=sys.stderr)
                continue
            
            try:
                #parse it out
                amount = int(record_parts[-1]) #last item
                desc = ' '.join(record_parts[1:-1]) #middle item
                category = record_parts[0]; #first item
                
                if not categories.is_category_valid(category):
                    print(f"Invalid category: {category}", file = sys.stderr)
                    continue
                
                #append both to records list
                self.records.append((category, desc, amount))
            
            # EXCEPTION 4: the second string of a record, after splitting, cannot be converted to an integer.
            except ValueError:
                print(f"Invalid amount in record: {record_str}.", file=sys.stderr)

    def view(self):
        '''
        Displays all records and calculates the current balance.
        '''
        print("\nHere's your expense and income records:")
        print("Category       Description          Amount")
        print("=============  ==================== ======")
    
        total = self.bank
        for rec in self.records:
            category = rec[0]
            desc = rec[1]
            amount = rec[2]
            print("{:<14} {:<20} {:>6}".format(category, desc, amount))
            total += amount
        
        print("=============  ==================== ======")
        print(f"Now you have {total} dollars.")   

    def delete(self):
        '''
        Deletes a record by its ID.
        Returns:
            list: Updated records after deletion.
        '''
        if not self.records:
            print("You don't have any records to delete.")
            return
        
        print("Current records:")
        print("ID   Category       Description          Amount")
        print("===  =============  ==================== ======")
        
        for i, (category, desc, amount) in enumerate(self.records, 1):
            print("{:<4} {:<14} {:<20} {:>6}".format(i, category, desc, amount))
        

        try:
            record_id = int(input("Delete record with ID:  ").strip())
            # EXCEPTION 6: ID is out of range (the specified record does not exist)
            if record_id < 1 or record_id > len(self.records):
                print("Invalid record ID.", file=sys.stderr)
                return
            del self.records[record_id - 1]
        # EXCEPTION 5: the user inputs in an invalid format in respect of your design
        except ValueError:
            print("Invalid input.", file=sys.stderr)

    def find(self, categories):
        '''
        Searches for records according to category and prints them.
        '''
        user_input = input('Which category do you want to find? ').strip()
        if not user_input:
            print("Please enter a category.")
            return
            
        sub_category = categories.find_subcategories(user_input)
        
        if not sub_category:
            print("Category does not exist")
            return
        
        #record is each tuple in self.records (ex: food, lunch, 50) and record[0] is the category name
        #filter(function, iterable) format returns an iterator containing items whose function returns true
        #in words: filtered_list checks if the category exists in sub_category and also in the self.records,
        #and then temporarily moves it for easy viewing into filtered_list
        filtered_list = list(filter(lambda record: record[0] in sub_category, self.records))
        
        if not filtered_list:
            print("Nothing found in this category.")
            return
        
        print(f"Here's your records under category '{user_input}':")
        print("Category       Description          Amount")
        print("=============  ==================== ======")

        total = 0
        for category, desc, amount in filtered_list:
            print("{:<14} {:<20} {:>6}".format(category, desc, amount))
            total += amount

        print("=============  ==================== ======")
        print(f"Total amount above is {total}")

    def save(self):
        '''
        Saves the current financial data to 'records.txt'.
        '''
        try:
            with open('records.txt', 'w') as f:
                f.write(f"{self.bank}\n")
                for category, desc, amount in self.records:
                    f.write(f"{category} {desc} {amount}\n")
        except Exception as e:
            print(f"Error saving records: {e}", file=sys.stderr)
            

class Categories:
    """Maintain the category list and provide some methods."""
    
    def __init__(self):
        """Initialize the list of categories."""
        self.categories = [
            'expense', [
                'food', ['meal', 'snack', 'drink'],
                'transportation', ['bus', 'railway'],
                'utilities', ['electricity', 'water', 'internet'],
                'entertainment', ['movies', 'games'],
                'clothing', ['shirt', 'pants', 'dress', 'suit']
            ],
            'income', [
                'salary',
                'bonus',
                'overtime'
            ]
        ]

    def view(self, categories=None, indent=0):
        '''
         Displays all available the category lists
        '''
        if categories is None:
            categories = self.categories
            
        bullets = ['>', '*', '-']
        
        for item in categories:
            if isinstance(item, list):
                self.view(item, indent + 2)
            else:
                # convert indent to level 
                level = indent // 2
                bullet = bullets[level] if level < len(bullets) else bullets[-1]
                print(" " * indent + f"{bullet} {item}")

    def is_category_valid(self, category, categories=None):
        '''
        Validates the existence of the category in the list
        Returns: 
            bool: True if the category exists, False otherwise.
        '''
        if categories is None:
            categories = self.categories
        for i in categories:
            if isinstance(i, list):
                #recursive subcategory checking
                if self.is_category_valid(category, i): #if found return true
                    return True
            elif i == category: #if the direct item is the category, return true
                return True
        return False

    def find_subcategories(self, category, categories=None):
        '''
        Finds all subcategories of a given category.
        Returns:
            list or bool: Flattened list of subcategories if found, else False.
        '''
        def find_subcategories_gen(categories, target, found=False):
            # Parent categories trigger this --> ex: food, transportation, etc
            if type(categories) == list:  # If the type is a list
                # Iterate through each item in current level
                for idx, item in enumerate(categories):
                    # Recursive child items search
                    yield from find_subcategories_gen(item, target, found)
                    
                    # If match is found and has subcategories
                    if (item == target and 
                        idx + 1 < len(categories) and 
                        type(categories[idx + 1]) == list):
                        # Yield all items in subcategory list
                        yield from find_subcategories_gen(categories[idx + 1], target, True)
            else:
                # Leaf categories trigger this --> ex: meal, drink
                if categories == target or found:
                    yield categories
                    
        # Return function
        if categories is None:
            return list(find_subcategories_gen(self.categories, category))
        else:
            return list(find_subcategories_gen(categories, category))

# === MAIN PROGRAM ===
print("=== THE ULTIMATE EXPENSE TRACKER ===")

categories = Categories()
records = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ').strip()
    if command == 'add':
        records.add(categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        records.delete()
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        records.find(categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')