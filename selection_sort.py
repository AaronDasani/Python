def selection_sort(a_list):
    print ("original list: ", a_list)
    for iteration in range(len(a_list)):
        minNum=a_list[iteration]
        for index1 in range(0+iteration,len(a_list)):
            
            if minNum<a_list[index1]:
                minNum=minNum
            else:
                minNum=a_list[index1]
                a_list[iteration],a_list[index1]=a_list[index1],a_list[iteration]

    return  a_list
print(selection_sort([5,8,2,9,40,3,0,14]))