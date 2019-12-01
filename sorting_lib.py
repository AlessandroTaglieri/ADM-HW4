# I have Wrote two versions
# the first one follow more the rules of count sorting and the O(n) time 

def convert_w_2_n(word, length):
    temp = ''
    split_word = list(word)
    for i in range(length):
        try:
            temp = temp + str(mapper[split_word[i]])
        except:
            temp = temp + '00'
            i
    return int(temp)



mapper = {}
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for i in range(len(alphabet)):
    mapper[alphabet[i]] = i + 10 
    
    
x = input('Enter the words, seperated by comma(,)').split(',')  # it's the input of the words
x_2 = x.copy()

# Finding the longest word
max_length = 0
for i in x:
    if max_length < len(list(i)):
        max_length = len(list(i))
    

# Turning words to numbers
for i in range(len(x)):
    x[i] = convert_w_2_n(x[i], max_length)
    

#Normalize between 0 to 1000

mx = max(x)
mn = min(x)
for i,j in enumerate(x):
    x[i] = int((10**(3))*(j-mn)/(mx-mn))
    
    

max_int = max(x)
#min_int = min(x)
aux_array = [0]*(max_int+1)
aux_array_2 = aux_array



# Step 1 : counting
for i in x:
    aux_array[i] = aux_array[i] + 1
    
# Step 2 : comulating
aux_array_2[0] = aux_array[0]
for i in range(1,max_int+1):
    aux_array_2[i] = aux_array_2[i-1] + aux_array[i]
    
# Sorting
final_list = ['']*len(x)
for i in reversed(range(len(x))): #e.g:  i = 2, 1, 0 
    final_list[aux_array_2[x[i]]-1] = x_2[i]
    aux_array_2[x[i]] = aux_array_2[x[i]] -1
    
    
    
final_list



