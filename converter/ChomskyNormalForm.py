class Chomsky:
    def __init__(self, startSymbol, nonTerminal, terminals,
                 productions):
        self.startSymbol = startSymbol
        self.nonTerminal = nonTerminal
        self.terminals = terminals
        self.productions = productions
        self.count = 0
        self.new_productions = {}
        self.new_prod_lookup = {}

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

    def convert(self):
        keys = list(self.productions.keys())
        for vt in self.terminals:
            new_symbol = self.new_lp()
            self.add_production(new_symbol, vt)
            self.nonTerminal.append(new_symbol)

            for lhs in keys:
                rhs = self.productions[lhs]

                for i in range(len(rhs)):
                    if len(rhs[i]) > 1:
                        old_production = rhs[i]
                        new_production = old_production.replace(vt, new_symbol)
                        rhs[i] = new_production

                self.productions[lhs] = rhs

    def new_lp(self):
        self.count += 1
        return "X" + str(self.count - 1)

    def add_production(self, lhs, rhs):
        if lhs in self.productions:
            self.productions[lhs].append(rhs)
        else:
            self.productions[lhs] = [rhs]

    def new_prod(self):
        for key in self.productions.keys():
            values = self.productions[key]
            values = list(map(self.form_prod, values))
            self.productions[key] = values

        for key, values in self.new_productions.items():
            self.productions[key] = values

    def form_prod(self, prod):
        upper_count = sum(1 for c in prod if c.isupper())
        while upper_count > 2:
            append = 0
            new_group = ""
            i = 0
            while i < len(prod):
                if append < 2:
                    if prod[i] == 'X':
                        append += 1
                        new_group += prod[i:i + 2]
                        i += 2
                    else:
                        append += 1
                        new_group += prod[i:i + 1]
                        i += 1

                else:
                    break

            if self.new_prod_lookup.get(new_group):
                prod = prod.replace(new_group, self.new_prod_lookup[new_group])
            else:
                new_symbol = self.new_lp()
                self.new_productions[new_symbol] = [new_group]
                self.new_prod_lookup[new_group] = new_symbol
                self.nonTerminal.append(new_symbol)
                prod = prod.replace(new_group, new_symbol)

            upper_count = sum(1 for c in prod if c.isupper())

        return prod

    def cfg_to_cnf(self):
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.eliminate_inaccessible_symbols()
        self.eliminate_nonproductive()
        self.convert()
        self.new_prod()
        return self

    def print_grammar(self):
        for variable, productions in self.productions.items():
            print(f"{variable} ->", " | ".join(productions))
