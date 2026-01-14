# IsNotNull

## Overview
`IsNotNull` is a unary predicate expression that tests whether a given expression evaluates to a non-null value. It returns `true` if the input expression is not null, and `false` if the input expression is null.

## Syntax
```sql
expression IS NOT NULL
```

```scala
// DataFrame API
col("column_name").isNotNull
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to test for non-null values |

## Return Type
`BooleanType` - Always returns a boolean value (never null).

## Supported Data Types

- All data types are supported as input
- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- String types (StringType, BinaryType)
- Date and time types (DateType, TimestampType)
- Complex types (ArrayType, MapType, StructType)
- Boolean type

## Algorithm

- Evaluates the child expression against the input row
- Performs a null check using Java's `!=` operator against null
- Returns `true` if the evaluated value is not null
- Returns `false` if the evaluated value is null
- Uses code generation optimization when possible to avoid boxing/unboxing

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling
- Can be pushed down as a filter predicate
- Maintains existing partitioning scheme when used in filters

## Edge Cases

- Always returns a non-null boolean result (nullable = false)
- If child expression is context-independent foldable, this expression is also foldable
- Code generation handles compile-time optimization when child's null state is known
- Works correctly with complex nested data types

## Code Generation
This expression supports Tungsten code generation:

- Generates optimized Java code for null checking
- Handles compile-time optimizations when child's null state is deterministic
- Falls back to `TrueLiteral` when child is guaranteed non-null
- Falls back to `FalseLiteral` when child is guaranteed null
- Uses fresh variable names to avoid code generation conflicts

## Examples
```sql
-- Basic usage
SELECT name FROM users WHERE name IS NOT NULL;

-- Example from documentation
SELECT _FUNC_(1);
-- Returns: true

-- With complex expressions
SELECT * FROM orders WHERE (amount * tax_rate) IS NOT NULL;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.filter(col("name").isNotNull)

// With complex expressions
df.filter((col("amount") * col("tax_rate")).isNotNull)

// In select clause
df.select(col("id"), col("name").isNotNull.as("has_name"))
```

## See Also

- `IsNull` - Tests for null values
- `Coalesce` - Returns first non-null value from a list
- `IfNull` / `NullIf` - Conditional null handling expressions
- `AtLeastNNonNulls` - Tests for minimum number of non-null values