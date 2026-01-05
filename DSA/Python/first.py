#Encapsulation
class car:
    count=0
    def __init__(self,ubrand,umodel): # Encapsulation
        self.__brand=ubrand # __ used to make data as privete then other user if user want access this they want call get_brand() function
        self.__model=umodel

        car.count+=1
    def fullname(self):
        print(self.__brand,self.__model)
        #return f"{self.brand},{self.model}"

    def get_brand(self): # this emthod used to use  brand data without this can not access brand 
        return self.__brand

    
    def fuel_type(self):
        return "petrol or desel"
    
    @staticmethod
    def totalcar(): # make it only for super class not want self staic can access by only main calss method no any other can access this
        return car.count# child class can be access this using own class name and super class name

    def model(self):
        return self.__model
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Inheritance
class electric(car):  # inharitance = use super class data in this calss using super() and __init__() method and add more data as per request
    def __init__(self,__brand,__model,battrary):
        self.battrary=battrary
        super().__init__(__brand,__model) # use to call super method data
      

    def full(self):
       # print(self.__brand,self.model,self.battrary)
         return self.get_brand()
        
    def fuel_type(self):
        return "electric"

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#same type&name of function in both class but work are diffent each other
#eg- fule_type: in electric and car both but work deferent


# mycar=car("toyota","fortuner")
# mycar1=car("toyota1","fortuner1")
# mycar2=car("toyota2","fortuner2")
# mye=electric("toyota","fortuner",32)
#mycar.model="city"

#print(mycar.model())


class battary:
    def battarys(self):
        return "batatrys mkv"


class engin:
    def engins(self):
        return "BMW"
    pass


class electrics(battary,engin,car):
    pass


mynew=electrics("tesala","EV5")
#print(mynew.battarys ())

import keyword
print(keyword.kwlist)



# print(electric.totalcar()) # static method 
# print(car.totalcar())



# print(mycar.fuel_type())
# print(mye.fuel_type())
# print(car.count)

# print(mye.full())
# print(mycar.get_brand())



#print(mycar.brand)
#print(mycar.fullname())

# ele=electric("tata","curv",300)
# print(ele.battrary)
# print(ele.fullname())