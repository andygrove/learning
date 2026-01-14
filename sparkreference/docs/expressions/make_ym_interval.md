# MakeYMInterval

## Overview
The `MakeYMInterval` expression creates a year-month interval value from separate year and month integer components. It constructs a `YearMonthIntervalType` object that represents a duration in terms of years and months, which is useful for date arithmetic operations in Spark SQL.

## Syntax
```sql
make_ym_interval(years, months)
make_ym_interval(years)  -- months defaults to 0
make_ym_interval()       -- both years and months default to 0
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| years | Integer | The number of years for the interval (optional, defaults to 0) |
| months | Integer | The number of months for the interval (optional, defaults to 0) |

## Return Type
Returns `YearMonthIntervalType()` - a year-month interval data type.

## Supported Data Types
- **Input Types**: Only `IntegerType` for both years and months parameters
- **Output Type**: `YearMonthIntervalType`
- Implicit casting is applied to convert compatible numeric types to integers

## Algorithm
- Accepts two integer parameters representing years and months
- Validates input values through `makeYearMonthInterval` utility function with query context for error reporting
- Creates a year-month interval object that stores the total duration
- Applies implicit type casting to ensure inputs are integers
- Maintains query context for detailed error messages when validation fails

## Partitioning Behavior
- **Preserves Partitioning**: Yes, this is a deterministic expression that doesn't require data movement
- **Shuffle Required**: No, the expression operates on individual row values independently
- Can be safely used in partitioned operations without affecting partition structure

## Edge Cases
- **Null Handling**: Expression is null-intolerant (`nullIntolerant = true`), meaning if either input is null, the result is null
- **Empty Input**: Default constructor provides zero values for both years and months
- **Overflow Behavior**: Depends on the underlying `makeYearMonthInterval` implementation - likely throws runtime exceptions for values outside valid interval ranges
- **Negative Values**: Accepts negative integers to create negative intervals (e.g., intervals representing past durations)

## Code Generation
Supports Spark's Tungsten code generation through the `doGenCode` method. Generated code calls `IntervalUtils.makeYearMonthInterval` directly, avoiding interpretation overhead in hot code paths. Includes proper error context propagation in generated code.

## Examples
```sql
-- Create a 2-year, 3-month interval
SELECT make_ym_interval(2, 3);
-- Returns: INTERVAL '2-3' YEAR TO MONTH

-- Create a 1-year interval (months default to 0)
SELECT make_ym_interval(1);
-- Returns: INTERVAL '1-0' YEAR TO MONTH

-- Create zero interval
SELECT make_ym_interval();
-- Returns: INTERVAL '0-0' YEAR TO MONTH

-- Use in date arithmetic
SELECT date '2023-01-01' + make_ym_interval(1, 6);
-- Returns: 2024-07-01
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("make_ym_interval(2, 3)"))

// Using with date arithmetic
df.withColumn("future_date", col("start_date") + expr("make_ym_interval(1, 6)"))
```

## See Also
- `MakeDTInterval` - Creates day-time intervals
- `INTERVAL` literal syntax - Alternative way to create intervals
- Date/timestamp arithmetic functions that work with intervals
- `YearMonthIntervalType` - The underlying data type