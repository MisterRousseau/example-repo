#========MODULES==========
import statistics as s
import tabulate as tab

#========CLASSES==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity, file_index):
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)
        self.file_index = file_index
        
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        name = self.product
        qty = self.quantity
        cost = self.cost
        id = self.code
        loc = self.country
        return f'''
        Country:    {loc}
        Code:       {id}
        Product:    {name}
        Quantity:   {qty}
        Cost:       {cost} '''
    
    def __iter__(self):
        yield self.country
        yield self.code
        yield self.product
        yield self.cost
        yield self.quantity

#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

#==========Functions outside the class==============
def user_input(prompt, check="bool"):
    '''
    This function is used to take user input and validate it against
    expected values
    '''
    #If expecting listed values print them out
    if type(check) == list:
        check_pairs = [[str(i), j] for i, j in enumerate(check)]
        check_strings = [f'{i}) {j}' for i, j in check_pairs]
        print('\n' + '\n'.join(check_strings))
              
    #Loop until valid input provided
    while True:

        #Get input, prepare failure message
        inpt = input(prompt)
        fail = f'"\n{inpt}" is not a valid input.'

        # Logic for listed expectation    
        if type(check) == list:
            for pair in check_pairs:
                if inpt.lower() in [check.lower() for check in pair]:
                    print(f'\nSelected: {pair[1]}')
                    return pair[1]
            print(fail)
        
        # Logic for boolean expectation
        if check == "bool":
            if inpt.lower() in ['y','yes','true']:
                return True
            elif inpt.lower() in ['n','no','false']:
                return False
            else:
                print(fail)

        # Logic for numeric (positive digit) expectation
        elif check == "numeric":
            if inpt.isdigit():
                return int(inpt)
            else:
                print(fail)

def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes. You must use the try-except in this function
    for error handling. Remember to skip the first line using your code.
    '''
    try:
        # Open inventory.txt file, loop through each line and call 
        # capture_shoes function on the data
        with open('inventory.txt', 'r') as file:
            lines = file.readlines()
            for i in range(1, len(lines)):
                capture_shoes(lines[i], i)  
            print('\nShoe data read into memory.')         
    except FileNotFoundError:
        print('Could not find file "inventory.txt"')
        return FileNotFoundError
    
def capture_shoes(shoe_str, file_index):

    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    # Unpack shoe string, add file_index to list, and create shoe
    # object to append to shoe_list
    shoe_data = *shoe_str.split(','), file_index
    shoe_list.append(Shoe(*shoe_data))

def modify_shoes_data(shoe, qty):
    '''
    This function will modify shoe data in the shoe_list list and in 
    the original text file for a given shoe object and quantity
    '''
    # Modify the shoe data as the object in 'shoe_list'
    shoe.quantity += qty

    # Modfy the shoe data as the string in 'inventory.txt'
    try:
        with open('inventory.txt','r') as file:
            lines = file.readlines()
            shoe_info = lines[shoe.file_index].split(',')
            shoe_info[4] = str(shoe.quantity)
            lines[shoe.file_index] = ','.join(shoe_info) + '\n'
        with open('inventory.txt', 'w') as file:
            file.writelines(lines)
    except FileNotFoundError:
        print('Could not find file "inventory.txt"')

def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    # Get headers and data, create table, and print
    headers = ['Country', 'Code', 'Product', 'Cost', 'Quantity']
    data = [[a, b, c, d, e] for a, b, c, d, e in shoe_list]
    table = tab.tabulate(data, headers)
    print(f'\n{table}')

def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    # Find shoe with lowest quantity and print info
    shoe_list.sort(key= lambda shoe: shoe.quantity)
    shoe_least = shoe_list[0]
    median_qty = s.median([i.quantity for i in shoe_list])
    ave_qty = s.mean([i.quantity for i in shoe_list])
    print(f'\nThe shoe product with the lowest quantity is:\n{shoe_least}')
    print(f'\nThe median shoe product quantity is:    {median_qty}')
    print(f'The average shoe product quantity is:   {ave_qty:.2f}')

    # Get user input for requesting restock and update data
    if user_input("\nWould you like to order more of this shoe?"):
        amt = user_input("\nHow many would you like to order?", "numeric")
        modify_shoes_data(shoe_least, amt)
        print(f'\nA quantity of {amt} ordered for shoe {shoe_least.code}.')
    else:
        print("\nRestock not ordered.")


def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    #Get user to select a shoe from those available
    code_prompt = '\nPlease select/type the code of the product to search:'
    shoe_codes = [shoe.code for shoe in shoe_list]
    code = user_input(code_prompt, shoe_codes)
    
    #Loop through shoe_list to find the shoe and print details
    for i in shoe_list:
        if i.code == code:
            print(f'\nSee below details of the selected shoe:\n{i}')

def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    #Get table data, create table and print (also get total value)
    headers = ['Country', 'Code', 'Product', 'Value']
    data = [[a, b, c, d*e] for a, b, c, d, e in shoe_list]
    table = tab.tabulate(data, headers)
    print(f'\n{table}')
    total_val = sum(row[-1] for row in data)
    print(f'\nThe total value of all shoes is: {total_val}')
    
def highest_qty():
    '''
    Determines the product with the highest quantity and
    prints this shoe as being for sale.
    '''
    shoe_list.sort(key= lambda shoe: shoe.quantity)
    print(f'\n\tSHOE FOR SALE!!!\n{shoe_list[-1]}')

#==========Main Menu=============

if __name__ == "__main__":
    '''
    Create a menu that executes each function above.
    This menu should be inside the while loop. Be creative!
    '''
    # List of all relevant functions
    func_lst = ['view_all()',
                'value_per_item()',
                're_stock()',
                'highest_qty()',
                'search_shoe()']

    # Read data into list before asking for input to avoid failure of other
    # functions
    if read_shoes_data() != FileNotFoundError:

        prompt = '\nPlease select a function to run (number or text):'
        while True:

            # Ask user to select a function to run then run the relevant function
            select = user_input(prompt, func_lst)
            match select:
                case 'view_all()':
                    view_all()
                case 'value_per_item()':
                    value_per_item()
                case 're_stock()':
                    re_stock()
                case 'highest_qty()':
                    highest_qty()
                case 'search_shoe()':
                    search_shoe()

            # Check if user wants to continue, break/exit if false
            if user_input('\nWould you like to continue?', "bool") == False:
                print('\nProgram ended.\n')
                break
    


