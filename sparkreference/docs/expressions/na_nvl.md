# NaNvl

## Overview
The `NaNvl` expression returns the second argument if the first argument is NaN (Not a Number), otherwise returns the first argument. This function is specifically designed for floating-point numbers to handle NaN values in a controlled manner.

## Syntax
```sql
nanvl(expr1, expr2)
```

```scala
// DataFrame API
col("column1").nanvl(col("column2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The expression to check for NaN values (must be DoubleType or FloatType) |
| right | Expression | The expression to return if the left expression is NaN (must be DoubleType or FloatType) |

## Return Type
Returns the same data type as the left argument (DoubleType or FloatType).

## Supported Data Types

- DoubleType
- FloatType

Both arguments must be of the same floating-point type or will be implicitly cast to compatible types.

## Algorithm

- Evaluate the left expression first
- If the left value is null, return null
- If the left value is not NaN, return the left value
- If the left value is NaN, evaluate and return the right expression
- The right expression is only evaluated when needed (lazy evaluation)

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Preserves existing partitioning schemes
- Can be pushed down to individual partitions

## Edge Cases

- **Null handling**: If the left expression is null, the result is null regardless of the right expression
- **NaN detection**: Uses the native `isNaN()` method for both Float and Double types
- **Type compatibility**: Both arguments must be floating-point types (Float or Double)
- **Right expression evaluation**: The right expression is only evaluated if the left expression is NaN, providing performance optimization

## Code Generation
This expression supports Tungsten code generation (whole-stage code generation) and generates efficient Java code that avoids boxing/unboxing overhead for floating-point operations.

## Examples
```sql
-- Return 123.0 when the first argument is NaN
SELECT nanvl(cast('NaN' as double), 123.0);
-- Result: 123.0

-- Return the original value when it's not NaN
SELECT nanvl(45.67, 0.0);
-- Result: 45.67

-- Handle null values
SELECT nanvl(null, 999.0);
-- Result: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(nanvl(col("price"), lit(0.0)))

// With floating-point calculations that might produce NaN
df.select(nanvl(col("dividend") / col("divisor"), lit(-1.0)))
```

## See Also

- `coalesce` - for general null value replacement
- `isnull` - for null value checking  
- `isnan` - for NaN value detection
- `nvl` - for null value replacement (Oracle compatibility)