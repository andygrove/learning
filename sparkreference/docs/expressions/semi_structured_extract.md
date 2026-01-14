# SemiStructuredExtract

## Overview
The `SemiStructuredExtract` expression extracts data from a specified field within a semi-structured data column. It is designed to work with Variant data types and provides a mechanism for accessing nested or dynamically structured data within Spark SQL queries.

## Syntax
```sql
-- SQL syntax (via function or operator)
EXTRACT_FIELD(semi_structured_column, 'field_name')
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.SemiStructuredExtract

// Programmatic construction (internal API)
SemiStructuredExtract(columnExpression, "field_name")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `child` | `Expression` | The semi-structured column expression containing the data to extract from |
| `field` | `String` | The name of the field to extract from the semi-structured data |

## Return Type
Always returns `StringType`, regardless of the actual data type of the extracted field.

## Supported Data Types
- **Input**: Variant type columns only (semi-structured data)
- **Output**: String type

## Algorithm
- Accepts a semi-structured column (currently limited to Variant type) as input
- Extracts the specified field name from the semi-structured data
- Returns the extracted value as a string representation
- Expression remains unresolved (`resolved = false`) indicating it requires further processing during analysis
- Marked as `Unevaluable`, meaning it cannot be directly evaluated and must be transformed during query planning

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a projection operation that doesn't change row distribution
- **Requires shuffle**: No, operates on individual rows without requiring data movement across partitions

## Edge Cases
- **Null handling**: Behavior depends on the underlying implementation (not specified in the provided code)
- **Non-existent fields**: Behavior when the specified field doesn't exist in the semi-structured data is implementation-dependent
- **Type conversion**: All extracted values are converted to string format, potentially losing type information
- **Nested fields**: The current interface only supports top-level field names as strings

## Code Generation
This expression does **not** support Tungsten code generation. It extends `Unevaluable`, which means:
- Falls back to interpreted mode during execution
- Must be resolved and potentially replaced with evaluable expressions during query analysis phase
- Cannot be directly executed in generated code paths

## Examples
```sql
-- Example SQL usage (hypothetical syntax)
SELECT EXTRACT_FIELD(variant_column, 'user_id') as user_id
FROM semi_structured_table
WHERE variant_column IS NOT NULL;
```

```scala
// Example DataFrame API usage (internal/advanced usage)
import org.apache.spark.sql.catalyst.expressions._
import org.apache.spark.sql.types._

// Create expression programmatically
val childExpr = col("variant_data").expr
val extractExpr = SemiStructuredExtract(childExpr, "customer_name")

// Note: This would typically be used internally by Spark's query planner
// rather than directly by end users
```

## See Also
- `GetStructField` - For extracting fields from struct types
- `GetArrayItem` - For extracting elements from array types
- `GetMapValue` - For extracting values from map types
- Variant data type documentation
- Semi-structured data handling in Spark SQL