
def insertion_sort(a_list):
    for index in range(1,len(a_list)):

        currentvalue = a_list[index]
        position = index

        while position>0 and a_list[position-1]>currentvalue:
            a_list[position]=a_list[position-1]
            position = position-1

        a_list[position]=currentvalue
    return a_list
sorted_List=insertion_sort([6,5,7,4,2,9,1,3,8])
print (sorted_List)