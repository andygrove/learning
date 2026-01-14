# SecondsOfTimeWithFraction

## Overview
SecondsOfTimeWithFraction extracts the seconds component from a time value and returns it as a decimal with fractional precision. This expression is implemented as a RuntimeReplaceable that delegates to DateTimeUtils for the actual computation, preserving subsecond precision based on the input time type's precision.

## Syntax
```sql
-- SQL syntax (function name may vary by implementation)
SECONDS_WITH_FRACTION(time_expression)
```

```scala
// DataFrame API usage
SecondsOfTimeWithFraction(timeColumn)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The time expression from which to extract seconds with fractional component |

## Return Type
DecimalType(8, 6) - A decimal with precision 8 and scale 6, allowing values up to 99.999999 seconds.

## Supported Data Types

- TimeType with any precision
- Any type conforming to AnyTimeType abstract data type

## Algorithm

- Determines the precision from the input TimeType, defaulting to MIN_PRECISION for non-TimeType inputs
- Creates a StaticInvoke expression that calls DateTimeUtils.getSecondsOfTimeWithFraction
- Passes the child expression and precision as arguments to the static method
- Returns a decimal value representing seconds with up to 6 decimal places of fractional precision
- Leverages Catalyst's code generation through StaticInvoke for optimized execution

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data partitioning since it's a row-level transformation
- Can be safely pushed down in query optimization

## Edge Cases

- Null input values are handled by the underlying DateTimeUtils implementation
- Non-TimeType inputs default to minimum precision (TimeType.MIN_PRECISION)
- Fractional seconds are preserved up to microsecond precision (6 decimal places)
- Invalid time values may result in null or error depending on DateTimeUtils behavior

## Code Generation
This expression supports Tungsten code generation through the StaticInvoke mechanism, which generates efficient Java code that directly calls the DateTimeUtils static method, avoiding interpreted expression evaluation overhead.

## Examples
```sql
-- Extract seconds with fractional component from time
SELECT SECONDS_WITH_FRACTION(TIME '14:30:25.123456') AS seconds_fraction;
-- Result: 25.123456
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.SecondsOfTimeWithFraction

val df = spark.range(1).select(
  SecondsOfTimeWithFraction(col("time_column")).as("seconds_with_fraction")
)
```

## See Also

- TimeExpression - Base trait for time-related expressions
- RuntimeReplaceable - Interface for expressions replaced at runtime
- DateTimeUtils - Utility class containing time computation methods
- StaticInvoke - Expression for calling static methods with code generation