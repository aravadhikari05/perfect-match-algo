import pandas as pd

#Data is taken from google form (csv file)
#Data will be organized as timestamp as first column, then rest of the columns
#Set name or email as column index

#TODO: create a better mock_data.csv to test our code 
#TODO: convert all data to lowercase (example would be when a question asks for 3 words to describe yourself and they enter upercase) - DONE
#TODO: may need to bin some types of data. example: words to describe yourself will have too many unique values, so create an algorithm to bin them
#      another example is age or height depending on how the data is entered 


def process_data(data_file='mock_data.csv'):
    
    data = pd.read_csv(data_file)

    #manually rename the columns from questions to values that are easy to work with
    #example code to test
    column_names = {'Name': 'name', 
                    'Age': 'age', 
                    'Gender': 'gender', 
                    'Do you prefer the same age?': 'prefer_same_age', 
                    'Preferences': 'preferences'
                }

    
    data = data.rename(columns=column_names)
    #data.timestamp = pd.to_datetime(data.timestamp)
    data.set_index('name', inplace=True) #set this to name or email
    #makes data lowercase
    data = data.apply(lambda col: col.str.lower() if col.dtype == 'object' else col)
    print(data.head())
    
    return data
