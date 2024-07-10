# boxcat

A small playground library for fp in Python, inspired from my time writing
Scala

### Development testing

```commandline
pytest
```

# Usage

---

## Options

To wrap values in Option monad

```
option_ten = Option(10)
option_string = Option("hello")
option_bool = Option(True)
```

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


print(option_uppercase.get_or_else(""))
```

```
result:
HELLO WORLD
```

### .unsafe_get()

To get the value out of the Option

```
option_hello_world = Option("just give me the value I know it's there")

print(option_hello_world.unsafe_get())
```

```
result:
"just give me the value I know it's there"
```

---

## Seq

So there isn't a great way to my knowledge of adding extension methods in Python
There was a thing called Monkey-Patching but seemed dodgy.

We can wrap traditional Lists [] in Seq()

```
seq_empty = Seq([])
seq_ten = Seq([10])
seq_string = Seq(['hello', 'world'])
seq_bool = Seq([True])

my_list = [1, 'a', 2, 'b', 3, 'c', 4, 'd', 5, 'e', 6, 'f', 7, 'g' 8, 'h', 9, 'i', 10]

seq_my_list = Seq(my_list)

```

## Important!!

###  .to_list()

Use `.to_list()` to get back the original Python List type from Seq()

```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

seq_my_list = Seq(my_list)

back_to_python_list = seq_my_list.to_list()

print(back_to_python_list)
```

```
result:
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### .map()

### Integer example

```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

seq_my_list = Seq(my_list)

seq_add_one = seq_my_list.map(lambda x: x + 1)
print(seq_add_one.to_list)
```

```
result:
[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
```

### .filter()

```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

seq_numbers = Seq(my_list)

only_evens = seq_numbers.filter(lambda x: x % 2 == 0)
print(seq_add_one.to_list)
```

```
result:
[2, 4, 6, 8, 10]
```