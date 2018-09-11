
import unittest


class Product:
    def __init__(self,item_name,price,tax=0,weight="Not Specify",brand="Not Specify",reason_for_return="like new"):
        status="for sale"
        self.item_name=item_name
        self.price=price
        self.weight=weight
        self.brand=brand
        self.tax=tax
        self.reason_for_return=reason_for_return.lower()
        self.status=status
        

    def sell(self):
        self.status="Sold"
        Product.display_info(self)
        return self.item_name+" Status: "+self.status

    def add_tax(self):
        
        self.price=self.price*(self.tax+1)
        Product.display_info(self)

        return self.price

    def return_item(self):
   
        if self.reason_for_return=="defective":
            self.status="Defective"
            self.price=0

        elif self.reason_for_return=="like new":
            self.status="For sale"

        elif self.reason_for_return=="opened":
            self.status="Used"
            self.price=self.price/1.2
            print ("\n","***** " +"20%"+" discount****","\n")

        return self.item_name+" Status: "+self.status

        
    def display_info(self):

        print ("Item_name: "+str(self.item_name),"\n", "price: $"+str(self.price),"\n","Brand: "+str(self.brand),"\n","Weight(lbs): "+str(self.weight),"\n","Status: "+str(self.status),"\n")
  
        return self


class ProductTest(unittest.TestCase):
    def setUp(self):
       self.product1=Product(item_name="cake",price=50,tax=0.07,weight=0.2,brand="addidas",reason_for_return="")
       self.product2=Product(item_name="candies",price=100,tax=0.07,weight=0.2,brand="addidas",reason_for_return="opened")

    def test_tax(self):
        
        self.assertEqual(self.product1.add_tax(),53.5)
        self.assertEqual(self.product2.add_tax(),107)
    def test_returnItem(self):
        self.assertEqual(self.product1.return_item(),"cake Status: for sale")
        self.assertEqual(self.product2.return_item(),"candies Status: Used")
        self.assertNotEqual(self.product2.return_item(),"candies Status: Defective")
    def test_Sold(self):
        self.assertEqual(self.product1.sell(),"cake Status: Sold")
        self.assertEqual(self.product2.sell(),"candies Status: Sold")
        self.assertNotEqual(self.product1.sell(),"candies Status: for sale")

    
if __name__=='__main__':
    unittest.main()