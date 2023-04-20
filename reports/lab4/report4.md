# Topic: Chomsky Normal Form
## Course: Formal Languages & Finite Automata
### Author: Racovcena Irina
### Variant: 24
____
## Theory Notations
In formal language theory, a context-free grammar, G, is said to be in Chomsky normal form (first described by Noam Chomsky) if all of its production rules are of the form:

A → BC,   or
A → a,   or
S → ε,
where A, B, and C are nonterminal symbols, the letter a is a terminal symbol (a symbol that represents a constant value), S is the start symbol, and ε denotes the empty string. Also, neither B nor C may be the start symbol, and the third production rule can only appear if ε is in L(G), the language produced by the context-free grammar G.

Every grammar in Chomsky normal form is context-free, and conversely, every context-free grammar can be transformed into an equivalent one which is in Chomsky normal form and has a size no larger than the square of the original grammar's size.

Converting a context-free grammar to Chomsky Normal Form (CNF) is a four-step process that involves the following transformations:

Step 1: Elimination of epsilon productions
An epsilon production is a production in which a non-terminal symbol can derive the empty string (ε). To eliminate epsilon productions, we need to identify all productions of the form A -> ε, where A is a non-terminal symbol. Then, we need to remove these productions from the grammar. Next, we need to replace each instance of A with ε in all the remaining productions that involve A. Finally, we need to add new productions to account for the replaced ε's. For each non-terminal symbol A that has a production B where B contains A, we add a new production that replaces A with ε for every subset of symbols in B that contains A.

Step 2: Elimination of unit productions
A unit production is a production in which a non-terminal symbol produces another non-terminal symbol.
To eliminate unit productions, we need to identify all productions of the form A -> B, where A and B are non-terminal symbols. Then, we need to replace each instance of A with the right-hand side of each of B's productions. We need to add all new productions created as a result of this replacement to the grammar.

Step 3: Elimination of inaccessible elements
An inaccessible non-terminal symbol is a non-terminal symbol that cannot derive any string of terminal symbols.
To eliminate inaccessible elements, we need to identify all non-terminal symbols that cannot be reached from the start symbol. Then, we need to remove all productions that involve these non-terminal symbols.

Step 4: Elimination of non-productive productions
A non-productive non-terminal symbol is a non-terminal symbol that cannot generate any string of terminal symbols.
To eliminate non-productive productions, we need to identify all non-terminal symbols that cannot be part of any derivation that leads to a string of terminal symbols. Then, we need to remove all productions that involve these non-terminal symbols.

After applying these four transformations, the context-free grammar will be in Chomsky Normal Form.

## Objectives:
1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description

1. Eliminating epsilon productions 

```
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
```

The first loop of the method identifies all nullable variables (variables that can produce an empty string). It does so by iterating through all productions in the grammar and adding any variables that produce an epsilon (represented by `ε`) to the nullables set.

The second loop creates new productions that do not include epsilon productions. It does so by iterating through all productions in the grammar and generating all possible combinations of removing nullable variables from the production. The resulting non-epsilon productions are added to the new_productions dictionary.

The third loop removes any remaining epsilon productions that may have been generated in the previous loop. It does so by iterating through all non-epsilon productions and generating new productions by removing each nullable variable from the production. The resulting non-epsilon productions are added to the new_productions dictionary.

Finally, any variables that have no productions left after the previous loops are removed from the `new_productions` dictionary. The resulting `new_productions` dictionary is then assigned to the productions attribute of the grammar.

2. Eliminating unit productions

```commandline
    def eliminate_unit_productions(self):
        for symbol in self.productions:
            unit_productions = [prod for prod in self.productions[symbol] if len(prod) == 1 and prod.isupper()]
            while unit_productions:
                unit = unit_productions.pop(0)
                self.productions[symbol].remove(unit)
                self.productions[symbol].extend(
                    prod for prod in self.productions[unit] if prod not in self.productions[symbol])
                unit_productions = [prod for prod in self.productions[symbol] if len(prod) == 1 and prod.isupper()]
```

For each unit production, the method removes the unit production from the productions for the current symbol and replaces it with the productions for the variable that the unit production produces. This is done by extending the productions for the current symbol with the productions for the unit variable, excluding any productions that were already in the productions for the current symbol. The method continues to perform this process until there are no more unit productions for the current symbol.

After the method has processed all unit productions for all symbols in the grammar, the grammar no longer contains any unit productions.

3. Eliminating inaccessible productions
```
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
```

This method eliminates inaccessible non-terminal symbols from a grammar. It starts by defining a visit function which takes a symbol and a set of visited symbols and recursively adds all symbols that are reachable from the given symbol to the visited set. Then, it calls visit on the start symbol of the grammar to find all accessible symbols. It then updates the non-terminal symbols to only include those that are accessible, and removes any productions that involve inaccessible symbols.

4. Eliminating non-productive productions

```commandline
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
```
This method is used to eliminate nonproductive variables from the grammar which are variables are that cannot be derived to any terminal symbol. It starts by initializing a set called productive with the start symbol of the grammar, and another set old_productive as an empty set. Then, it enters a loop that continues until old_productive is equal to productive. In this loop, for each non-productive symbol in the grammar, the method checks if all its productions contain only symbols that are already in productive or are terminals. If so, the symbol is added to productive.

After all non-productive symbols are removed from productive, the method finds the set of non-productive symbols by subtracting productive from the set of all non-terminals. It removes all productions with non-productive symbols from the grammar and removes all productions that contain symbols that are not in productive or are not terminals. Finally, the method updates the set of non-terminals with the productive symbols and returns the modified grammar.

5. Converting to Chomsky Normal Form

Convert function:
```commandline
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
```

Helper functions:
```commandline
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
```
The `convert()` method first iterates over each terminal symbol in the grammar, creating a new non-terminal symbol to replace each terminal symbol using the `new_lp()` method. It then adds a 
new production rule to the grammar that maps the new non-terminal symbol to the original terminal symbol using 
the `add_production()` method. The `convert()` method also adds the new non-terminal symbol to the set of non-terminal 
symbols in the grammar.

Next, the `convert()` method iterates over each production rule in the grammar and replaces any occurrences of the current 
terminal symbol with the new non-terminal symbol using the `replace()` method. This is done to ensure that all production rules in 
the grammar which corresponds to requirements for CNF.

The `convert()` method calls the `new_prod()` method to further modify the grammar into CNF. The `new_prod()` method first applies 
a helper function called `form_prod()` to each production rule in the grammar to ensure that each production rule contains 
at most two non-terminal symbols. The `form_prod()` method replaces any groups of three or more non-terminal symbols with new non-terminal symbols.

Finally, the `new_prod()` method adds the new production rules created by the `form_prod()` method to the grammar and updates the 
existing production rules to contain only two non-terminal symbols.

Then we have to gather all the necessary method for the conversion which looks like this:
```commandline
    def cfg_to_cnf(self):
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.eliminate_inaccessible_symbols()
        self.eliminate_nonproductive()
        self.convert()
        self.new_prod()
        return self
```

## Conclusion

In conclusion, converting a context-free grammar to Chomsky normal form is an essential step in formal language theory, 
and it requires careful attention to detail and a solid understanding of the underlying concepts. The process involves 
several steps, such as eliminating non-productive and unreachable symbols, removing ε-productions, and replacing all 
remaining rules with two non-terminal symbols or a single terminal symbol. By converting a context-free grammar to Chomsky 
normal form, we can simplify the grammar and make it easier to analyze. 

This laboratory work has provided an opportunity to 
practice the process of converting a context-free grammar to Chomsky normal form and to deepen our understanding of formal 
language theory. Overall, this laboratory work has been a valuable learning experience that has helped to improve our skills 
and knowledge in the field of formal language theory.

## Results
```commandline
Original Context Free Grammar:
S -> dB | A
A -> d | dS | aBdAB
B -> a | dA | A | ε
C -> Aa


After eliminating epsilon productions:
S -> d | dB | A
A -> d | dS | adA | aBdAB | adAB | aBdA
B -> a | dA | A
C -> Aa


After eliminating unit productions:
S -> d | dB | dS | adA | aBdAB | adAB | aBdA
A -> d | dS | adA | aBdAB | adAB | aBdA
B -> a | dA | d | dS | adA | aBdAB | adAB | aBdA
C -> Aa


After eliminating inaccessible symbols:
S -> d | dB | dS | adA | aBdAB | adAB | aBdA
A -> d | dS | adA | aBdAB | adAB | aBdA
B -> a | dA | d | dS | adA | aBdAB | adAB | aBdA


After eliminating non-productive productions:
S -> d | dB | dS | adA | aBdAB | adAB | aBdA
A -> d | dS | adA | aBdAB | adAB | aBdA
B -> a | dA | d | dS | adA | aBdAB | adAB | aBdA


Chomsky Normal Form:
S -> d | X1B | X1S | X2A | X5B | X6B | X4A
A -> d | X1S | X2A | X5B | X6B | X4A
B -> a | X1A | d | X1S | X2A | X5B | X6B | X4A
X0 -> a
X1 -> d
X2 -> X0X1
X3 -> X0B
X4 -> X3X1
X5 -> X4A
X6 -> X2A

```