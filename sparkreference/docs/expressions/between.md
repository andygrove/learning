# Between

## Overview
The Between expression implements a range check operation that determines if a given input value falls within a specified range (inclusive of both bounds). It is a runtime replaceable expression that gets transformed into a combination of `GreaterThanOrEqual` and `LessThanOrEqual` operations during query planning.

## Syntax
```sql
input BETWEEN lower AND upper
```

```scala
// DataFrame API
col("column_name").between(lowerValue, upperValue)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | The expression to be evaluated against the range |
| lower | Expression | Lower bound of the between check (inclusive) |
| upper | Expression | Upper bound of the between check (inclusive) |

## Return Type
Returns `BooleanType` - true if the input value is within the specified range (inclusive), false otherwise.

## Supported Data Types
Supports any data types that can be compared using comparison operators:

- Numeric types (IntegerType, LongType, DoubleType, FloatType, DecimalType, etc.)
- String types (StringType)
- Date and time types (DateType, TimestampType)
- Binary types (BinaryType)
- Any other types that support ordering comparisons

## Algorithm
The Between expression is evaluated through the following steps:

- The expression is replaced at runtime with an AND operation of two comparisons
- First comparison: `input >= lower` (GreaterThanOrEqual)
- Second comparison: `input <= upper` (LessThanOrEqual)
- Final result: `(input >= lower) AND (input <= upper)`
- When `ALWAYS_INLINE_COMMON_EXPR` is disabled, the input expression is evaluated once using a `With` wrapper to avoid duplicate evaluation

## Partitioning Behavior
This expression has the following partitioning characteristics:

- Does not affect data partitioning as it's a filtering predicate
- Does not require shuffle operations by itself
- Can be pushed down to data sources for partition pruning when used in WHERE clauses
- Preserves existing partitioning schemes

## Edge Cases

- **Null handling**: If any of the three expressions (input, lower, upper) evaluates to null, the entire Between expression returns null
- **Inverted bounds**: When lower > upper, the expression will always return false (except for null cases)
- **Equal bounds**: When lower == upper, the expression behaves as an equality check (input == lower)
- **Type coercion**: Implicit type casting may occur between input, lower, and upper expressions according to Spark's type precedence rules

## Code Generation
This expression supports Tungsten code generation through its replacement expression. The generated code depends on the underlying `GreaterThanOrEqual`, `LessThanOrEqual`, and `And` expressions, which all support code generation for efficient execution.

## Examples
```sql
-- Numeric range check
SELECT * FROM table WHERE age BETWEEN 18 AND 65;

-- Date range check  
SELECT * FROM table WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';

-- String range check
SELECT * FROM table WHERE name BETWEEN 'A' AND 'M';
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Numeric range
df.filter(col("age").between(18, 65))

// Date range
df.filter(col("order_date").between(lit("2023-01-01"), lit("2023-12-31")))

// With column expressions
df.filter(col("price").between(col("min_price"), col("max_price")))
```

## See Also

- `GreaterThanOrEqual` - Component expression for lower bound check
- `LessThanOrEqual` - Component expression for upper bound check  
- `And` - Logical operator combining the bound checks
- `In` - Check if value exists in a set of discrete values
- `RuntimeReplaceable` - Base trait for expressions that are replaced at runtime