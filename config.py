import json

class config():

    def __init__(self,json_filepath="config.json"):
        self.json_save = json_filepath
    
    def get(self,key):
        obj = self._json_dict()[key]
        return obj
        
    def append(self,obj):
        # open list of networks
        config_dict = self._json_dict()

        for key, data in obj.items():
            item = self.get(key)
            #print(data.values())
            for i in item:
                for value in data.values():
                    if value in i.values():
                        item.remove(i)
                        break
            item.append(data)
            # Open and read in the file
            config_dict.update({key:item})
        self.save_config(config_dict)

    def update(self,obj):
        config_dict = self._json_dict()

        for k,d in obj.items():
            config_dict.update({k:d})
        self.save_config(config_dict)

    def _json_dict(self):
        try:
            jfile = open(self.json_save)
            json_dict = json.load(jfile)
        except Exception as e:
            pass
        finally:
            jfile.close()
        return json_dict

    def save_config(self,json_dict):
        out_data = json.dumps(json_dict, sort_keys=True, indent=1) 
        try:
            with open(self.json_save,'w') as file:
                file.write(out_data)

        except Exception as e:
            pass
        
#test = config()
#test.append({"networks":{"network":"RGGCNN","password":"123456789"}})





