with open ('username.txt','r') as file:
    a = file.read()
    if 'athena' in a:
        print('found')
     
    