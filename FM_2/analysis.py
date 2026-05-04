import re

# ---------- read file ----------
def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


# ---------- remove comments ----------
def remove_comments(code):
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
    return code


# ---------- get statements ----------
def get_statements(code):
    lines = code.split('\n')
    stmts = []

    for line in lines:
        line = line.strip()
        if line and ';' in line:
            stmts.append(line)

    return stmts


# ---------- find definitions ----------
def get_definitions(statements):
    defs = {}

    for i, stmt in enumerate(statements):
        if '=' in stmt:
            left = stmt.split('=')[0]
            vars_found = re.findall(r'[a-zA-Z_]\w*', left)

            for v in vars_found:
                defs.setdefault(v, []).append(i)

    return defs


# ---------- find uses ----------
def get_uses(statements):
    uses = {}
    keywords = ["int", "float", "double", "char", "return"]

    for i, stmt in enumerate(statements):
        vars_found = re.findall(r'[a-zA-Z_]\w*', stmt)

        for v in vars_found:
            if v not in keywords:
                uses.setdefault(v, []).append(i)

    return uses


# ---------- reaching definitions ----------
def print_reaching_defs(statements, defs):
    print("\nREACHING DEFINITIONS:")

    for i in range(len(statements)):
        reaching = []

        for var in defs:
            for line in defs[var]:
                if line <= i:
                    reaching.append((var, line))

        print("Line", i, ":", reaching)


# ---------- live variables ----------
def print_live_variables(statements):
    print("\nLIVE VARIABLES:")

    live = set()

    for i in reversed(range(len(statements))):
        stmt = statements[i]

        all_vars = set(re.findall(r'[a-zA-Z_]\w*', stmt))

        if '=' in stmt:
            left = set(re.findall(r'[a-zA-Z_]\w*', stmt.split('=')[0]))
        else:
            left = set()

        live = (live - left) | all_vars
        print("Line", i, ":", live)


# ---------- def-use chains ----------
def print_def_use(defs, uses):
    print("\nDEF-USE CHAINS:")

    for var in defs:
        if var in uses:
            for d in defs[var]:
                for u in uses[var]:
                    if u > d:
                        print(var, ":", d, "->", u)


# ---------- main ----------
def main():
    code = read_file("input.c")
    code = remove_comments(code)

    statements = get_statements(code)

    print("STATEMENTS:")
    for i, s in enumerate(statements):
        print(i, ":", s)

    defs = get_definitions(statements)
    uses = get_uses(statements)

    print("\nDEFINITIONS:")
    for v in defs:
        print(v, "defined at", defs[v])

    print("\nUSES:")
    for v in uses:
        print(v, "used at", uses[v])

    print_reaching_defs(statements, defs)
    print_live_variables(statements)
    print_def_use(defs, uses)


# ---------- run ----------
main()