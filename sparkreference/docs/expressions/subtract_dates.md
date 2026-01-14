# SubtractDates

## Overview
SubtractDates is a binary expression that calculates the difference between two date values. It supports both legacy interval output (CalendarIntervalType) and the newer day-time interval format (DayTimeIntervalType) depending on configuration settings.

## Syntax
```sql
date1 - date2
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The left date operand (minuend) |
| right | Expression | The right date operand (subtrahend) |
| legacyInterval | Boolean | Flag determining output format (defaults to SQLConf.legacyIntervalEnabled) |

## Return Type
- **CalendarIntervalType**: When `legacyInterval` is true, returns a calendar interval with months=0, days=difference, microseconds=0
- **DayTimeIntervalType(DAY)**: When `legacyInterval` is false, returns a day-time interval representing the difference in microseconds

## Supported Data Types

- Input types: DateType for both left and right operands
- Implicit casting is supported through ImplicitCastInputTypes trait

## Algorithm

- Both input expressions are evaluated to get integer day values
- For legacy interval mode: calls `DateTimeUtils.subtractDates()` to create a CalendarInterval
- For day-time interval mode: performs `Math.subtractExact(leftDays, rightDays)` then multiplies by `MICROS_PER_DAY`
- Uses exact arithmetic operations to prevent overflow without detection
- The expression is null-intolerant, meaning null inputs produce null output

## Partitioning Behavior
This expression preserves partitioning characteristics since it operates on individual rows without requiring data movement:

- Does not affect partitioning schemes
- Does not require shuffle operations
- Can be safely pushed down in query optimization

## Edge Cases

- **Null handling**: Returns null if either input is null (null-intolerant behavior)
- **Overflow behavior**: Uses `Math.subtractExact()` and `Math.multiplyExact()` which throw ArithmeticException on overflow
- **Empty input**: Not applicable as this is a binary expression requiring two operands
- **Negative results**: Supported when left date is earlier than right date

## Code Generation
This expression fully supports Tungsten code generation through the `doGenCode` method:

- Legacy mode generates calls to `DateTimeUtils.subtractDates()`
- Day-time interval mode generates inline Math operations for optimal performance
- Falls back to interpreted evaluation only when code generation is disabled globally

## Examples
```sql
-- Basic date subtraction
SELECT DATE '2023-01-15' - DATE '2023-01-10' AS diff;

-- Using with table columns
SELECT order_date - ship_date AS processing_days FROM orders;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("end_date") - col("start_date") as "duration")

// Direct expression construction
val leftExpr = Literal(Date.valueOf("2023-01-15"))
val rightExpr = Literal(Date.valueOf("2023-01-10"))
val subtractExpr = SubtractDates(leftExpr, rightExpr)
```

## See Also

- AddMonths: For adding months to dates
- DateDiff: Alternative date difference calculation
- CalendarIntervalType: Legacy interval data type
- DayTimeIntervalType: Modern interval data type