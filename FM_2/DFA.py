from collections import defaultdict

class DataFlow:

    def __init__(self):
        self.lines = []
        self.graph = defaultdict(list)
        self.parents = defaultdict(list)

        self.defs = []
        self.use = []
        self.expr = []

        self.gen = []
        self.kill = []



#FORMAT SET
    def format_set(self, s):
        if not s:
            return "∅"
        return "{ " + ", ".join(sorted(s)) + " }"



#READ FILE
    def read_file(self, file):
        with open(file) as f:
            for line in f:
                line = line.split("//")[0].strip()

                if line == "":
                    continue

                if "=" in line or "if" in line or "while" in line or "for" in line or "}" in line or "{" in line or "else" in line:
                    self.lines.append(line)



#CFG
    def build_graph(self):
        n = len(self.lines)
        stack = []  

        for i in range(n):
            line = self.lines[i]

            
            if i < n - 1:
                self.graph[i].append(i+1)

            
            if line.startswith("if"):
                stack.append(("if", i))

            
            elif line.startswith("else"):
                if stack and stack[-1][0] == "if":
                    _, if_index = stack.pop()
                    stack.append(("else", if_index, i))

            
            elif line.startswith("while") or line.startswith("for"):
                stack.append(("loop", i))

           
            elif line == "}":
                if not stack:
                    continue

                top = stack.pop()

                
                if top[0] == "if":
                    if_index = top[1]
                    if i + 1 < n:
                        self.graph[if_index].append(i + 1)

                
                elif top[0] == "else":
                    if_index, else_index = top[1], top[2]
                    if i + 1 < n:
                        self.graph[if_index].append(else_index)
                        self.graph[else_index].append(i + 1)

                
                elif top[0] == "loop":
                    loop_index = top[1]
                    self.graph[i].append(loop_index)  # back edge

     
        for u in self.graph:
            for v in self.graph[u]:
                self.parents[v].append(u)


#ANALYZE
    def analyze(self):
        for line in self.lines:
            if "=" in line:
                left, right = line.split("=")
                var = left.strip()
                tokens = right.replace(";", "").split()

                used = [t for t in tokens if t.isalpha()]
                self.defs.append(var)
                self.use.append(set(used))

                if len(tokens) >= 3:
                    self.expr.append(" ".join(tokens))
                else:
                    self.expr.append(None)
            else:
                self.defs.append(None)
                self.use.append(set())
                self.expr.append(None)


#GEN / KILL
    def compute_gen_kill(self):
        n = len(self.lines)

        all_expr = set(e for e in self.expr if e)

        for i in range(n):
            stmt = f"s{i+1}"

            gen_set = set()
            kill_set = set()

            if self.defs[i]:
                gen_set.add(stmt)

            if self.expr[i]:
                gen_set.add(self.expr[i])

            for j in range(n):
                if i != j and self.defs[i] == self.defs[j]:
                    kill_set.add(f"s{j+1}")

            if self.defs[i]:
                for e in all_expr:
                    if self.defs[i] in e:
                        kill_set.add(e)

            self.gen.append(gen_set)
            self.kill.append(kill_set)


#ANALYSES
    def reaching_def(self):
        n = len(self.lines)
        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        change = True
        while change:
            change = False
            for i in range(n):
                old = exit[i].copy()

                e = set()
                for p in self.parents[i]:
                    e |= exit[p]

                entry[i] = e
                exit[i] = (e - self.kill[i]) | self.gen[i]

                if old != exit[i]:
                    change = True

        return entry, exit

    def live_var(self):
        n = len(self.lines)
        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        change = True
        while change:
            change = False
            for i in reversed(range(n)):
                old = entry[i].copy()

                e = set()
                for s in self.graph[i]:
                    e |= entry[s]

                exit[i] = e

                d = {self.defs[i]} if self.defs[i] else set()
                entry[i] = (e - d) | self.use[i]

                if old != entry[i]:
                    change = True

        return entry, exit

    def available_expr(self):
        n = len(self.lines)
        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        all_expr = set(e for e in self.expr if e)

        for i in range(n):
            entry[i] = all_expr.copy()

        change = True
        while change:
            change = False
            for i in range(n):
                old = exit[i].copy()

                if self.parents[i]:
                    e = set.intersection(*(exit[p] for p in self.parents[i]))
                else:
                    e = set()

                entry[i] = e

                gen = {self.expr[i]} if self.expr[i] else set()
                kill = {ex for ex in all_expr if self.defs[i] and self.defs[i] in ex}

                exit[i] = (e - kill) | gen

                if old != exit[i]:
                    change = True

        return entry, exit

    def very_busy_expr(self):
        n = len(self.lines)
        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        all_expr = set(e for e in self.expr if e)

        for i in range(n):
            exit[i] = all_expr.copy()

        change = True
        while change:
            change = False
            for i in reversed(range(n)):
                old = entry[i].copy()

                if self.graph[i]:
                    e = set.intersection(*(entry[s] for s in self.graph[i]))
                else:
                    e = set()

                exit[i] = e

                gen = {self.expr[i]} if self.expr[i] else set()
                kill = {ex for ex in all_expr if self.defs[i] and self.defs[i] in ex}

                entry[i] = (e - kill) | gen

                if old != entry[i]:
                    change = True

        return entry, exit

#PRINT
    def print_gen_kill(self):
        print("\nGEN and KILL Sets")
    
        
        state_w = 10
        gen_w = 30
        kill_w = 30

        
        print(f"{'State'.ljust(state_w)} | {'GEN'.ljust(gen_w)} | {'KILL'.ljust(kill_w)}")
        print("-" * (state_w + gen_w + kill_w + 6))

       
        print(f"{'ENTRY'.ljust(state_w)} | {'∅'.ljust(gen_w)} | {'∅'.ljust(kill_w)}")

        
        for i in range(len(self.lines)):
            state = str(i + 1)

            gen_str = self.format_set(self.gen[i])
            kill_str = self.format_set(self.kill[i])

            print(f"{state.ljust(state_w)} | {gen_str.ljust(gen_w)} | {kill_str.ljust(kill_w)}")

       
        print(f"{'EXIT'.ljust(state_w)} | {'∅'.ljust(gen_w)} | {'∅'.ljust(kill_w)}")

    def print_result(self, name, entry, exit):
        print(f"\n--> {name} <--")
        for i in range(len(self.lines)):
            print(f"s{i+1}: {self.lines[i]}")
            print("   Entry:", self.format_set(entry[i]))
            print("   Exit :", self.format_set(exit[i]))

#RUN
    def run(self, file):
        self.read_file(file)
        self.build_graph()
        self.analyze()
        self.compute_gen_kill()

        self.print_gen_kill()

        rd_e, rd_x = self.reaching_def()
        lv_e, lv_x = self.live_var()
        ae_e, ae_x = self.available_expr()
        vb_e, vb_x = self.very_busy_expr()

        print("="*80)
        self.print_result("Reaching Definitions", rd_e, rd_x)
        print("="*80)
        self.print_result("Live Variables", lv_e, lv_x)
        print("="*80)
        self.print_result("Available Expressions", ae_e, ae_x)
        print("="*80)
        self.print_result("Very Busy Expressions", vb_e, vb_x)


#MAIN
dfa = DataFlow()
dfa.run("input.c")