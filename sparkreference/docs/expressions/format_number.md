# FormatNumber

## Overview

The FormatNumber expression formats numeric values as strings using either a specified number of decimal places or a custom DecimalFormat pattern. It provides locale-aware number formatting with US locale configuration, using a dot (.) as the decimal separator and supporting comma-separated thousands groupings.

## Syntax

```sql
format_number(number, format)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| number | NumericType | The numeric value to format (supports Byte, Short, Int, Long, Float, Double, Decimal) |
| format | IntegerType or StringType | Either the number of decimal places (integer) or a custom DecimalFormat pattern string |

## Return Type

Returns `StringType` (UTF8String) containing the formatted numeric representation.

## Supported Data Types

**Input numeric types:**

- ByteType
- ShortType  
- IntegerType
- LongType
- FloatType
- DoubleType
- DecimalType

**Format parameter types:**

- IntegerType (number of decimal places)
- StringType (DecimalFormat pattern)

## Algorithm

- Caches DecimalFormat instances for performance, updating only when format parameter changes
- For integer format parameter: constructs pattern using default format "#,###,###,###,###,###,##0" with specified decimal places
- For string format parameter: applies the custom pattern directly to DecimalFormat
- Uses US Locale configuration to ensure consistent decimal separator behavior
- Converts input numeric value to appropriate Java type before formatting
- Returns null if integer format parameter is negative

## Partitioning Behavior

This expression preserves partitioning as it:

- Operates on individual rows without requiring data redistribution
- Does not require shuffle operations
- Can be applied within existing partitions

## Edge Cases

**Null handling:**

- Returns null if either input argument is null (nullIntolerant = true)
- Returns null if integer format parameter is negative

**Empty input behavior:**

- Empty string format parameter defaults to using the standard format pattern
- Numeric value of 0 formats according to specified pattern

**Format validation:**

- Invalid DecimalFormat patterns may cause runtime exceptions
- Negative decimal places (integer format) return null

## Code Generation

This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized code for both integer and string format parameters
- Maintains mutable state for cached DecimalFormat instances
- Uses null-safe code generation patterns
- Avoids object allocation in generated code paths

## Examples

```sql
-- Format with specific decimal places
SELECT format_number(12332.123456, 4);
-- Result: "12,332.1235"

-- Format with custom pattern
SELECT format_number(12332.123456, '##################.###');
-- Result: "12332.123"

-- Integer formatting
SELECT format_number(1234567, 0);
-- Result: "1,234,567"
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(format_number(col("amount"), 2))
df.select(format_number(col("price"), lit("$###,##0.00")))
```

## See Also

- `printf` - for C-style string formatting
- `round` - for numeric rounding operations
- `cast` - for basic type conversions