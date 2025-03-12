vars_dict = {}
def lambda_handler(event):
     
     # 1. Handling ingestion of previously defined variables
     # This allows for the variables to be used.
     metadata = event['metadata']
     for key, value in metadata.items():
          globals()[key] = value
     
          
     #########
     # Main body function goes here @ggnadiek :)
     #########
     
     # 2. Handling export of current and previously defined variables;
     # 3. Exporting variables (both from current and previous workflows)
     # This is ensured by the `event` variable.
     var_list = globals()
     # Note G: this is a bit ugly, but it works. I'll refactor this after.
     vars_dict_curr = { k: v for k, v in var_list.items() if not
               k.startswith('__') |
               k.startswith('json') |
               k.startswith('lambda_handler') |
               k.startswith('vars_dict')
          }
     for key, value in vars_dict_curr.items():
          if key == 'event':
               # Ensure that there's no overwritten data
               if vars_dict.get(key) == None:
                    vars_dict.update(value['metadata'])
          else:
               vars_dict.update({ key: value })
     print(vars_dict)
     

