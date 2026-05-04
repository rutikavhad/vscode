import re
def read_c_file(filename):
    with open(filename, "r") as file:
        return file.read()

def clean_code(code):
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
    return code

def find_inline_functions(code):
    return re.findall(r'\b(?:static\s+)?inline\s+\w+\s+(\w+)\s*\(', code)

def extract_functions(code):
    pattern = re.compile(
        r'(\w[\w\s\*]*?)\s+(\w+)\s*\(([^)]*)\)\s*\{([\s\S]*?)\}',
        re.MULTILINE
    )
    return pattern.findall(code), pattern.sub('', code)

def get_global_variables(code):
    globals_set = set()

    matches = re.findall(r'\b(int|float|double|char|long|short|unsigned|bool)\s+([^;]+);', code)

    for var_type, var_list in matches:
        for var in var_list.split(","):
            var = var.strip()
            var = re.sub(r'=.*', '', var)

            name = re.match(r'[a-zA-Z_]\w*(\[\w*\])?', var)
            if name:
                globals_set.add((var_type, name.group()))

    return globals_set

def get_local_variables(function_body):
    locals_set = set()

    matches = re.findall(r'\b(int|float|double|char|long|short|unsigned|bool)\s+([^;]+);', function_body)

    for var_type, var_list in matches:
        for var in var_list.split(","):
            var = var.strip()
            var = re.sub(r'=.*', '', var)

            name = re.match(r'[a-zA-Z_]\w*(\[\w*\])?', var)
            if name:
                locals_set.add((var_type, name.group()))
                
    loop_vars = re.findall(r'for\s*\(\s*(int|float|double|char|long|short|unsigned|bool)\s+(\w+)', function_body)
    for v in loop_vars:
        locals_set.add(v)

    return locals_set
    
def get_function_calls(function_body, func_name):
    calls = set(re.findall(r'\b(\w+)\s*\(', function_body))
    calls.discard(func_name)

    ignore = {
        "printf", "scanf", "sizeof",
        "if", "for", "while", "switch", "return"
    }

    return calls - ignore


#main
def main():
    code = read_c_file("input.c")
    code = clean_code(code)

    inline_functions = find_inline_functions(code)

    functions, code_without_funcs = extract_functions(code)
    print("GLOBAL VARIABLES:")
    global_vars = get_global_variables(code_without_funcs)

    if not global_vars:
        print("  None")
    else:
        for var in sorted(global_vars):
            print("  Type:", var[0], "Name:", var[1])

    print("Total Global Variables:", len(global_vars))

    print("\nFUNCTIONS:")

    for return_type, func_name, params, body in functions:
        print("\nFunction Name:", func_name)
        print("Return Type:", return_type)

        print("Parameters:")
        if params.strip() == "":
            print("  None")
        else:
            for p in params.split(","):
                print(" ", p.strip())
        print("Local Variables:")
        local_vars = get_local_variables(body)

        if not local_vars:
            print("  None")
        else:
            for var in sorted(local_vars):
                print("  Type:", var[0], "Name:", var[1])

        print("Total Local Variables:", len(local_vars))

        print("Function Calls:")
        calls = get_function_calls(body, func_name)

        if not calls:
            print("  None")
        else:
            for c in sorted(calls):
                print(f"  {func_name} -> {c}()")

    print("\nINLINE FUNCTIONS:")
    if inline_functions:
        for f in inline_functions:
            print(" ", f)
    else:
        print("  None")


main()