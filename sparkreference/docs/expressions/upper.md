# Upper

## Overview
The `Upper` expression converts all characters in a string to uppercase. It supports various collations and uses either ICU or JVM case mappings depending on configuration and collation type.

## Syntax
```sql
UPPER(str)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.upper
df.select(upper($"column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | StringType | The input string to convert to uppercase |

## Return Type
Returns `StringType` with the same collation as the input string.

## Supported Data Types

- StringType (all collations)

## Algorithm

- Extracts the collation ID from the input StringType
- Determines whether to use ICU case mappings based on `spark.sql.collation.icu.enabled` configuration
- Delegates the actual uppercase conversion to `CollationSupport.Upper.exec()` with the appropriate collation and ICU settings
- Preserves the original collation of the input string in the result
- Uses collation-aware case mapping rules for proper internationalization support

## Partitioning Behavior

- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down in query optimization

## Edge Cases

- **Null handling**: Returns null for null input (null-intolerant behavior)
- **Empty string**: Returns empty string unchanged
- **Unicode characters**: Handles international characters correctly based on collation rules
- **Collation sensitivity**: Respects different collation rules for case mapping
- **ICU vs JVM**: Behavior may vary between ICU and JVM case mappings for certain Unicode characters

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which calls `CollationSupport.Upper.genCode()` to generate optimized bytecode for the uppercase conversion operation.

## Examples
```sql
-- Basic usage
SELECT UPPER('SparkSql');
-- Result: SPARKSQL

-- With null input
SELECT UPPER(NULL);
-- Result: NULL

-- With international characters
SELECT UPPER('café');
-- Result: CAFÉ

-- With empty string
SELECT UPPER('');
-- Result: ''
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.upper

val df = Seq("SparkSql", "hello world", "ALREADY_UPPER").toDF("text")
df.select(upper($"text").as("upper_text")).show()

// Result:
// +----------+
// |upper_text|
// +----------+
// |  SPARKSQL|
// |HELLO WORLD|
// |ALREADY_UPPER|
// +----------+
```

## See Also

- `Lower` - Converts strings to lowercase
- `InitCap` - Converts strings to title case
- String collation functions for locale-specific string operations