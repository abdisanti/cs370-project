import pickle 

#Get mock data to simulate using headband store into data 
file = open('tools/MockBrainData1.pkl', 'r')
data = file.readlines()
file.close()

if __name__ == '__main__':

    #Pickle testing: Send mock data to pickle file as if it were real data, pickle it then unpickle it/
    with open('BrainDataFile.pkl', 'wb') as file: 
        pickle.dump(data, file)
        file.close()

    with open('BrainDataFile.pkl', 'rb') as f: 
        unpickle_data = pickle.load(f)
        #Check to make sure unpickled data is deseralized 
        print("Unpickled Data: \n\n")
        print(unpickle_data)
