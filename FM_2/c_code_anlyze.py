import re

# ---------- READ C FILE ----------
with open("input.c", "r") as f:
    code = f.read()

# ---------- REMOVE COMMENTS ----------
code = re.sub(r'//.*', '', code)
code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)

# ---------- FUNCTION DEFINITIONS ----------
func_pattern = re.compile(
    r'(int|void|float|double)\s+(\w+)\s*\(([^)]*)\)\s*\{([\s\S]*?)\n\}',
    re.MULTILINE
)

functions = func_pattern.findall(code)

# ---------- REMOVE FUNCTIONS TO FIND GLOBAL VARIABLES ----------
code_without_functions = func_pattern.sub('', code)

# ---------- GLOBAL VARIABLES ----------
print("GLOBAL VARIABLES:")
global_vars = set()

global_decls = re.findall(
    r'\b(int|float|double|char)\s+([^;]+);',
    code_without_functions
)

for vtype, varlist in global_decls:
    for v in varlist.split(","):
        v = v.strip()
        v = re.sub(r'=.*', '', v)
        name = re.match(r'[a-zA-Z_]\w*(\[\w*\])?', v)
        if name:
            global_vars.add((vtype, name.group()))

if not global_vars:
    print("  None")
else:
    for g in sorted(global_vars):
        print("  Type:", g[0], "Name:", g[1])

# ---------- FUNCTIONS ----------
print("\nFUNCTIONS:")

for ret_type, fname, params, body in functions:
    print("\nFunction Name:", fname)
    print("Return Type:", ret_type)

    # ---------- PARAMETERS ----------
    print("Parameters:")
    if params.strip() == "":
        print("  None")
    else:
        for p in params.split(","):
            print(" ", p.strip())

    # ---------- LOCAL VARIABLES ----------
    print("Local Variables:")
    local_vars = set()

    local_decls = re.findall(
        r'\b(int|float|double|char)\s+([^;]+);',
        body
    )

    for vtype, varlist in local_decls:
        for v in varlist.split(","):
            v = v.strip()
            v = re.sub(r'=.*', '', v)
            name = re.match(r'[a-zA-Z_]\w*(\[\w*\])?', v)
            if name:
                local_vars.add((vtype, name.group()))

    # for-loop variables
    for_loop_vars = re.findall(
        r'for\s*\(\s*(int|float|double|char)\s+(\w+)',
        body
    )

    for fl in for_loop_vars:
        local_vars.add(fl)

    if not local_vars:
        print("  None")
    else:
        for lv in sorted(local_vars):
            print("  Type:", lv[0], "Name:", lv[1])

    # ---------- FUNCTION CALLS ----------
    print("Function Calls:")
    calls = re.findall(r'\b(\w+)\s*\(', body)
    calls = set(calls)

    # skip keywords and standard library calls ONLY
    skip_calls = {
        "printf", "scanf", "sizeof",
        "if", "for", "while", "switch", "return"
    }

    calls = calls - skip_calls

    if not calls:
        print("  None")
    else:
        for c in sorted(calls):
            print(" ", c + "()")