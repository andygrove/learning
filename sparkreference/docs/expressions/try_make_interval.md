# TryMakeInterval

## Overview
The `TryMakeInterval` expression creates an interval from separate components (years, months, weeks, days, hours, minutes, seconds). Unlike `MakeInterval`, this expression returns `NULL` instead of throwing an exception when an error occurs during interval creation. It is implemented as a `RuntimeReplaceable` expression that delegates to `MakeInterval` with `failOnError = false`.

## Syntax
```sql
try_make_interval([years [, months [, weeks [, days [, hours [, mins [, secs]]]]]]])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| years | Expression | Number of years (optional, defaults to 0) |
| months | Expression | Number of months (optional, defaults to 0) |
| weeks | Expression | Number of weeks (optional, defaults to 0) |
| days | Expression | Number of days (optional, defaults to 0) |
| hours | Expression | Number of hours (optional, defaults to 0) |
| mins | Expression | Number of minutes (optional, defaults to 0) |
| secs | Expression | Number of seconds as Decimal (optional, defaults to 0) |

## Return Type
Returns `INTERVAL` data type or `NULL` if an error occurs during interval construction.

## Supported Data Types
- **Numeric types**: All numeric expressions are supported for input parameters
- **Decimal**: The seconds parameter specifically uses Decimal type with `MAX_LONG_DIGITS` precision and scale of 6
- **Integer literals**: Default values use integer literals (0) for most parameters

## Algorithm
- Validates and converts input expressions to appropriate numeric types
- Delegates actual interval creation to the underlying `MakeInterval` expression
- Sets `failOnError = false` to ensure NULL return instead of exceptions
- Uses `RuntimeReplaceable` pattern for expression rewriting during analysis
- Supports variable number of arguments through constructor overloading

## Partitioning Behavior
- **Preserves partitioning**: This expression operates on individual rows and does not require data movement
- **No shuffle required**: Row-level computation that maintains existing data distribution
- **Deterministic**: Given the same inputs, always produces the same output

## Edge Cases
- **Null handling**: Returns `NULL` if any input parameter is `NULL`
- **Invalid intervals**: Returns `NULL` instead of throwing exceptions for invalid interval combinations
- **Overflow conditions**: Returns `NULL` when interval components exceed valid ranges
- **Missing parameters**: Automatically fills missing parameters with appropriate zero values (Literal(0) for most, Decimal(0) for seconds)
- **Empty constructor**: Intentionally not supported in try version as it would never overflow

## Code Generation
This expression supports Tungsten code generation through its `RuntimeReplaceable` implementation. The expression is replaced with `MakeInterval` during analysis phase, which then benefits from the underlying `MakeInterval` code generation capabilities.

## Examples
```sql
-- Create interval with all components
SELECT try_make_interval(1, 2, 3, 4, 5, 6, 7.5);

-- Create interval with partial components
SELECT try_make_interval(2, 3);

-- Handle invalid input gracefully (returns NULL)
SELECT try_make_interval(9999999, 9999999, 9999999);

-- Compare with make_interval behavior
SELECT 
  try_make_interval(1, NULL, 3) as safe_result,  -- Returns NULL
  make_interval(1, NULL, 3) as unsafe_result;    -- Throws exception
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Create interval column
df.select(try_make_interval(col("years"), col("months"), col("days")))

// With literal values
df.select(try_make_interval(lit(1), lit(6), lit(0), lit(15)))

// Handle potentially invalid data
df.select(try_make_interval(col("user_years"), col("user_months")))
  .filter(col("interval_col").isNotNull)
```

## See Also
- `MakeInterval` - The non-safe version that throws exceptions on errors
- `INTERVAL` literal syntax - Direct interval creation
- Date/time arithmetic functions for interval operations