import object_Product

cheesecake=object_Product.Product(item_name="cheesecake",price=5,tax=0.07,weight=0.2,brand="Cheesecake Factory",reason_for_return="")
chips=object_Product.Product(item_name="Chips",price=50,tax=0.07,weight=0.2,brand="chipZo",reason_for_return="")
shoes=object_Product.Product(item_name="Shoes",price=100,tax=0.07,weight=1,brand="addidas",reason_for_return="")
Tv=object_Product.Product(item_name="TV",price=500,tax=0.07,weight=30,brand="microsoft",reason_for_return="defective")

cheesecake.add_tax()
chips.add_tax()
shoes.add_tax()
Tv.add_tax()

Tv.return_item()
Tv.display_info()
