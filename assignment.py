sample_text = """What is Python? Executive Summary

Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. Its high-level built in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, as well as for use as a scripting or glue language to connect existing components together. Python's simple, easy to learn syntax emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available in source or binary form without charge for all major platforms, and can be freely distributed.

Often, programmers fall in love with Python because of the increased productivity it provides. Since there is no compilation step, the edit-test-debug cycle is incredibly fast. Debugging Python programs is easy: a bug or bad input will never cause a segmentation fault. Instead, when the interpreter discovers an error, it raises an exception. When the program doesn't catch the exception, the interpreter prints a stack trace. A source level debugger allows inspection of local and global variables, evaluation of arbitrary expressions, setting breakpoints, stepping through the code a line at a time, and so on. The debugger is written in Python itself, testifying to Python's introspective power. On the other hand, often the quickest way to debug a program is to add a few print statements to the source: the fast edit-test-debug cycle makes this simple approach very effective. """

#defining class for first part where it is easy to call and manage ETL methods

class first_part():   

    #initializing the paths as an attribute to an instance of this class 
    
    def __init__(self, path1, path2):    
        self.path1 = path1
        self.path2 = path2

    #transformer method for processing the string, converting characters to upper and sending to load
    
    def transformer(self,data):
        data = data.upper()
        self.load(data)

    #extract method for reading text from file and sending it to transformer

    def extract(self):
        try:
            f = open(self.path1,"w+")
            if f.read() == "":
                print("Sending a sample text to transformer as the default file is empty \n")
                self.transformer(sample_text)
            else:
                self.transformer(f.read())
            f.close()
        except Exception as e:
            print('could not read file: ' + str(e))

    #load method to write string to file in another directory

    def load(self,data):
        try:
            f = open(self.path2,"a")
            f.write(data)
            f.close()
        except Exception as e:
            print('could not write file: ' + str(e))

# parent class of transformation for second_part to inherit which contains all the logic for transformer

class transformation():

    # method for getting unique words out of data

    def unique_word(self, data):
        count = {}
        processed_string = []

        temp_word = ""

        for char in data:
            
            if ord(char.lower()) in range(97,122):
                temp_word += char  
            else:
                if temp_word == "":
                    pass
                else:
                    processed_string.append(temp_word)
                    temp_word = ""
          
        for word in processed_string:
            if word.lower() in count.keys():
                count[word.lower()] += 1
            else:
                count[word.lower()] = 1
                
        return self.dict_to_str(count)

    #method to recieve dictionary as data and converting it to string for loading in another file
        
    def dict_to_str(self, data):
        data = sorted(data.items() , reverse=True, key=lambda x: x[1])
        summary = "Summary is -->\n\n"
        for elements in data:
            temp = str(elements[0]) + " -> " + str(elements[1]) +"\n\n"
            summary += temp
        return summary

#class for second_part which inherits transformation    
        
class second_part(transformation):

    #initializing the paths as an attribute to an instance of this class

    def __init__(self, path1, path2):    
        self.path1 = path1
        self.path2 = path2

    #transformer method to get unique words and sending the summary string to load method
        
    def transformer(self, data):
        summary = self.unique_word(data)
        self.load(summary)


    #extract method for reading text from file and sending it to transformer

    def extract(self):
        try:
            f = open(self.path1,"w+")
            data = f.read()
            if data == "":
                print("Sending a sample text to transformer as the default file is empty \n")
                self.transformer(sample_text)
            else:
                self.transformer(data)
            f.close()
        except Exception as e:
            print('could not read file: ' + str(e))


    #load method to write string to file in another directory

    def load(self,data):
        try:
            f = open(self.path2,"a")
            f.write(str(data))
            f.close()
        except Exception as e:
            print('could not write file: ' + str(e))

#importing path for checking valid paths

import os.path
from os import path

#while loop to continously run the program

while True: 

    #parts method to select the part to be executed

    def parts(path1,path2):
        print("Select the part that you want to execute ")
        try:
            part = int(input("1 -> 1st Part" + "\n" + "2 -> 2nd Part " + "\n"))
            if part == 1:
                first = first_part(path1,path2)
                print("Successfully Added \n")
                first.extract()
            elif part == 2:
                second = second_part(path1,path2)
                print("Successfully Added \n")
                second.extract()
            else:
                raise Exception("Invalid selection!!! \n")
        except Exception as e:
            print("Please try again -> Error ->",e)
            parts(path1,path2)

    #main function which runs again and again till user exit

    def main():
        print("Welcome to the terminal application of a simple ETL Process \n")
        print("Select if you would like to add a custom file path & data or a predefined data ")
        try:
            test = int(input("1 -> Custom" + "\n" + "2 -> Predefined " + "\n"))
            if test == 1:
                path1 = str(input("Enter the path for the file to read from directory. \n Note - If you entered an incorrect value then the file will be saved as that name. You will have to change the content manually. \n"))
                path2 = str(input("Enter the path for the file to write to directory \n Note - In this case also an incorrect path will automatically create a file and try to write content into it \n"))
                parts(path1,path2)
            elif test == 2:
                path1 = 'C:/Users/sriji/Desktop/py.txt'
                path2 = 'C:/Users/sriji/Desktop/new/warehouse.txt'
                parts(path1,path2)
            else:
                raise Exception("Invalid selection!!! \n")
        except Exception as e:
            print("Please try again -> Error ->",e)
            main()

    main()

    #a prompt for user to either delete, end or continue the program
            
    flag1 = 0
    while True:        
        print("Would you like to end the program, delete the content of a file or continue the program? \n")
        final = input("1 -> End" + "\n" + "2 -> Delete " + "\n" + "3 -> Continue" + "\n")
        if final not in ['1','2','3']:
            print("Enter a valid number!!! \n")
        elif int(final) == 1:
            print("Successfully Exited")
            flag1 = 1
            break
        elif int(final) == 2:
            while True:
                file_path = str(input(("Enter the file path \n")))
                if path.exists(file_path) == True:
                    open(file_path, 'w').close()
                    print("Successfully Deleted \n")
                    break
                else:
                    print("Please enter a valid path \n")
            break
        else: 
            main()
            break
    if flag1 == 1:
        break

    #another prompt for user to end the program
            
    flag2 = 0
    while True:
        print("Would you like to end the program?")
        ques = str(input("Type yes to end or no to continue \n"))
        if ques in ["yes","y","Yes","Y"]:
            flag2 = 1
            break
        elif ques in ["no","n","No","N"]:
            break
        else:
            print("Your input is invalid. Please try again!!! \n")
    if flag2 == 1:
        print("Successfully Exited")
        break
    

#for future mysql queries we can use petl package for extracting, transforming and loading tables of data.

# # join tables
#     expenses = petl.outerjoin(exchangeRates,expenses,key='date')

#     # fill down missing values
#     expenses = petl.filldown(expenses,'rate')

#     # remove dates with no expenses
#     expenses = petl.select(expenses,lambda rec: rec.USD != None)

#     # add CDN column
#     expenses = petl.addfield(expenses,'CAD', lambda rec: decimal.Decimal(rec.USD) * rec.rate)
    
#     # intialize database connection
#     try:
#         dbConnection = pymssql.connect(server=destServer,database=destDatabase)
#     except Exception as e:
#         print('could not connect to database:' + str(e))
#         sys.exit()

#     # populate Expenses database table
#     try:
#         petl.io.todb (expenses,dbConnection,'Expenses')
#     except Exception as e:
#         print('could not write to database:' + str(e))
#     print (expenses)