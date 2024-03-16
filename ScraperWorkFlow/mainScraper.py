import time 
import pandas as pd
import importlib.util
import os


"""
Below loads the googleNews function from the google.py file in the SearchEngines folder dynamically.
This is done because the directory of the executing python file is not known and the google.py file is not in the same directory as the executing file.

"""


def import_module_from_directory(directory, module_name):
    file_path = os.path.join(directory, module_name + ".py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module


directory = os.path.dirname(os.path.abspath(__file__))

google = import_module_from_directory(os.path.join(directory, "SearchEngines"), "google")

def mainWorkFlow():
    df1 = google.googleNews("Space Research")
    df2 = google.googleNews("Space Travel")
    
    allDF = [df1, df2]


    allDF = pd.concat(allDF)
    
    return allDF




if __name__ =="__main__":
    start = time.time()
    df = mainWorkFlow()
    print(df)
    end = time.time()
    print("\n")
    print("Time taken by mainScraper was: ", end-start)
    print("\n")