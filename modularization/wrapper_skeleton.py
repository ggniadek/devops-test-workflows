vars_dict = {}

def make_serializable(obj):
        """Recursively convert non-serializable objects (like DataFrames) into serializable ones."""
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            if isinstance(obj, pd.DataFrame):
                # Convert DataFrame to a list of records (or use another orient if preferred)
                return obj.to_dict(orient='records')
            elif isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            elif hasattr(obj, 'to_dict') and callable(obj.to_dict):
                return make_serializable(obj.to_dict())
            elif hasattr(obj, '__dict__'):
                return make_serializable(obj.__dict__)
            else:
                # As a last resort, return the string representation
                return str(obj)

def lambda_handler(event, context):
    # Handling ingestion of previously defined variables
    # Allows for the variables to be used.
    if "metadata" in event:
        metadata = event["metadata"]
        for key, value in metadata.items():
            globals()[key] = value

    #########
    # Main body function
    #########

    local_vars = locals()
    local_vars_dict_curr = {
        k: v
        for k, v in local_vars.items()
        if not (
            k.startswith("key")
            or k.startswith("value")
            or k.startswith("event")
            or k.startswith("metadata")
            or k.startswith("context")
            or k.startswith("make_serializable")
        )
    }

    # Handling export of current and previously defined variables
    # Exporting variables (both from current and previous workflows)
    var_list = globals()

    vars_dict_curr = {
        k: v
        for k, v in var_list.items()
        if not (
            k.startswith("__")
            or k.startswith("json")
            or k.startswith("lambda_handler")
            or k.startswith("vars_dict")
            or k.startswith("context")
            or k.startswith("types")
            or k.startswith("make_serializable")
        )
    }

    for key, value in vars_dict_curr.items():
        if key == "event":
            # Ensure that there's no overwritten data
            if vars_dict.get(key) is None:
                if "metadata" in value:
                    vars_dict.update(value["metadata"])
        else:
            vars_dict.update({key: value})

    for key, value in local_vars_dict_curr.items():
        vars_dict.update({key: value})
        
    for key, value in vars_dict.items():
        if not is_json_serializable(value):
            vars_dict.update({key: vars_dict[key].to_dict()})

    return {
        "metadata": make_serializable(vars_dict)
    }
