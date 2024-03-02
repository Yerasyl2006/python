import os 
   
os.getcwd() 

#print files and directories
print("Files and directories in '", os.getcwd() , "' :")  
with os.scandir(os.getcwd() ) as it:
    for x in it: 
            print(x.name)
            
#print directories
print("Directories:") 
with os.scandir(os.getcwd() ) as it:
    for entry in it: 
        if entry.is_dir():
            print(entry.name)

#print files
print("Files:")   
with os.scandir(os.getcwd() ) as it:
    for entry in it: 
        if not entry.is_dir(): 
            print(entry.name)