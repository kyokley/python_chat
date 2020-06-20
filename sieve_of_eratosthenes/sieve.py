def get_list(number):
    
    if not isinstance(number, int):
        raise Exception('try something else') 
    
    result = []
    

    if number < 2:
            raise Exception('passing an integer less than two doesnt work.')


    for i in range(2, number + 1):  # 0, 1, 2, 3, ..., number
        if number < 2:
            raise Exception('passing an integer less than two doesnt work.')

        result.append(i)


    return result








def remove_multiples(sequence, number):
   
    result = []



    for element in sequence:

        if element % number == 0 and element > number:

            # This is a multiple

            pass

        else:

            # This is not a multiple

            result.append(element)



    return result  





def prime_list(number):
    
    long_list = get_list(number)



    idx = 0

    while idx < len(long_list):

        multiple_check = long_list[idx]
        
        long_list = remove_multiples(long_list, multiple_check)

        idx = idx + 1



    return long_list
