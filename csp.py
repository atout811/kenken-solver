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
    
    
