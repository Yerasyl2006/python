def unique(input_list):
    unique_list = []
    for i in list1:
        if i not in unique_list:
            unique_list.append(i)

    return unique_list

list1 = input().split()
print(unique(list1))