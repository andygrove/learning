# Spark Catalyst Interval Expressions Reference

## Overview

This module provides expressions for working with interval data types in Apache Spark SQL, including extraction of interval parts, creation of intervals, and arithmetic operations. These expressions support both legacy `CalendarInterval` types and ANSI-compliant `YearMonthIntervalType` and `DayTimeIntervalType` introduced in Spark 3.2.

## Interval Part Extraction Expressions

### ExtractIntervalPart (Legacy CalendarInterval)

#### Overview
Extracts specific time units (years, months, days, hours, minutes, seconds) from `CalendarInterval` objects using a unified abstract base class pattern.

#### Syntax
```sql
EXTRACT(field FROM interval_expression)
```

#### Available Extractors
- `ExtractIntervalYears` - Returns `IntegerType`
- `ExtractIntervalMonths` - Returns `ByteType` 
- `ExtractIntervalDays` - Returns `IntegerType`
- `ExtractIntervalHours` - Returns `ByteType`
- `ExtractIntervalMinutes` - Returns `ByteType`
- `ExtractIntervalSeconds` - Returns `DecimalType(8, 6)`

#### Algorithm
- Delegates to `IntervalUtils` functions (`getYears`, `getMonths`, etc.)
- Supports Tungsten code generation via `defineCodeGen`
- Null-intolerant (returns null if input is null)

### ExtractANSIIntervalPart (ANSI Intervals)

#### Overview
Extracts time units from ANSI-compliant interval types (`YearMonthIntervalType`, `DayTimeIntervalType`) with stricter type checking.

#### Supported Extractors
- `ExtractANSIIntervalYears/Months` - For `YearMonthIntervalType`
- `ExtractANSIIntervalDays/Hours/Minutes/Seconds` - For `DayTimeIntervalType`

#### Algorithm
- Validates that the requested unit is within the interval's defined range
- Uses same extraction functions but operates on primitive types (`Int` for YM, `Long` for DT)

---

## Interval Arithmetic Expressions

### MultiplyInterval / DivideInterval

#### Overview
Performs multiplication and division operations between `CalendarInterval` and numeric types with optional overflow checking based on ANSI mode.

#### Syntax
```sql
interval_expression * numeric_value
interval_expression / numeric_value
```

#### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| interval | CalendarIntervalType | Source interval |
| num | DoubleType | Numeric multiplier/divisor |
| failOnError | Boolean | Whether to throw on overflow (default: ANSI mode setting) |

#### Return Type
`CalendarIntervalType`

#### Algorithm
- Uses `IntervalUtils.multiplyExact/multiply` or `divideExact/divide`
- ANSI mode (`failOnError=true`) throws `ArithmeticException` on overflow
- Non-ANSI mode returns null on overflow

---

## Interval Creation Expressions

### MakeInterval

#### Overview
Creates `CalendarInterval` objects from individual time unit components with microsecond precision for seconds.

#### Syntax
```sql
make_interval([years[, months[, weeks[, days[, hours[, mins[, secs]]]]]]])
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
| secs | DecimalType(Decimal.MAX_LONG_DIGITS, 6) | Seconds with microsecond precision |

#### Return Type
`CalendarIntervalType`

#### Supported Data Types
- All integer types for time units
- High-precision decimal for seconds to preserve microsecond accuracy

#### Algorithm
- Converts weeks to days (weeks × 7)
- Validates against arithmetic overflow
- Preserves microsecond precision in seconds component
- Uses `IntervalUtils.makeInterval` for core logic

#### Edge Cases
- Null handling: Returns null if any argument is null
- Overflow: Throws `ArithmeticException` in ANSI mode, returns null otherwise
- Default values: Missing arguments default to 0

#### Code Generation
Supports Tungsten code generation with inline overflow checking and error handling.

#### Examples
```sql
SELECT make_interval(100, 11, 1, 1, 12, 30, 01.001001);
-- Result: 100 years 11 months 8 days 12 hours 30 minutes 1.001001 seconds

SELECT make_interval(0, 1, 0, 1, 0, 0, 100.000001);  
-- Result: 1 months 1 days 1 minutes 40.000001 seconds
```

### TryMakeInterval

#### Overview
Safe version of `make_interval` that returns NULL instead of throwing exceptions on overflow, implemented as a `RuntimeReplaceable` expression.

#### Syntax
```sql
try_make_interval([years[, months[, weeks[, days[, hours[, mins[, secs]]]]]]]) 
```

#### Return Type
`CalendarIntervalType` or `NULL`

#### Algorithm
- Wraps `MakeInterval` with `failOnError = false`
- Returns NULL on any overflow condition
- Otherwise identical behavior to `MakeInterval`

#### Examples
```sql
SELECT try_make_interval(2147483647);
-- Result: NULL (overflow)

SELECT try_make_interval(100, 11, 1, 1, 12, 30, 01.001001);
-- Result: 100 years 11 months 8 days 12 hours 30 minutes 1.001001 seconds
```

---

## ANSI Interval Creation Expressions

### MakeYMInterval

#### Overview
Creates ANSI-compliant year-month intervals with overflow checking and query context for error reporting.

#### Syntax
```sql
make_ym_interval([years[, months]])
```

#### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| years | IntegerType | Number of years |
| months | IntegerType | Number of months |

#### Return Type
`YearMonthIntervalType()`

#### Algorithm
- Uses `IntervalUtils.makeYearMonthInterval` with query context
- Normalizes months (e.g., 14 months → 1 year 2 months)
- Throws overflow exceptions with context information

#### Examples
```sql
SELECT make_ym_interval(1, 2);
-- Result: 1-2

SELECT make_ym_interval(-1, 1);  
-- Result: -0-11 (normalized)
```

### MakeDTInterval

#### Overview
Creates ANSI-compliant day-time intervals with microsecond precision and query context support.

#### Syntax
```sql
make_dt_interval([days[, hours[, mins[, secs]]]])
```

#### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| days | IntegerType | Number of days |
| hours | IntegerType | Number of hours | 
| mins | IntegerType | Number of minutes |
| secs | DecimalType(Decimal.MAX_LONG_DIGITS, 6) | Seconds with microsecond precision |

#### Return Type
`DayTimeIntervalType()`

#### Algorithm
- Converts all components to microseconds internally
- Uses `IntervalUtils.makeDayTimeInterval` with query context
- Validates against Long overflow for microsecond storage

#### Examples
```sql
SELECT make_dt_interval(1, 12, 30, 01.001001);
-- Result: 1 12:30:01.001001000

SELECT make_dt_interval(2);
-- Result: 2 00:00:00.000000000
```

---

## ANSI Interval Arithmetic

### MultiplyYMInterval / MultiplyDTInterval

#### Overview
Type-safe multiplication of ANSI intervals by numeric values with precision handling for different numeric types.

#### Supported Data Types
- **YearMonth**: `YearMonthIntervalType` × `NumericType`
- **DayTime**: `DayTimeIntervalType` × `NumericType`

#### Algorithm
- **Integer types**: Exact multiplication with overflow checking
- **Decimal types**: High-precision decimal arithmetic with rounding
- **Floating types**: Double-precision with HALF_UP rounding

### DivideYMInterval / DivideDTInterval

#### Overview
Type-safe division of ANSI intervals with comprehensive overflow and divide-by-zero checking.

#### Edge Cases
- **Divide by zero**: Throws `QueryExecutionErrors.intervalDividedByZeroError`
- **Integral overflow**: Special handling for `MIN_VALUE / -1` cases
- **Rounding**: Uses `HALF_UP` rounding mode for all numeric types

#### Partitioning Behavior
All interval expressions preserve partitioning as they operate on individual rows without requiring data redistribution.

#### Code Generation
All expressions support Tungsten code generation with optimized numeric type handling and inline error checking.

## See Also
- `IntervalUtils` - Core interval arithmetic and utility functions
- `CalendarInterval` - Legacy interval representation
- `YearMonthIntervalType` / `DayTimeIntervalType` - ANSI interval types
- Date/time extraction expressions for timestamp types