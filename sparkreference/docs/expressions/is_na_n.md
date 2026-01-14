# IsNaN

## Overview
The `IsNaN` expression checks whether a floating-point value is NaN (Not a Number). It returns `true` if the input value is NaN, and `false` otherwise, including for null inputs.

## Syntax
```sql
ISNAN(expr)
```

```scala
// DataFrame API
col("column_name").isNaN
isnan(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The floating-point expression to check for NaN |

## Return Type
`BooleanType` - Returns a boolean value indicating whether the input is NaN.

## Supported Data Types

- `DoubleType`
- `FloatType`

## Algorithm

- Evaluates the child expression to get the input value
- Returns `false` immediately if the input value is null
- For non-null values, calls the appropriate `isNaN()` method based on data type
- Uses `Double.isNaN()` for double values and `Float.isNaN()` for float values
- Always returns a non-null boolean result

## Partitioning Behavior
This expression preserves partitioning since it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be pushed down to individual partitions

## Edge Cases

- **Null handling**: Returns `false` for null inputs (expression is never nullable)
- **NaN values**: Returns `true` for both positive and negative NaN values
- **Infinity values**: Returns `false` for positive and negative infinity
- **Regular numbers**: Returns `false` for all finite floating-point numbers including zero

## Code Generation
This expression supports Tungsten code generation for both `DoubleType` and `FloatType` inputs. It generates optimized Java code that uses `Double.isNaN()` for runtime evaluation, avoiding the overhead of interpreted execution.

## Examples
```sql
-- Check for NaN values in a double column
SELECT ISNAN(CAST('NaN' AS DOUBLE));
-- Result: true

-- Check regular numeric value
SELECT ISNAN(42.5);
-- Result: false

-- Check null value
SELECT ISNAN(CAST(NULL AS DOUBLE));
-- Result: false

-- Check infinity
SELECT ISNAN(CAST('Infinity' AS DOUBLE));
-- Result: false
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Check for NaN values
df.select(isnan(col("double_col")))

// Filter out NaN values
df.filter(!isnan(col("price")))

// Count NaN values in a column
df.select(sum(when(isnan(col("value")), 1).otherwise(0)))
```

## See Also

- `IsNull` - Check for null values
- `IsNotNull` - Check for non-null values
- `Coalesce` - Handle null and NaN values with defaults
- `NaNvl` - Replace NaN values with alternative values