# ParseToDate

## Overview
ParseToDate is a Spark Catalyst expression that converts string values to date values using an optional format pattern. It serves as a runtime-replaceable expression that delegates to GetTimestamp and Cast operations internally, providing backward compatibility for date parsing operations.

## Syntax
```sql
to_date(date_str[, format])
```

```scala
// DataFrame API usage
df.select(to_date($"date_column"))
df.select(to_date($"date_column", "yyyy-MM-dd"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The input expression containing the date string or date-like value to convert |
| format | Option[Expression] | Optional format pattern string specifying how to parse the input |
| timeZoneId | Option[String] | Optional timezone identifier for date parsing (default: None) |
| ansiEnabled | Boolean | Whether ANSI SQL compliance mode is enabled, affecting error handling behavior |

## Return Type
DateType - Returns a date value representing the parsed input.

## Supported Data Types

- StringTypeWithCollation (with trim collation support)
- DateType  
- TimestampType
- TimestampNTZType

## Algorithm

- If a format expression is provided, creates a GetTimestamp operation with the input and format, then casts the result to DateType
- If no format is provided, performs a direct cast from the input to DateType for backward compatibility
- Applies timezone-aware processing when timeZoneId is specified
- Uses EvalMode based on ansiEnabled setting to determine error handling behavior
- Leverages ImplicitCastInputTypes for automatic type coercion of inputs

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual row values
- Maintains existing data partitioning since it's a row-level transformation
- Can be safely used in partition-by operations without affecting distribution

## Edge Cases

- Null input values are handled according to the underlying Cast operation behavior
- Invalid date strings may return null or throw exceptions based on ansiEnabled setting
- When ansiEnabled is true, invalid formats cause runtime exceptions
- When ansiEnabled is false, invalid formats typically return null values
- Empty strings are processed according to the Cast operation's null handling rules

## Code Generation
This expression supports code generation through its RuntimeReplaceable interface. The actual code generation is delegated to the replacement expression (GetTimestamp + Cast combination), which supports Tungsten code generation for optimized execution.

## Examples
```sql
-- Basic date parsing with default format
SELECT to_date('2016-12-31') AS parsed_date;

-- Date parsing with custom format
SELECT to_date('12/31/2016', 'MM/dd/yyyy') AS parsed_date;

-- Parsing timestamp to date
SELECT to_date(current_timestamp()) AS today;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic date conversion
df.select(to_date($"date_string"))

// With custom format
df.select(to_date($"date_string", "MM/dd/yyyy"))

// Converting timestamp column to date
df.select(to_date($"timestamp_column"))
```

## See Also

- GetTimestamp - underlying expression used for formatted date parsing
- Cast - used for direct type conversion when no format is specified  
- ParseToTimestamp - similar expression for parsing to timestamp type
- DateFormatClass - related date formatting expressions