def bubble_sort(list):
    while True:
        swap = False
        for i in range(len(list) - 1):
            if list[i] > list[i+1]:
                list[i],list[i+1] = list[i+1],list[i]
                swap = True
        if swap == False:
            return list

def merge_sort(list):
    if len(list) == 1:
        return list
    first = list[:len(list)//2]
    second = list[len(list)//2:]
    if len(first) > 1:
        first = merge_sort(first)
    if len(second) > 1:
        second = merge_sort(second)
    return(merge(first,second))

def merge(first,second):
    first_len = len(first)
    second_len = len(second)
    new_list = []
    while range(first_len+second_len):
        if len(first) > 0:
            element1 = first[0]
        else:
            element1 = None

        if len(second) > 0:
            element2 = second[0]
        else:
            element2 = None
        

        if element1 == None:
            new_list.extend(second)
            return(new_list)
        elif element2 == None:
            new_list.extend(first)
            return(new_list)

        if element1 > element2:
            new_list.append(element2)
            second = second[1:]
        else:
            new_list.append(element1)
            first = first[1:]
    return new_list


print(merge_sort([38, 27, 43, 3, 9, 82, 10]))  # [3, 9, 10, 27, 38, 43, 82]
print(merge_sort([5, 1, 4, 2, 8]))              # [1, 2, 4, 5, 8]
print(merge_sort([1]))                           # [1]
print(merge_sort([3, 1]))                        # [1, 3]