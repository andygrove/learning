# Interval Expressions

## Overview

The interval expressions in Apache Spark Catalyst provide functionality for extracting components from intervals, performing arithmetic operations on intervals, and creating intervals from individual time unit components. These expressions support both legacy `CalendarInterval` types and ANSI standard `YearMonthIntervalType` and `DayTimeIntervalType` intervals, enabling comprehensive interval manipulation in SQL queries and DataFrame operations.

## ExtractIntervalPart Expressions

### Overview
The `ExtractIntervalPart` family of expressions extracts specific time unit components (years, months, days, hours, minutes, seconds) from interval values, supporting both CalendarInterval and ANSI interval types.

### Syntax
```sql
EXTRACT(field FROM interval_expression)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| field | String | Time unit to extract: YEAR, MONTH, DAY, HOUR, MINUTE, SECOND (with various aliases) |
| interval_expression | CalendarIntervalType/YearMonthIntervalType/DayTimeIntervalType | Source interval value |

### Return Type
- Years: `IntegerType`
- Months: `ByteType` 
- Days: `IntegerType`
- Hours: `ByteType`
- Minutes: `ByteType`
- Seconds: `DecimalType(8, 6)`

### Supported Data Types
- `CalendarIntervalType` - Legacy Spark interval type
- `YearMonthIntervalType` - ANSI year-month intervals
- `DayTimeIntervalType` - ANSI day-time intervals

### Algorithm
- Validates that the requested field exists in the interval type's range
- Routes to appropriate extract function based on interval type (Calendar vs ANSI)
- Uses `IntervalUtils` helper functions for actual extraction logic
- Supports code generation through Tungsten for optimized execution
- Returns null-safe results with proper type casting

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- No shuffle required
- Can be pushed down in predicate pushdown optimization

### Edge Cases
- Null intervals return null results (`nullIntolerant = true`)
- Throws `QueryCompilationErrors` for unsupported field/type combinations
- ANSI intervals validate field is within the interval's defined range
- Seconds extraction includes microsecond precision as decimal fraction

### Code Generation
Supports full code generation through `defineCodeGen`, generating optimized Java code that calls `IntervalUtils` methods directly.

### Examples
```sql
-- Extract years from calendar interval
SELECT EXTRACT(YEAR FROM INTERVAL '2-3' YEAR TO MONTH);
-- Returns: 2

-- Extract seconds with microsecond precision
SELECT EXTRACT(SECOND FROM INTERVAL '1 12:30:45.123456' DAY TO SECOND);  
-- Returns: 45.123456

-- Various field aliases supported
SELECT EXTRACT(YRS FROM interval_col), EXTRACT(MINS FROM interval_col);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(extract(lit("YEAR"), col("interval_col")))
```

## Interval Arithmetic Operations

### MultiplyInterval / DivideInterval

#### Overview
Arithmetic operations for multiplying and dividing `CalendarInterval` values by numeric types, with configurable overflow behavior based on ANSI mode.

#### Syntax
```sql
interval_expr * numeric_expr
interval_expr / numeric_expr
```

#### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| interval | CalendarIntervalType | Source interval value |
| num | DoubleType | Numeric multiplier/divisor |
| failOnError | Boolean | Whether to throw on overflow (default: ANSI mode setting) |

#### Algorithm
- Converts numeric input to Double type through implicit casting
- Delegates to `IntervalUtils.multiply/divide` or `multiplyExact/divideExact` methods
- In non-ANSI mode, returns null on overflow instead of throwing exception
- Supports code generation for optimized execution

### MultiplyYMInterval / MultiplyDTInterval

#### Overview
Specialized multiplication operations for ANSI year-month and day-time intervals with type-specific numeric handling.

#### Return Type
- `MultiplyYMInterval`: `YearMonthIntervalType()`
- `MultiplyDTInterval`: `DayTimeIntervalType()`

#### Algorithm
- Year-month intervals: Multiplies internal `Int` months value
- Day-time intervals: Multiplies internal `Long` microseconds value  
- Uses appropriate rounding modes for fractional results (HALF_UP)
- Different evaluation functions based on numeric input type (integral, decimal, fractional)

### DivideYMInterval / DivideDTInterval

#### Overview
Division operations for ANSI intervals with comprehensive overflow and divide-by-zero checking.

#### Edge Cases
- Throws `QueryExecutionErrors.intervalDividedByZeroError` on division by zero
- Checks for overflow when dividing minimum values by -1
- Uses `HALF_UP` rounding mode for fractional results
- Integral division uses Google Guava's `IntMath`/`LongMath` for overflow safety

## Interval Creation Functions

### MakeInterval

#### Overview
Creates `CalendarInterval` objects from individual time unit components with optional overflow handling.

#### Syntax
```sql
MAKE_INTERVAL([years[, months[, weeks[, days[, hours[, mins[, secs]]]]]]])
```

#### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| years | IntegerType | Number of years (positive or negative) |
| months | IntegerType | Number of months (positive or negative) |
| weeks | IntegerType | Number of weeks (positive or negative) |
| days | IntegerType | Number of days (positive or negative) |
| hours | IntegerType | Number of hours (positive or negative) |
| mins | IntegerType | Number of minutes (positive or negative) |
| secs | DecimalType(MAX_LONG_DIGITS, 6) | Seconds with microsecond precision |

#### Algorithm
- Accepts up to 7 parameters with default values for omitted arguments
- Uses high-precision `DecimalType` for seconds to preserve microsecond accuracy
- Validates arguments don't cause arithmetic overflow in strict mode
- Converts weeks to days (weeks × 7) during interval construction

### TryMakeInterval

#### Overview
Safe version of `MakeInterval` that returns null instead of throwing exceptions on overflow.

#### Return Type
`CalendarIntervalType` or null on overflow

### MakeDTInterval / MakeYMInterval  

#### Overview
Create ANSI-compliant day-time and year-month intervals with proper error context handling.

#### Syntax
```sql
MAKE_DT_INTERVAL([days[, hours[, mins[, secs]]]])
MAKE_YM_INTERVAL([years[, months]])
```

#### Return Type
- `MakeDTInterval`: `DayTimeIntervalType()`
- `MakeYMInterval`: `YearMonthIntervalType()`

### Partitioning Behavior
- All interval creation functions preserve partitioning
- Deterministic for the same inputs
- Can be used in partitioning expressions

### Edge Cases
- Any null input parameter results in null output (`nullIntolerant = true`)
- Arithmetic overflow behavior controlled by `failOnError` parameter
- `TryMakeInterval` never throws, always returns null on overflow
- ANSI interval functions include `QueryContext` for enhanced error reporting

### Code Generation
All interval creation functions support full code generation with proper exception handling branches and optimized arithmetic operations.

### Examples
```sql
-- Create complex interval
SELECT MAKE_INTERVAL(1, 2, 0, 5, 12, 30, 45.123);
-- Returns: 1 years 2 months 5 days 12 hours 30 minutes 45.123 seconds

-- Create day-time interval  
SELECT MAKE_DT_INTERVAL(5, 12, 30, 0);
-- Returns: 5 12:30:00.000000000

-- Safe interval creation
SELECT TRY_MAKE_INTERVAL(2147483647, 0, 0, 0, 0, 0, 0);
-- Returns: NULL (overflow)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(make_interval(lit(1), lit(6), lit(0), lit(15)))
```

## See Also
- `DateAdd`, `DateSub` for date arithmetic with intervals
- `TimestampAdd`, `TimestampSub` for timestamp arithmetic  
- `IntervalUtils` utility class for low-level interval operations
- ANSI SQL interval data types documentation