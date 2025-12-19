import json

class Clothes :
      def __init__(self, name : str, category : str):
            self.name = name 
            self.category = category
            
      def __repr__(self):
         return f"Prenda : {self.name} , Categoría : {self.category}"
     
#función encargada de cargar los datos del json    
def load_clothes_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)   
    except   FileNotFoundError:
        print(f"ERROR : El archivo {file_path} no aparece.Verifique la ubicación")
        return []
    
    clothes_list = []
    for category, items  in data.items() :
        for item_name in items:
            clothes_obj = Clothes(
              name = item_name.strip(),
              category= category.strip()
            )
            clothes_list.append(clothes_obj)
            
    return clothes_list        
      
                