# InitCap

## Overview
InitCap is a Spark Catalyst expression that converts the first character of each word in a string to uppercase and the remaining characters to lowercase. It implements proper word capitalization logic with support for different string collations and can optionally use ICU (International Components for Unicode) libraries for more accurate case mappings.

## Syntax
```sql
initcap(str)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.initcap
df.select(initcap(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string to be converted to initial capitalization format |

## Return Type
Returns the same StringType as the input, preserving the original collation settings.

## Supported Data Types

- StringType with any collation that supports trim operations
- Maintains collation compatibility between input and output

## Algorithm

- Extracts the collation ID from the input StringType to maintain collation consistency
- Checks the ICU_CASE_MAPPINGS_ENABLED configuration to determine whether to use ICU or JVM case mappings
- Delegates the actual capitalization logic to CollationSupport.InitCap.exec() which handles word boundary detection
- Preserves the original string's collation properties in the result
- Uses null-safe evaluation to handle null inputs appropriately

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic row-level transformation
- Does not require shuffle operations
- Can be safely used in partitioned operations without affecting data distribution

## Edge Cases

- **Null handling**: Returns null when input is null (null-intolerant behavior)
- **Empty string**: Returns empty string unchanged
- **Single character**: Converts single character to uppercase if it's a letter
- **Non-alphabetic characters**: Preserves numbers, punctuation, and symbols unchanged
- **Unicode handling**: Behavior depends on ICU configuration - ICU provides more accurate Unicode case mappings than JVM defaults
- **Collation sensitivity**: Respects the input string's collation settings for case conversion rules

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It uses `defineCodeGen` with `CollationSupport.InitCap.genCode()` to generate optimized bytecode, avoiding interpreted mode execution for better performance in tight loops.

## Examples
```sql
-- Example SQL usage
SELECT initcap('sPark sql') AS result;
-- Result: 'Spark Sql'

SELECT initcap('hello WORLD') AS result;
-- Result: 'Hello World'

SELECT initcap('multiple   spaces') AS result;
-- Result: 'Multiple   Spaces'
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions.initcap

df.select(initcap(col("name"))).show()

// With column alias
df.select(initcap(col("description")).alias("formatted_desc"))
```

## See Also

- `upper()` - Converts entire string to uppercase
- `lower()` - Converts entire string to lowercase  
- `trim()` - Removes leading and trailing whitespace
- Other string manipulation functions in the string_funcs group