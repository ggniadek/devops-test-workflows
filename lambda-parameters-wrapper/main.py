vars_dict = {}
def lambda_handler(event, context):
     
     # 1. Handling ingestion of previously defined variables
     # This allows for the variables to be used.
     if 'metadata' in event:
          metadata = event['metadata']
          for key, value in metadata.items():
               globals()[key] = value
          
     #########
     # Main body function
     #########

     local_vars = locals()
     local_vars_dict_curr = { k: v for k, v in local_vars.items() if not
               k.startswith('key') |
               k.startswith('value') |
               # k.startswith('event') |
               k.startswith('metadata') |
               k.startswith('context')
          }

     # 2. Handling export of current and previously defined variables;
     # 3. Exporting variables (both from current and previous workflows)
     # This is ensured by the `event` variable.
     var_list = globals()
     # Note G: this is a bit ugly, but it works. I'll refactor this after.
     vars_dict_curr = { k: v for k, v in var_list.items() if not
               k.startswith('__') |
               k.startswith('json') |
               k.startswith('lambda_handler') |
               k.startswith('vars_dict') |
               k.startswith('context')
          }
     for key, value in vars_dict_curr.items():
          if key == 'event':
               # Ensure that there's no overwritten data
               if vars_dict.get(key) == None:
                    if 'metadata' in value:
                         vars_dict.update(value['metadata'])
          else:
               vars_dict.update({ key: value })
     for key, value in local_vars_dict_curr.items():
          vars_dict.update({ key: value})
     return {
          "metadata": vars_dict
     }

