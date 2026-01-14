# Uniform

## Overview
The `uniform` function generates random floating-point numbers from a uniform distribution within a specified range. It returns pseudo-random values between the minimum and maximum bounds (inclusive of min, exclusive of max) using an optional seed for reproducible results.

## Syntax
```sql
uniform(min, max)
uniform(min, max, seed)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| min | Numeric | The minimum bound of the uniform distribution (inclusive) |
| max | Numeric | The maximum bound of the uniform distribution (exclusive) |
| seed | Integer/Long | Optional seed value for reproducible random number generation |

## Return Type
The return type follows numeric type precedence rules:

- For integral types: returns the wider of the two input types
- For floating-point types: returns DoubleType when either input is DoubleType, otherwise FloatType
- For decimal types: returns the wider decimal type
- Mixed numeric types follow standard SQL numeric precedence

## Supported Data Types

- **Input types**: All numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- **Seed types**: IntegerType or LongType only
- **Output**: Numeric type based on input type precedence

## Algorithm

- Validates that all inputs are foldable (constant expressions)
- Uses the internal `Rand` function with the provided or default seed
- Implements the formula: `min + (max - min) * rand(seed)`
- Casts inputs to DoubleType for calculation, then casts result back to target type
- Returns null if any input expression evaluates to null

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning schemes
- Does not require data shuffle
- Generates independent random values per partition

## Edge Cases

- **Null handling**: Returns null if any input parameter (min, max, seed) is null
- **Non-foldable inputs**: Throws DataTypeMismatch error if min, max, or seed are not constant expressions
- **Type resolution**: Returns NullType if seed expression is unresolved or NullType
- **Invalid ranges**: No explicit validation for min >= max cases in the expression itself
- **Deterministic behavior**: Non-deterministic by nature, but reproducible with same seed

## Code Generation
This expression uses runtime replacement and does not directly support Tungsten code generation. It is replaced at runtime with a combination of `Add`, `Multiply`, `Subtract`, `Cast`, and `Rand` expressions that may support code generation.

## Examples
```sql
-- Generate random number between 10 and 20
SELECT uniform(10, 20) AS random_value;

-- Generate reproducible random number with seed
SELECT uniform(0.0, 1.0, 12345) AS seeded_random;

-- Use with different numeric types
SELECT uniform(1, 100, 0) AS int_range;
SELECT uniform(1.5, 2.5, 42) AS float_range;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Generate random values in range
df.select(expr("uniform(1, 10)").alias("random_int"))

// With seed for reproducibility  
df.select(expr("uniform(0.0, 1.0, 123)").alias("seeded_random"))
```

## See Also

- `rand()` - Generates random numbers between 0 and 1
- `randn()` - Generates normally distributed random numbers
- `random()` - Alternative random number generation function