vars_dict = {}


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
            # or k.startswith("event")  # Commented out
            or k.startswith("metadata")
            or k.startswith("context")
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

    return {
        "metadata": vars_dict
    }
