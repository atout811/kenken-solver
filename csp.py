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

    
    def count(self,seq):
      
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
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
    
    
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

