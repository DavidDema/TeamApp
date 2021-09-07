EVENT = "events!A2:U"
row = 2

string = EVENT.split("!")[0]+"!A"+ str(row) + ":U" + str(row)

print(string)