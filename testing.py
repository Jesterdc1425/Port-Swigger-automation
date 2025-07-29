""" 
usernames=[]
with open("username.txt",'r') as file:
    for i in file:
        usernames.append(i.strip())
print(usernames)
for item in usernames:
    for j in range(0,5):
        print(f"{item} - {j}")
    

for i in range(1111,9999):
    print(i,end='') """


# winer:password -> base64 encode

# carlos:md5 encode

#carlos+password_file+encode


import hashlib 
text = "peter"

md5= hashlib.md5(text.encode()).hexdigest()
print(md5)

