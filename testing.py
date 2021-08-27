import csv
users = "website/static/Users.csv"


with open(users, 'r+') as tokensFile:
    reader = csv.reader(tokensFile)
    feilds2 = ['Tokens']
    feilds = []
    feilds = next(reader)
    Tokens = []
    for row in reader:
        Tokens.append(row)
    print(Tokens)
    Tokens_main = ['887778378747834784']
    if Tokens_main in Tokens:
        print("Username taken")
    else:
        writer = csv.writer(tokensFile)
        writer.writerows(Tokens_main)
