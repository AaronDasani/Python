class Node:
    def __init__(self,data):
        self.data=data
        self.next=None
        self.prev=None


class double_link_list:
    def __init__(self):
        self.head=None
    def add_node(self,data):
        runner=self.head

        if self.head is None:
            new_node=Node(data)
            self.prev=None
            self.head=new_node
        else:
            newNode=Node(data)
            while runner.next!=None:
                runner=runner.next
            newNode.prev=runner
            runner.next=newNode
            newNode.next=None
    
    def insertNode_After(self,key,data):
        runner=self.head
        
        while runner:        
            if runner.data==key and runner.next is None:#if there is only the head is present in the list
                self.add_node(data)
                return self
            elif runner.data==key:#if there is more than one node in the list
                new_node=Node(data)
                temp=runner.next
                new_node.prev=runner
                new_node.next=temp
                runner.next=new_node
                temp.prev=new_node
                return self
            runner=runner.next

    def insertNode_Before(self,key,data):
        
        runner=self.head
        while runner:
            
            if runner.prev is None and runner.data==key:#if we are inserting a node before the head
                new_node=Node(data)
                runner.prev=new_node
                new_node.next=runner
                new_node.prev=None
                self.head=new_node
                return self

            elif runner.data==key:
                new_node=Node(data)
                temp=runner.prev
                new_node.next=runner
                new_node.prev=temp
                runner.prev=new_node
                temp.next=new_node
                return self

            runner=runner.next

    def delete_node(self,key=None,node=None):
        runner=self.head

        while runner:

            if runner.prev is None and (runner.data==key or runner==node):
                if not runner.next:# if there is only head in the list
                    runner=None
                    self.head=None
                    return
                else:
                    temp=runner.next              
                    runner.next=None
                    temp.prev=None
                    runner=None
                    self.head=temp
                    return self
            elif runner.data==key or runner==node:
                if runner.next is not None:
                    
                    nextNode=runner.next
                    prevNode=runner.prev
                    prevNode.next=nextNode
                    nextNode.prev=prevNode
                    runner.next=None
                    runner.prev=None
                    runner=None
                    return self
                else:
                    temp=runner.prev
                    temp.next=None
                    runner.prev=None
                    runner=None
                    return self

            runner=runner.next

    def Reverse_list(self):
        runner=self.head
        temp=None
        while runner:
            temp=runner.prev
            runner.prev=runner.next
            runner.next=temp

            runner=runner.prev
        if temp:
            self.head=temp.prev

    def remove_duplicate(self):
        runner=self.head
        data_Seen=[]
        
        while runner:
            if runner.data not in data_Seen:
                data_Seen.append(runner.data)
                runner=runner.next
            else:
                next_node=runner.next
                self.delete_node(node=runner)
                runner=next_node


    def display_list(self):
        runner=self.head
        element_list=[]
        if self.head is not None:
            
            while runner.next!=None:
                element_list.append(runner.data)
                runner=runner.next
            element_list.append(runner.data)
            print(element_list)
        else:
            print("no data in double linked list")



dllist=double_link_list()
dllist.add_node(10)
dllist.add_node(3)
dllist.add_node(3)
dllist.add_node(5)
dllist.add_node(10)
dllist.add_node(8)
dllist.add_node(3)
dllist.add_node(20)


dllist.display_list()

dllist.insertNode_After(5,23)
dllist.insertNode_Before(10,99)
dllist.delete_node(10)
dllist.remove_duplicate()
dllist.Reverse_list()


dllist.display_list()