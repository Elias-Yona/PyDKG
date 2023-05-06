# ABOUT

A Simple and Fast Distributed Key Generator

# SETUP

- Install poetry
- Run

```bash
poetry install
```

# DRIVETHROUGH

- Get the shares and commitments

```python
from pedersen import Vss
from pedersen import CyclicGroup

group = CyclicGroup(20)

p = group.p
h = group.h
g = group.g
t = 5
n = 5

# Initialize the dealer
dealer = Vss(degree=t)

# Generate the commitment
C = dealer.get_commitment(p=p, g=g, h=h)

# Generate shares for n players
shares = dealer.get_shares(n, p)

...
```

- Verify shares

```python
x, x_prime = [10.0, 20.0]


```
