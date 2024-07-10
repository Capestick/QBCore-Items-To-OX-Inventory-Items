import re
import ast
import os
import sys

def transform_data(input_string):
    # Regex pattern to match both formats of Lua table definitions
    pattern1 = r"\['(\w+)'\]\s*=\s*{([^}]*)}"
    pattern2 = r"(\w+)\s*=\s*{([^}]*)}"
    
    # Find all matches in the input string
    matches = re.findall(pattern1, input_string, re.MULTILINE) + re.findall(pattern2, input_string, re.MULTILINE)
    
    output = []

    for match in matches:
        item_name = match[0] if match[0] else match[1]
        item_properties = match[1]

        # Clean up the properties string
        properties_dict = {}
        pairs = re.findall(r"\['?(\w+)'?\]\s*=\s*([^,]+),?", item_properties)
        
        for key, value_str in pairs:
            try:
                value = ast.literal_eval(value_str.strip())
            except (ValueError, SyntaxError):
                value = value_str.strip()
            properties_dict[key] = value

        # Use the item_name as the label
        label = item_name.lower()
        
        # Create the transformed dictionary
        transformed_dict = {
            'label': label,
            'weight': properties_dict.get('weight', 0),
            'close': properties_dict.get('shouldClose', False),
            'consume': 1 if properties_dict.get('useable', False) else 0
        }
        
        # Format the transformed dictionary to the required output format
        transformed_string = f"\t['{item_name}'] = {{\n"
        for key, value in transformed_dict.items():
            # Convert boolean values to lowercase strings
            if isinstance(value, bool):
                value = str(value).lower()
            transformed_string += f"\t\t{key} = {repr(value)},\n"
        transformed_string += "\t},"
        
        output.append(transformed_string)
    
    return "\n".join(output)

def main():
    user_input = input("Have You Added Your QB-Items To the Script?     Yes / No: ")

    if user_input == 'no':
        # Get the absolute path of the script
        script_file = os.path.abspath(__file__)
        
        # Open the script file in the default text editor
        if sys.platform.startswith('win'):
            os.system(f'start "" "{script_file}"')
        elif sys.platform.startswith('darwin'):
            os.system(f'open "{script_file}"')
        elif sys.platform.startswith('linux'):
            os.system(f'xdg-open "{script_file}"')
        else:
            print(f"Unsupported platform: {sys.platform}. Please open {script_file} manually.")
        
        print("Please edit the 'input_data' with your qb core items for it to work and run it again.")
        sys.exit()  # Exit the script after opening the file

    elif user_input != 'yes':
        print("Invalid input. Please enter 'yes' or 'no'.")
    
    # Input data containing Lua-like table definitions
    input_data = """
    ['cluckin_bucket'] = {['name'] = 'cluckin_bucket', ['label'] = 'cluckin Bucket', ['weight'] = 1000, ['type'] = 'item', ['image'] = 'gn_cluckin_bucket.png', ['unique'] = false, ['useable'] = true, ['shouldClose'] = true, ['combinable'] = nil, ['description'] = 'Contains Meal with Toy'},
    ["diamond"] = {
        ["name"] = "diamond",
        ["label"] = "Diamond",
        ["weight"] = 150,
        ["type"] = "item",
        ["image"] = "diamond.png",
        ["unique"] = false,
        ["useable"] = false,
        ["shouldClose"] = false,
        ["combinable"] = nil,
        ["description"] = ""
    },
    md_quarter = { name = 'md_quarter', label = 'Quarter', weight = 25, type = 'item', image = 'md_quarter.png', unique = false, useable = false, shouldClose = true, combinable = nil, description = nil },
    """
    
    transformed_data = transform_data(input_data)
    
    # Write the transformed data to a file
    with open('transformed_data.txt', 'w') as file:
        file.write(transformed_data)
    
    # Print completion message with creator details
    print(r"""
  Kyan Made this! 

  Discord Solo_Capestick
  Github Capestick

  Thanks for using!                                          
    """)
    
    print("Transformation complete! Check the 'transformed_data.txt' file for the result.")

if __name__ == "__main__":
    main()