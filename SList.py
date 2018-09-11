
class Node:
    def __init__(self,value=None):
        self.value=value
        self.next=None
    
class SList:
    def __init__(self):
        self.head=Node()
         
    def length(self):
        runner=self.head
        count=0

        while runner.next!=None:
            count+=1
            runner=runner.next
        return count

    def add_node(self,value):
        runner=self.head
        new_node=Node(value)

        while runner.next !=None:
            runner=runner.next

        runner.next=new_node

    def display_node(self):
        runner=self.head
        a_list=[]

        while runner.next!=None:
            runner=runner.next
            a_list.append(runner.value) 

        print (a_list)

    def remove_node(self,value):
        runner=self.head

        while runner.next!=None:
            previous_node=runner
            runner=runner.next
            if runner.value==value:
                previous_node.next=runner.next 
                return 
    def insert_node(self,value,index):#inset node at specific index

        if index>=self.length():
            print("index:"+" "+str(index)+" "+ "is out of bound")
            return None

        runner=self.head
        new_node=Node(value)
        current_index=0

        while runner.next !=None:
            previous_node=runner
            runner=runner.next
            if current_index==index:
                previous_node.next=new_node
                new_node.next=runner
                return

            current_index+=1


my_list=SList()

my_list.add_node(4)
my_list.add_node(6)
my_list.add_node(100)
my_list.add_node(79)
my_list.display_node()
my_list.remove_node(4)
my_list.insert_node(45,2)
my_list.display_node()