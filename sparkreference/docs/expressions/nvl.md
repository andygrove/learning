# Nvl

## Overview
The `Nvl` expression returns the first non-null value from two expressions. It is a conditional function that provides a null-safe way to substitute a default value when the primary expression evaluates to null.

## Syntax
```sql
NVL(expr1, expr2)
```

```scala
// DataFrame API
col("column_name").isNull.when(col("default_value"))
// or using coalesce
coalesce(col("expr1"), col("expr2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The primary expression to evaluate |
| right | Expression | The fallback expression used when left is null |

## Return Type
Returns the same data type as the input expressions. Both expressions must be of compatible types or castable to a common type.

## Supported Data Types
All Spark SQL data types are supported:

- Numeric types (IntegerType, LongType, DoubleType, DecimalType, etc.)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Complex types (ArrayType, MapType, StructType)
- Binary types (BinaryType)

## Algorithm
The expression evaluation follows these steps:

- Evaluate the left (primary) expression
- If the left expression is not null, return its value
- If the left expression is null, evaluate and return the right expression
- The implementation internally uses `Coalesce(Seq(left, right))` for actual evaluation
- Runtime replacement occurs during query planning phase

## Partitioning Behavior
This expression has neutral partitioning behavior:

- Preserves existing partitioning schemes
- Does not require data shuffle operations
- Can be pushed down to individual partitions for evaluation
- Does not affect partition pruning capabilities

## Edge Cases

- When both expressions are null, returns null
- No type coercion is performed automatically - expressions must be type compatible
- Empty strings are treated as valid non-null values
- For complex types (arrays, maps), empty collections are considered non-null values
- Expression evaluation is lazy - right expression is only evaluated if left is null

## Code Generation
This expression supports Tungsten code generation through its underlying `Coalesce` implementation. The generated code includes:

- Null-check branching logic
- Optimized evaluation path that skips right expression when left is non-null
- Efficient memory management for complex data types

## Examples
```sql
-- Basic null substitution
SELECT NVL(NULL, 'default_value');
-- Returns: "default_value"

-- Non-null value preservation  
SELECT NVL('existing_value', 'default_value');
-- Returns: "existing_value"

-- With array types
SELECT NVL(NULL, array('2'));
-- Returns: ["2"]

-- With column references
SELECT NVL(customer_name, 'Unknown Customer') FROM customers;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Using coalesce (equivalent to NVL)
df.select(coalesce(col("primary_col"), col("backup_col")))

// Using when/otherwise pattern
df.select(when(col("primary_col").isNull, col("backup_col"))
          .otherwise(col("primary_col")))
```

## See Also

- `Coalesce` - Handles multiple expressions, not just two
- `IfNull` - Similar null-handling function
- `IsNull` / `IsNotNull` - Null checking expressions
- `Case` / `When` - More complex conditional logic