python-mayadate
===============

Maya Date:
```python
>>> m = mayadate.date(8, 3, 2, 10, 15)
>>> m
mayadate.date(8, 3, 2, 10, 15)
```

Human readable:
```python
>>> str(m)
"8.3.2.10.15 | 2 Men | 13 Pax | 1 Ik' | G8"
```

Long Count:
```python
>>> m.longcountstr
'8.3.2.10.15'
```

Tzolkin:
```python
>>> m.tzolkinstr
'2 Men'
```

Haab:
```python
>>> m.haabstr
'13 Pax'
```
Year Bearer:
```python
>>> m.yearbearerstr
"1 Ik'"
```

Lord of Night:
```python
>>> m.lordofnightstr
'G8'
```

To Gregorian Date Conversion:
```python
>>> g = m.togregorian()
>>> g
datetime.date(103, 5, 19)
```

Computations:
```python
>>> n = m - mayadate.delta(1)
>>> n
mayadate.date(8, 3, 2, 10, 14)
```

Comparsions:
```python
>>> n < m
True
```

TODO:
-----
* replace() method
* custom formatting support
* pickle support
