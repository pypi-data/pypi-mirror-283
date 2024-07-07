def treeshow(dictionary, indent="", last=True):
    keys = list(dictionary.keys())
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            newIndent = indent + "    "
            print(indent + "└── ", end="")
            lastChild = True
        else:
            newIndent = indent + "│   "
            print(indent + "├── ", end="")
            lastChild = False
        if isinstance(dictionary[key], dict):
            print(key + ":")
            treeshow(dictionary[key], newIndent, lastChild)
        else:
            value = dictionary[key]
            if isinstance(value, list):
                value_str = ", ".join(map(str, value))
                print(key + ": " + value_str)
            elif value is not None:
                print(key + ": " + value)
            else:
                print(key + ": None")