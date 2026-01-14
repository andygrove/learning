# CollationKey

## Overview
The `CollationKey` expression generates a binary collation key from a string input based on the string's collation rules. This enables efficient comparison and sorting of strings according to locale-specific collation semantics by converting strings to binary keys that can be compared byte-wise.

## Syntax
```sql
COLLATION_KEY(string_expr)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.CollationKey
CollationKey(col("string_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Expression | String expression with collation information to generate collation key from |

## Return Type
`BinaryType` - Returns a binary array representing the collation key for the input string.

## Supported Data Types

- `StringTypeWithCollation` with trim collation support enabled
- Input must be a string type that contains collation metadata

## Algorithm

- Extracts the collation ID from the input string expression's data type
- Converts the input UTF8String to a collation-specific binary key using `CollationFactory.getCollationKeyBytes`
- The binary key preserves the collation ordering semantics, allowing byte-wise comparison
- Handles null inputs by returning null (via `nullSafeEval` mechanism)
- Uses the collation ID to determine the appropriate collation rules for key generation

## Partitioning Behavior
This expression affects partitioning behavior:

- Does not preserve existing partitioning schemes since it transforms string data to binary keys
- May require shuffle operations when used in grouping or sorting contexts
- The binary output enables consistent partitioning based on collation order

## Edge Cases

- **Null handling**: Returns null when input string is null (handled by `nullSafeEval`)
- **Empty string**: Generates a valid collation key for empty strings based on collation rules
- **Invalid collation ID**: Relies on `CollationFactory` to handle invalid or unsupported collation identifiers
- **Collation mismatch**: Requires input to be `StringTypeWithCollation` with trim support, enforced by `ExpectsInputTypes`

## Code Generation
Supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code calling `CollationFactory.getCollationKeyBytes` directly with the resolved collation ID.

## Examples
```sql
-- Generate collation keys for locale-specific string comparison
SELECT COLLATION_KEY(name) as name_key 
FROM customers 
WHERE name COLLATE 'en_US' > 'Smith';
```

```scala
// DataFrame API usage for sorting with collation
import org.apache.spark.sql.catalyst.expressions.CollationKey
import org.apache.spark.sql.functions._

val df = spark.table("customers")
val collationKeyExpr = CollationKey(col("name").expr)
df.select(col("name"), collationKeyExpr.as("name_key"))
  .orderBy("name_key")
```

## See Also

- `CollationFactory` - Factory class for collation operations and key generation
- `StringTypeWithCollation` - String data type with collation metadata
- Collation-aware string comparison expressions
- `UnaryExpression` - Base class for single-argument expressions