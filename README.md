# Factorio Factory Solver

An automated Factorio factory analyzer and optimizer using Z3 SMT solver to verify factory designs and minimize machine usage.

## Overview

This tool takes a Factorio factory design (as a blueprint string or factory graph) and uses constraint solving to:
1. **Verify the design is viable** - Check if the factory can operate without stalls
2. **Optimize machine settings** - Find the minimal speed settings needed for all assemblers and inserters
3. **Compute production rates** - Calculate item throughput at each point in the factory

### Dependencies

Install the required packages:

```bash
pip install z3-solver
pip install factorio-draftsman
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Team
Hayden Feeney
Pranav GolGopalkrishnan
Eric Han
Minh-Trien Vuong
