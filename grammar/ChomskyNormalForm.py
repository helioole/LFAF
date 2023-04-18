class Chomsky:
    def __init__(self, startSymbol, nonTerminal, terminals,
                 productions):
        self.startSymbol = startSymbol
        self.nonTerminal = nonTerminal
        self.terminals = terminals
        self.productions = productions


    def eliminate_epsilon_productions(self):
        nullables = set()
        for variable, productions in self.productions.items():
            if "ε" in productions:
                nullables.add(variable)

        new_productions = {}
        for variable, productions in self.productions.items():
            new_productions[variable] = []
            for production in productions:
                if production == "ε":
                    continue
                for nullable in nullables:
                    if nullable in production:
                        new_production = production.replace(nullable, "")
                        if new_production not in new_productions[variable]:
                            new_productions[variable].append(new_production)
                if production not in new_productions[variable]:
                    new_productions[variable].append(production)

        for variable, productions in new_productions.items():
            new_productions[variable] = [p for p in productions if p != "ε"]

        for variable, productions in new_productions.items():
            for production in productions:
                if len(production) == 1 and production in nullables:
                    continue
                for i in range(len(production)):
                    if production[i] in nullables:
                        new_production = production[:i] + production[i + 1:]
                        if new_production not in new_productions[variable]:
                            new_productions[variable].append(new_production)

        self.productions = {k: v for k, v in new_productions.items() if v}

    def eliminate_unit_productions(self):
        for symbol in self.productions:
            unit_productions = [prod for prod in self.productions[symbol] if len(prod) == 1 and prod.isupper()]
            while unit_productions:
                unit = unit_productions.pop(0)
                self.productions[symbol].remove(unit)
                self.productions[symbol].extend(
                    prod for prod in self.productions[unit] if prod not in self.productions[symbol])
                unit_productions = [prod for prod in self.productions[symbol] if len(prod) == 1 and prod.isupper()]

    def eliminate_inaccessible_symbols(self):
        def visit(symbol, visited):
            if symbol not in visited:
                visited.add(symbol)
                for prod in self.productions[symbol]:
                    for s in prod:
                        if s in self.nonTerminal:
                            visit(s, visited)

        accessible_symbols = set()
        visit(self.startSymbol, accessible_symbols)

        self.nonTerminal = [nt for nt in self.nonTerminal if nt in accessible_symbols]
        self.productions = {k: v for k, v in self.productions.items() if k in accessible_symbols}

    def eliminate_nonproductive(self):
        productive = {self.startSymbol}
        old_productive = set()

        while old_productive != productive:
            old_productive = productive.copy()
            for symbol, rhs in self.productions.items():
                if symbol not in productive:
                    for prod in rhs:
                        if all(s in productive or s in self.terminals for s in prod):
                            productive.add(symbol)

        nonproductive = set(self.nonTerminal) - productive

        for symbol in nonproductive:
            del self.productions[symbol]

        for symbol, rhs in self.productions.items():
            new_rhs = []
            for prod in rhs:
                if all(s in productive or s in self.terminals for s in prod):
                    new_rhs.append(prod)
            self.productions[symbol] = new_rhs

        self.nonTerminal = sorted(list(productive))


    def to_cnf(self):
        new_productions = {}
        next_new_var = 1
        terminal_var_map = {}

        for var, prods in self.productions.items():
            new_productions[var] = []

            for prod in prods:
                if len(prod) >= 3:
                    prod_vars = [f"X{next_new_var + i}" for i in range(len(prod) - 1)]
                    next_new_var += len(prod) - 1
                    self.nonTerminal.extend(prod_vars)

                    new_productions[var].append(prod[0] + prod_vars[0])
                    for i in range(len(prod) - 2):
                        new_var = prod_vars[i]
                        new_productions.setdefault(new_var, [])
                        new_productions[new_var].append(prod[i + 1] + prod_vars[i + 1])
                    new_productions.setdefault(prod_vars[-1], [])
                    new_productions[prod_vars[-1]].append(prod[-1])

                elif len(prod) == 2 and all(sym in self.nonTerminal for sym in prod):
                    new_productions[var].append(prod)

                else:
                    new_prod = prod
                    for sym in prod:
                        if sym in self.terminals:
                            if sym not in terminal_var_map:
                                new_var = f"T{next_new_var}"
                                next_new_var += 1
                                self.nonTerminal.append(new_var)
                                new_productions.setdefault(new_var, [])
                                new_productions[new_var].append(sym)
                                terminal_var_map[sym] = new_var
                            new_prod = new_prod.replace(sym, terminal_var_map[sym], 1)
                    new_productions[var].append(new_prod)

        self.productions = new_productions
        self.nonTerminal = sorted(list(set(self.nonTerminal)))

    def cfg_to_cnf(self):
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.eliminate_inaccessible_symbols()
        self.eliminate_nonproductive()
        self.to_cnf()
        return self

    def print_grammar(self):
        for variable, productions in self.productions.items():
            print(f"{variable} ->", " | ".join(productions))
