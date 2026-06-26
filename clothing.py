import json

class Clothes :
      def __init__(self, name : str, category : str):
            self.name = name 
            self.category = category
            
      def is_accesory(self):
          return self.category.strip().lower() == "accesorios"
     
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
        clean_category = category.strip()
        for item_name in items:
            clothes_obj = Clothes(
              name = item_name.strip(),
              category= clean_category
            )
            clothes_list.append(clothes_obj)
            
    return clothes_list        
      
      
                