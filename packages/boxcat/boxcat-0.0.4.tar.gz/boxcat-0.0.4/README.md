# boxcat


A small playground library for fp in Python, inspired from my time writing
Scala

### Development testing

```commandline
pytest
```


## Usage

To wrap values in Option monad

### .map()

### Integer example

```
option_ten = Option(10)
option_multiply_by_two = option_ten.map(lambda x: x * 2)
print(option_multiply_by_two.get_or_else(0))
```

```
result:
20
```
### String example

```
option_hello_world = Option("hello world")
option_uppercase = option_hello_world.map(lambda s: s.upper())
option_uppercase.get_or_else("")  

print(option_uppercase.get_or_else(""))
```

```
result:
HELLO WORLD
```
