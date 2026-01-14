# Bitwise Expressions Reference

## BitwiseAnd

### Overview
BitwiseAnd calculates the bitwise AND operation (&) between two integral numeric values. This expression performs bit-level AND logic on the binary representations of the input values, returning 1 for each bit position where both operands have a 1.

### Syntax
```sql
expr1 & expr2
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | IntegralType | Left operand for bitwise AND operation |
| right | IntegralType | Right operand for bitwise AND operation |

### Return Type
Returns the same integral data type as the input operands (ByteType, ShortType, IntegerType, or LongType).

### Supported Data Types
- ByteType
- ShortType  
- IntegerType
- LongType

### Algorithm
- Evaluates both left and right expressions to get numeric values
- Performs bitwise AND operation using the `&` operator
- Casts result back to appropriate integral type (toByte/toShort for smaller types)
- Uses type-specific lambda functions for null-safe evaluation
- Inherits code generation from BinaryArithmetic for optimized execution

### Partitioning Behavior
- Preserves partitioning as it's a row-level transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions independently

### Edge Cases
- **Null handling**: Returns null if either operand is null (null-safe evaluation)
- **Type casting**: Results are cast to maintain original data type precision
- **Overflow**: No overflow possible as bitwise AND cannot produce values larger than inputs

### Code Generation
Supports Tungsten code generation through inheritance from BinaryArithmetic, generating efficient Java bytecode for the bitwise operations.

### Examples
```sql
-- Basic bitwise AND
SELECT 3 & 5;  -- Returns 1

-- Column operations
SELECT col1 & col2 FROM table;

-- Complex expressions
SELECT (status_flags & 7) AS lower_bits FROM events;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select($"col1".bitwiseAND($"col2"))
df.select($"status" & lit(15))  // Mask lower 4 bits
```

### See Also
BitwiseOr, BitwiseXor, BitwiseNot

---

## BitwiseOr

### Overview
BitwiseOr calculates the bitwise OR operation (|) between two integral numeric values. This expression performs bit-level OR logic, returning 1 for each bit position where at least one operand has a 1.

### Syntax
```sql
expr1 | expr2
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | IntegralType | Left operand for bitwise OR operation |
| right | IntegralType | Right operand for bitwise OR operation |

### Return Type
Returns the same integral data type as the input operands (ByteType, ShortType, IntegerType, or LongType).

### Supported Data Types
- ByteType
- ShortType
- IntegerType  
- LongType

### Algorithm
- Evaluates both left and right expressions to get numeric values
- Performs bitwise OR operation using the `|` operator
- Casts result back to appropriate integral type for smaller types
- Uses type-specific lambda functions for null-safe evaluation
- Inherits code generation from BinaryArithmetic

### Partitioning Behavior
- Preserves partitioning as it's a row-level transformation
- Does not require shuffle operations
- Can be executed independently on each partition

### Edge Cases
- **Null handling**: Returns null if either operand is null
- **Type casting**: Results maintain original data type through explicit casting
- **Overflow**: No overflow risk as OR operation cannot exceed maximum value bounds

### Code Generation
Inherits Tungsten code generation from BinaryArithmetic for optimized runtime performance.

### Examples
```sql
-- Basic bitwise OR
SELECT 3 | 5;  -- Returns 7

-- Setting flags
SELECT permissions | 4 AS new_permissions FROM users;
```

```scala
// DataFrame API usage
df.select($"flags".bitwiseOR($"new_flags"))
df.select($"permissions" | lit(7))  // Set multiple permission bits
```

### See Also
BitwiseAnd, BitwiseXor, BitwiseNot

---

## BitwiseXor

### Overview
BitwiseXor calculates the bitwise exclusive OR (XOR) operation (^) between two integral values. This expression returns 1 for each bit position where exactly one operand has a 1, and 0 where both operands have the same bit value.

### Syntax
```sql
expr1 ^ expr2
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | IntegralType | Left operand for bitwise XOR operation |
| right | IntegralType | Right operand for bitwise XOR operation |

### Return Type
Returns the same integral data type as the input operands (ByteType, ShortType, IntegerType, or LongType).

### Supported Data Types
- ByteType
- ShortType
- IntegerType
- LongType

### Algorithm
- Evaluates both operand expressions to numeric values
- Applies bitwise XOR using the `^` operator
- Casts result to maintain original integral type precision
- Uses pattern matching for type-specific evaluation functions
- Leverages BinaryArithmetic for code generation

### Partitioning Behavior
- Preserves existing partitioning scheme
- No shuffle required as it operates on individual rows
- Fully parallelizable across partitions

### Edge Cases
- **Null handling**: Returns null when either input is null
- **Identity property**: `x ^ 0 = x` and `x ^ x = 0`
- **Type preservation**: Maintains input data type through explicit casting

### Code Generation
Benefits from BinaryArithmetic's Tungsten code generation for efficient bytecode generation.

### Examples
```sql
-- Basic XOR operation
SELECT 3 ^ 5;  -- Returns 6

-- Toggle bits
SELECT flags ^ mask AS toggled_flags FROM settings;
```

```scala
// DataFrame API usage  
df.select($"value1" ^ $"value2")
df.select($"data".bitwiseXOR($"toggle_mask"))
```

### See Also
BitwiseAnd, BitwiseOr, BitwiseNot

---

## BitwiseNot

### Overview
BitwiseNot calculates the bitwise complement (~) of a single integral value. This unary expression flips all bits in the binary representation, converting 0s to 1s and 1s to 0s.

### Syntax
```sql
~expr
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | IntegralType | Expression to apply bitwise NOT operation |

### Return Type
Returns the same integral data type as the input (ByteType, ShortType, IntegerType, or LongType).

### Supported Data Types
- ByteType
- ShortType
- IntegerType
- LongType

### Algorithm
- Evaluates the child expression to get numeric value
- Applies bitwise complement using `~` operator
- Casts result back to original data type for smaller integral types
- Uses type-specific evaluation functions for proper type handling
- Implements custom code generation for optimal performance

### Partitioning Behavior
- Preserves partitioning as a unary row-level operation
- No shuffle operations required
- Executes independently per partition

### Edge Cases
- **Null handling**: Returns null if input is null (null intolerant)
- **Two's complement**: Result follows two's complement arithmetic rules
- **Type bounds**: ~0 produces -1 due to signed integer representation

### Code Generation
Implements custom Tungsten code generation using `defineCodeGen` with type-appropriate casting.

### Examples
```sql
-- Basic bitwise NOT
SELECT ~0;  -- Returns -1

-- Flip all bits
SELECT ~status_bits FROM system_status;
```

```scala
// DataFrame API usage
df.select(~$"bitmask")
df.select(bitwiseNOT($"flags"))
```

### See Also
BitwiseAnd, BitwiseOr, BitwiseXor

---

## BitwiseCount

### Overview
BitwiseCount returns the number of set bits (1s) in the binary representation of an integral or boolean value. This function is also known as population count or Hamming weight.

### Syntax
```sql
bit_count(expr)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | IntegralType or BooleanType | Expression to count set bits in |

### Return Type
Always returns IntegerType regardless of input type.

### Supported Data Types
- BooleanType
- ByteType
- ShortType
- IntegerType
- LongType

### Algorithm
- For BooleanType: returns 1 if true, 0 if false
- For integral types: uses `java.lang.Long.bitCount()` method
- Converts input to appropriate type before bit counting
- Returns count as 32-bit integer value
- Implements type-specific code generation paths

### Partitioning Behavior
- Preserves partitioning as unary transformation
- No shuffle required
- Can execute in parallel across all partitions

### Edge Cases
- **Null handling**: Returns null for null input (null intolerant)
- **Boolean handling**: Special case returns 1/0 for true/false
- **Range**: Result is always between 0 and bit-width of input type

### Code Generation
Uses conditional code generation based on input type, with optimized paths for BooleanType vs integral types.

### Examples
```sql
-- Count set bits
SELECT bit_count(0);   -- Returns 0
SELECT bit_count(7);   -- Returns 3 (binary: 111)
SELECT bit_count(15);  -- Returns 4 (binary: 1111)

-- Count flags set
SELECT bit_count(user_permissions) FROM users;
```

```scala
// DataFrame API usage
df.select(bit_count($"flags"))
df.select(bit_count($"is_active"))  // Boolean column
```

### See Also
BitwiseAnd, BitwiseOr, BitwiseGet

---

## BitwiseGet

### Overview
BitwiseGet extracts the value of a specific bit (0 or 1) at a given position from an integral value. Bit positions are numbered from right to left starting at zero (LSB = position 0).

### Syntax
```sql
bit_get(expr, pos)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | IntegralType | Source value to extract bit from |
| right | IntegerType | Bit position (0-based from right) |

### Return Type
Always returns ByteType (0 or 1).

### Supported Data Types
- ByteType (8 bit positions: 0-7)
- ShortType (16 bit positions: 0-15)  
- IntegerType (32 bit positions: 0-31)
- LongType (64 bit positions: 0-63)

### Algorithm
- Validates position is within valid range for data type
- Converts target value to long for uniform bit shifting
- Right-shifts target by position amount
- Masks result with 1 to extract single bit
- Returns result as ByteType (0 or 1)

### Partitioning Behavior
- Preserves partitioning as row-level binary operation
- No shuffle operations needed
- Fully parallelizable across partitions

### Edge Cases
- **Null handling**: Returns null if either argument is null (null intolerant)
- **Position validation**: Throws `QueryExecutionErrors.bitPositionRangeError` for invalid positions
- **Negative positions**: Not allowed, throws error
- **Out of range**: Position must be < bit size of data type

### Code Generation
Implements null-safe code generation with runtime position validation and bit extraction logic.

### Examples
```sql
-- Extract specific bits
SELECT bit_get(11, 0);  -- Returns 1 (LSB of binary 1011)
SELECT bit_get(11, 2);  -- Returns 0 (3rd bit of binary 1011) 
SELECT bit_get(8, 3);   -- Returns 1 (4th bit of binary 1000)

-- Check permission flags
SELECT bit_get(permissions, 2) AS can_write FROM users;
```

```scala
// DataFrame API usage
df.select(bit_get($"status_flags", lit(0)))  // Check LSB
df.select(bit_get($"permissions", $"bit_position"))
```

### See Also
BitwiseAnd, BitwiseOr, BitwiseCount