# Sample GitHub Issue for `levenshtein` Expression

**Title:** `[Feature] Support Spark expression: levenshtein`

---

## What is the problem the feature request solves?

Comet does not currently support the Spark `levenshtein` string function, causing queries using this function to fall back to Spark's JVM execution instead of running natively on DataFusion.

The Levenshtein expression computes the Levenshtein distance (also known as edit distance) between two strings. This represents the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform one string into another. An optional threshold parameter can be provided to limit the maximum distance calculated.

This is a commonly used string similarity function for fuzzy matching, data deduplication, and text analysis workloads.

## Describe the potential solution

### Spark Specification

**Syntax:**
```sql
LEVENSHTEIN(str1, str2)
LEVENSHTEIN(str1, str2, threshold)
```

**Arguments:**

| Argument | Type | Description |
|----------|------|-------------|
| str1 | String | The first input string for comparison |
| str2 | String | The second input string for comparison |
| threshold | Integer (optional) | Maximum distance to calculate; computation stops early if distance exceeds this value |

**Return Type:** Integer - representing the Levenshtein distance between the two input strings.

**Supported Data Types:**
- Input strings: StringType with collation support
- Threshold: IntegerType
- Output: IntegerType

**Edge Cases:**
- **Null handling**: Returns null if any input parameter (left, right, or threshold) is null
- **Empty strings**: Handles empty strings correctly - distance equals the length of the non-empty string
- **Identical strings**: Returns 0 for identical input strings
- **Threshold behavior**: When threshold is provided, computation may terminate early if distance exceeds the threshold value

**Examples:**
```sql
-- Basic usage
SELECT LEVENSHTEIN('kitten', 'sitting');  -- Returns 3

-- With threshold
SELECT LEVENSHTEIN('kitten', 'sitting', 5);  -- Returns 3

-- Null handling
SELECT LEVENSHTEIN('test', NULL);  -- Returns NULL

-- Empty strings
SELECT LEVENSHTEIN('', 'abc');  -- Returns 3
```

### Implementation Approach

1. **Scala Serde** (`spark/src/main/scala/org/apache/comet/serde/strings.scala`):
   - Add `CometLevenshtein` expression handler
   - Register in `QueryPlanSerde.scala` stringExpressions map

2. **Protobuf** (`native/proto/src/proto/expr.proto`):
   - Add message type if needed, or use `ScalarFunc`

3. **Rust Implementation** (`native/spark-expr/src/`):
   - DataFusion has a built-in `levenshtein` function that may be usable
   - May need wrapper for threshold parameter support

## Additional context

**Spark Expression Class:** `org.apache.spark.sql.catalyst.expressions.Levenshtein`

**DataFusion Support:** DataFusion has a built-in `levenshtein(str1, str2)` function. The threshold variant may require custom implementation.

**Related Expressions:**
- `soundex` - Phonetic similarity (also not yet supported in Comet)

**Difficulty:** Medium - Basic version maps to DataFusion function, threshold variant needs additional work.

---

*This issue was auto-generated from Spark reference documentation.*
