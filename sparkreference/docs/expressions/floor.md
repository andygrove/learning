# Floor

## Overview
The Floor expression computes the largest integer less than or equal to the input value. It extends UnaryMathExpression and uses `math.floor` as the underlying mathematical function, with optimized handling for decimal and long integer types.

## Syntax
```sql
FLOOR(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.floor
df.select(floor(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the floor value for |

## Return Type
The return type depends on the input data type:

- For `DecimalType` with scale 0: Returns the same `DecimalType`
- For `DecimalType` with scale > 0: Returns `DecimalType.bounded(precision - scale + 1, 0)`
- For all other supported types: Returns `LongType`

## Supported Data Types
The expression accepts the following input data types:

- `DoubleType`
- `DecimalType` (any precision and scale)
- `LongType`

## Algorithm
The evaluation algorithm varies by input data type:

- For `LongType`: Returns the input value unchanged (already an integer)
- For `DoubleType`: Applies `math.floor()` function and converts result to Long
- For `DecimalType`: Uses the Decimal class's built-in `floor()` method
- Null inputs are handled by the parent class and return null results

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffling
- Can be applied within each partition independently
- Maintains existing data distribution patterns

## Edge Cases

- **Null handling**: Null inputs return null outputs (handled by UnaryMathExpression parent class)
- **Long integer inputs**: Values are returned unchanged since they are already integers
- **Decimal precision**: For decimals with scale 0, the original type is preserved
- **Decimal scale reduction**: For decimals with scale > 0, the result has scale 0 with adjusted precision
- **Double overflow**: Large double values may overflow when converted to Long type

## Code Generation
This expression supports Tungsten code generation with optimized paths:

- **DecimalType with scale 0**: Generates identity code (`$c`)
- **DecimalType with scale > 0**: Generates `$c.floor()` method call
- **LongType**: Generates identity code (`$c`)
- **Other types**: Generates `(long)(java.lang.Math.FLOOR($c))` with explicit casting

## Examples
```sql
-- Basic floor operations
SELECT FLOOR(3.7);        -- Returns 3
SELECT FLOOR(-2.1);       -- Returns -3
SELECT FLOOR(5.0);        -- Returns 5
SELECT FLOOR(42);         -- Returns 42

-- With decimal types
SELECT FLOOR(CAST(123.456 AS DECIMAL(6,3)));  -- Returns 123 as DECIMAL(4,0)
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions.floor

// Apply floor to a numeric column
df.select(floor(col("price")))

// Floor operation in transformations
df.withColumn("price_floor", floor(col("price")))

// Combined with other operations
df.select(floor(col("rating") * 2.5))
```

## See Also

- `Ceil` - Computes the ceiling (smallest integer greater than or equal to input)
- `Round` - Rounds to the nearest integer or specified decimal places
- `Truncate` - Truncates decimal places without rounding