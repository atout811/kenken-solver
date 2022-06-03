class CSP():

    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def count(self, seq):

        return sum(bool(x) for x in seq)

    def nconflicts(self, var, val, assignment):

        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return self.count(conflict(v) for v in self.neighbors[var])

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {
                v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):

        for B, b in removals:
            self.curr_domains[B].append(b)


def first(self, iterable, default=None):
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)


def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])


def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)

# return true if a solution is found and false otherwise


def AC3(csp):
    queue = [(x, y) for x in csp.variables for y in csp.neighbors[x]]
    while queue:
        x, y = queue.pop()
        if revise(csp, x, y):
            if not csp.domains[y]:
                return False
            for z in csp.neighbors[y]:
                if z != x:
                    queue.append((z, y))
    return True


def revise(csp, x, y):
    revised = False
    for xi in csp.domains[x]:
        if not any(csp.constraints(xi, y)):
            csp.domains[x].remove(xi)
            revised = True
    return revised


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):

    csp.support_pruning()

    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals):
    """Maintain arc consistency."""
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):

    def backtrack(assignment):
        # check if we added all var
        if len(assignment) == len(csp.variables):
            return assignment
        # add var to dict
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            # check the number if conflicts =0 the add this var with this val
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)

                removals = csp.suppose(var, value)  # ??
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
