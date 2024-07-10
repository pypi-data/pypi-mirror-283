# boxcat

Please do not actually use this library. 

A small playground library for fp in Python, inspired from my time writing
Scala

### Development testing

```commandline
pytest
```

* Github Actions runs the tests when making a pull request and on push.
* Github Actions also creates a new tag, release and publishes to PyPi on merge/push into `main`

Please be careful during dev 


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
print(only_evens.to_list)
```

```
result:
[2, 4, 6, 8, 10]
```

---

## Either

So Eithers have 2 projections a Right and a Left.

Conventionally a Left is used for error handling.

Whilst Right will contain the values we want to work with.

### Basic lifting value into the Either datatype 
    left_value = Left("Error")
    right_value = Right(42)

### .map() on a Right(value)
    right_value = Right(42)

    mapped_right = right_value.map(lambda x: x * 2)
    print(mapped_right.value if mapped_right.is_right() else "No value") 

    # Output: 84

### .map() on a Left(value)

    left_value = Left("Error")

    flat_mapped_right = right_value.flat_map(lambda x: Right(x * 2))
    print(flat_mapped_right.value if flat_mapped_right.is_right() else "No value")  # Output: 84

### .fold() on a Right(value)

    right_value = Right(42)

    result = right_value.fold(
        if_left=lambda x: f"Error: {x}",
        if_right=lambda x: f"Success: {x}"
    )
    print(result)  
    
    # Output: Success: 42

### .fold() on a Left(value)

    left_value = Left("Error")

    result = left_value.fold(
        if_left=lambda x: f"Error: {x}",
        if_right=lambda x: f"Success: {x}"
    )
    print(result)  

    # Output: Error: Error

### pattern_matching on Either

Similar to .fold() we can handle the Either by just pattern-matching on the Either, performing
the pattern match within a method.

```
right_value = Right(999)

def handle_either(either: Either[str, int]):
    match result:
        case Right(value):
            return value
        case Left(error_message):
            return f"Got the error message: {error_messa
            
handle_either(right_value)

# Output: 999
```
```
left_value = Left("Error")

def handle_either(either: Either[str, int]):
    match result:
        case Right(value):
            return value
        case Left(error_message):
            return f"Got the error message: {error_message}" 

handle_either(left_value)

# Output: "Error"
```
---

# Products

So these were going to be added to the Tuple datatype but had to come up with
another name for Tuples. So resorted to the Product type, from type algebra.

Again my understanding is rudimentary at best when it comes to type theory and laws etc.

### Important:

    These only work for a single type, consistent across all Options 
    within a ProductOpt() or Seqs within a ProductSeq() 

But for the sake of hacking something together I present: 

## .mapN()

---

## ProductOpt

Pretty cursed but hey whatever, basically allows you to apply a function 
to all the Option[T] within the ProductOpt()

```
opt1 = Option(1)
opt2 = Option(2)
opt3 = Option(3)

productOpt = (
    ProductOpt(
        opt1,
        opt2,
        opt3
    )
    .mapN(lambda x, y, z: x + y + z)
    .unsafe_get()
)

print(productOpt)

# Output: 6
```
---

## ProductSeq

Hacky and Wacky

Again basically allows you to apply a function 
to all the Seq[T] within the ProductSeq()

```
seq1 = Seq([1, 2, 3, 4])
seq2 = Seq([4, 5, 6, 4])
seq3 = Seq([7, 8, 9, 4])

productSeq = (
    ProductSeq(
        seq1,
        seq2,
        seq3,
    )
    .mapN(lambda x: x.fold_left(0)(lambda i, j: i + j))
    .to_list()
)

print(productSeq)

# Output: [10, 19, 28]