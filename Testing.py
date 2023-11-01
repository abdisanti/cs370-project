import pickle 

data1 = [
    0,
    0, 
    -0.0277309682187731,      
    -0.09960145912309563, 
    0.020192737763154757, 
    0.09928674629854803, 
]
class user_data: 
    def __init__(self, PackNum: int, Marker: int, O1: float, O2: float, T3: float, T4: float):
        self.PackNum = PackNum 
        self.Marker = Marker 
        self.O1 = O1
        self.O2 = O2 
        self.T3 = T3
        self.T4 = T4
    
    def desribe_user_data(self): 
        print(self.PackNum, self.Marker, self.O1, self.O2, self.T3, self.T4)

user_info = user_data()

print(user_info)

if __name__ == '__main__':

    userData: user_data(data1)
    userData.user_data()
    
    with open('BrainDataFile.pkl', 'wb') as file: 
        pickle.dump(user_info, file )
        file.close()

    with open('BrainDataFile.pkl', 'rb') as f: 
        unpickle_data = pickle.load(f)
        #Check to make sure unpickled data is deseralized 
        print(unpickle_data)