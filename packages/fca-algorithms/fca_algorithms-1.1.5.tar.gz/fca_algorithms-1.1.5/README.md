![build](https://gitlab.com/cps-phd-leutwyler-nicolas/rca_fca_general/badges/master/pipeline.svg)

# FCA algorithms

This is a module providing a set of commonly used algorithms in FCA, RCA, and some of its variants. Its general intention is to provide an easy to use API so that it's easier to create other programs using these algorithms. The main algorithm that calculates formal concepts is `inclose`, and, in [this version](https://pypi.org/project/fca-algorithms/1.0.0/), it is implemented in C++. Considering this, the API is expected to behave somewhat acceptably.

[API Reference](https://fca-algorithms-docs-cps-phd-leutwyler-nicolas-50eff1e931e894d3e.gitlab.io/index.html)

# CLI

## FCA

### Plot a hasse diagram from a context

```bash
fca_cli -c input.csv --show_hasse
```

The context is expected to be a `csv` with the following format

| name | attr1 | attr2 |
| ---- | :---: | :---: |
| obj1 |   x   |
| obj2 |       |   x   |
| obj3 |   x   |   x   |
| obj4 |       |

### Output files

```bash
fca_cli -c input.csv --show_hasse --output_dir path/to/folder/
```

Will create two files, one representing the hasse graph, the other one with a concept for each line. The line is the index in the hasse graph.

## RCA

To plot the hasse diagrams of the contexts 1 and 2 after applying RCA with exists

```bash
fca_cli -k context_1.csv context_2.csv -r relation_1_2.csv relation_2_1.csv --show_hasse
```

to specify operator

```bash
fca_cli -k context_1.csv context_2.csv -r relation_1_2.csv relation_2_1.csv --show_hasse -o forall
```

# FCA utils

Module for FCA basics such as retrieving concepts, drawing a hasse diagram, etc

## Getting formal concepts

### In batch

```python
from fca.api_models import Context, Concept

c = Context(O : List[str], A : List[str], I : List[List[int]])
concepts = c.get_concepts(c) List[Concept]
```

### Incrementally

#### By intent

```python
from fca.api_models import IncLattice

l = IncLattice(attributes=['a', 'b', 'c', 'd'])
l.add_intent('o1', [0, 2])  # numbers are the indices of the attributes
l.add_intent('o2', [1, 2])
.
.
.
```

#### By pair

```python
from fca.api_models import IncLattice

l = IncLattice()
l.add_pair('o1', 'a')
l.add_pair('o2', 'b')
l.add_pair('o2', 'a')
.
.
.
```

## Getting association rules

```python
from fca.api_models import Context

c = Context(O, A, I)
c.get_association_rules(min_support=0.4, min_confidence=1)
```

## Drawing hasse diagram

```python
from fca.plot.plot import plot_from_hasse
from fca.api_models import Context


k = Context(O, A, I)
k.get_lattice().plot()
# plot receives a number of kwargs such as print_latex=True|False


l = IncLattice(attributes=['a', 'b', 'c', 'd'])
l.add_intent('o1', [0, 2])  # numbers are the indices of the attributes
l.add_intent('o2', [1, 2])
.
.
.
l.plot()
```

# Contributors

- Ramshell (Nicolas Leutwyler)
