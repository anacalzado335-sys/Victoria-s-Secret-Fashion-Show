import json 

clothes = {
        "Ropa Interior " : ["sostén", "bragas","corsés", "bikinis"],
        "Línea Pink" : ["blusas", "deportiva", "juvenil"],
        "Calzado" : ["tenis" "tacón extremo"],
        "Accesorios" : ["collares", "aretes gigantes", "guantes","cinturones" ]      
        }

with open("clothes.json", 'w') as outfile:
    json.dump(clothes,outfile)
with open("clothes.json") as file:        
    data_clothes = json.load(file)

p = data_clothes.values()
for j in p :
    for i in j :
        print(i)