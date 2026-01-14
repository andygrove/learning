# Empty2Null

## Overview
The `Empty2Null` expression converts empty strings to null values specifically for partition column handling in V1 data source writes. This internal function ensures proper null representation in partitioned datasets where empty strings should be treated as null partition values.

## Syntax
This is an internal expression not directly accessible through SQL or DataFrame API. It is automatically applied during V1 write operations for partition columns.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that evaluates to a string value |

## Return Type
UTF8String (or null)

## Supported Data Types

- String types (UTF8String)
- Any expression that produces string output

## Algorithm

- Evaluates the child expression to get a UTF8String value
- Checks if the resulting string has zero bytes (empty string)
- Returns null if the string is empty, otherwise returns the original string unchanged
- Preserves all non-empty string values including whitespace-only strings
- Uses byte-level checking for optimal performance

## Partitioning Behavior
How this expression affects partitioning:

- Specifically designed for partition column processing in V1 writes
- Does not affect data distribution or require shuffles
- Ensures consistent null representation across partition boundaries
- Maintains partition pruning capabilities by normalizing empty values

## Edge Cases

- Null handling: Input nulls are preserved as nulls (handled by UnaryExpression)
- Empty input: Empty strings ("") are converted to null values
- Whitespace strings: Strings containing only spaces are preserved unchanged
- Zero-width characters: Strings with zero-width Unicode characters may still have bytes > 0
- Memory efficiency: Uses numBytes() check rather than string comparison for performance

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized bytecode that:

- Performs null-safe evaluation using `nullSafeCodeGen`
- Uses efficient byte count checking (`numBytes() == 0`)
- Directly sets null flags and values without boxing overhead
- Avoids string object creation for the comparison

## Examples
```sql
-- Not directly accessible in SQL
-- Applied internally during partition writes
```

```scala
// Not directly accessible in DataFrame API
// Used internally by Spark during V1 write operations
// Example of internal usage context:
// partitionColumns.map(col => Empty2Null(col))
```

## See Also

- String2StringExpression (parent trait)
- UnaryExpression (base class)
- V1 Write operations and partition handling
- Partition column null handling strategies