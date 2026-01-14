# Left

## Overview
The `Left` expression extracts a specified number of characters from the left side of a string or binary value. This expression is implemented as a `RuntimeReplaceable` that internally uses the `Substring` expression with a starting position of 1.

## Syntax
```sql
LEFT(str, len)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(left(col("column_name"), 5))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String/Binary | The input string or binary data from which to extract characters |
| len | Integer | The number of characters to extract from the left side |

## Return Type
Returns the same data type as the input `str` argument:

- String input returns String
- Binary input returns Binary

## Supported Data Types

- **String types**: All string types with collation support (specifically those supporting trim collation)
- **Binary type**: Raw binary data

## Algorithm

- Validates input types ensuring `str` is string/binary and `len` is integer
- Performs implicit type casting when necessary through `ImplicitCastInputTypes`
- Internally replaces the expression with `Substring(str, Literal(1), len)` at runtime
- The substring operation starts at position 1 (1-based indexing) and extracts `len` characters
- Leverages the existing `Substring` expression implementation for actual evaluation

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains existing data partitioning since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: If either `str` or `len` is null, the result is null
- **Negative length**: Behavior depends on underlying `Substring` implementation
- **Length exceeds string**: Returns the entire string when `len` is greater than string length
- **Zero length**: Returns empty string when `len` is 0
- **Empty string input**: Returns empty string regardless of `len` value

## Code Generation
This expression supports Tungsten code generation through its `RuntimeReplaceable` nature:

- The replacement `Substring` expression supports code generation
- Compilation occurs at query planning time, replacing `Left` with optimized `Substring` code
- Falls back to interpreted mode only if the underlying `Substring` expression cannot be code-generated

## Examples
```sql
-- Extract first 3 characters
SELECT LEFT('Apache Spark', 3); -- Returns 'Apa'

-- With column reference
SELECT LEFT(name, 5) FROM users;

-- With binary data
SELECT LEFT(CAST('binary_data' AS BINARY), 4);
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Extract first 3 characters
df.select(left(col("text_column"), 3))

// Dynamic length based on another column
df.select(left(col("description"), col("max_length")))

// With literal string
df.select(left(lit("Apache Spark"), 5))
```

## See Also

- `Substring` - The underlying expression used for implementation
- `Right` - Extracts characters from the right side of a string
- `Mid`/`Substr` - General substring extraction with custom start position