# Apache Spark Catalyst Bitmap Expressions

This reference documentation covers the bitmap-related expressions introduced in Apache Spark SQL for efficient bitmap operations and aggregations.

## BitmapBucketNumber

### Overview
BitmapBucketNumber calculates the bucket number for a given input value, typically used in bitmap indexing operations. This is a utility function for determining which bucket a particular value belongs to in a bitmap data structure.

### Syntax
```sql
bitmap_bucket_number(child)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BIGINT | The input value for which to calculate the bucket number |

### Return Type
`BIGINT` - Returns the bucket number as a long integer.

### Supported Data Types
- Input: `LongType` (BIGINT) - other numeric types are implicitly cast to BIGINT

### Algorithm
- Takes a long integer input value
- Delegates computation to `BitmapExpressionUtils.bitmapBucketNumber()`
- Uses static method invocation for runtime replacement
- Implements implicit type casting for numeric inputs
- Returns non-nullable result

### Partitioning Behavior
- Preserves partitioning as it's a deterministic unary expression
- No shuffle required
- Can be pushed down to data sources

### Edge Cases
- Returns 0 for input value 0
- Returns 1 for input value 123 (as shown in examples)
- Implicit casting may cause precision loss for very large numbers
- Non-nullable return type - never returns null even for null input

### Code Generation
Uses `RuntimeReplaceable` with `StaticInvoke`, enabling code generation through Tungsten for optimal performance.

### Examples
```sql
-- Basic usage
SELECT bitmap_bucket_number(123);  -- Returns 1
SELECT bitmap_bucket_number(0);    -- Returns 0

-- With table data
SELECT id, bitmap_bucket_number(id) as bucket 
FROM my_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(col("id"), expr("bitmap_bucket_number(id)").alias("bucket"))
```

### See Also
- `bitmap_bit_position()` - Related bitmap utility function

---

## BitmapBitPosition

### Overview
BitmapBitPosition calculates the bit position for a given input value, determining where a specific value should be positioned within a bitmap structure. This is essential for bitmap indexing and bit manipulation operations.

### Syntax
```sql
bitmap_bit_position(child)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BIGINT | The input value for which to calculate the bit position |

### Return Type
`BIGINT` - Returns the bit position as a long integer.

### Supported Data Types
- Input: `LongType` (BIGINT) - other numeric types are implicitly cast to BIGINT

### Algorithm
- Takes a long integer input value
- Delegates computation to `BitmapExpressionUtils.bitmapBitPosition()`
- Calculates the zero-based bit position for the input value
- Uses static method invocation for runtime replacement
- Returns non-nullable result

### Partitioning Behavior
- Preserves partitioning as it's a deterministic unary expression
- No shuffle required
- Can be pushed down to data sources

### Edge Cases
- Returns 0 for input value 1
- Returns 122 for input value 123 (value - 1)
- Non-nullable return type - never returns null even for null input
- Implicit casting may cause precision loss for very large numbers

### Code Generation
Uses `RuntimeReplaceable` with `StaticInvoke`, enabling code generation through Tungsten for optimal performance.

### Examples
```sql
-- Basic usage
SELECT bitmap_bit_position(1);    -- Returns 0
SELECT bitmap_bit_position(123);  -- Returns 122

-- Use with bitmap construction
SELECT bitmap_construct_agg(bitmap_bit_position(id)) 
FROM my_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(col("id"), expr("bitmap_bit_position(id)").alias("bit_pos"))
```

### See Also
- `bitmap_bucket_number()` - Related bitmap utility function
- `bitmap_construct_agg()` - Uses bit positions to build bitmaps

---

## BitmapCount

### Overview
BitmapCount returns the number of set bits (1-bits) in a binary bitmap. This function is used to count the cardinality of a bitmap, determining how many distinct values are represented in the bitmap structure.

### Syntax
```sql
bitmap_count(child)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BINARY | The bitmap data as binary type |

### Return Type
`BIGINT` - Returns the count of set bits as a long integer.

### Supported Data Types
- Input: `BinaryType` only - no implicit casting available
- Strict type checking enforced at analysis time

### Algorithm
- Validates input is of BinaryType during type checking phase
- Delegates computation to `BitmapExpressionUtils.bitmapCount()`
- Counts all bits set to 1 in the binary data
- Uses static method invocation for runtime replacement
- Returns non-nullable result

### Partitioning Behavior
- Preserves partitioning as it's a deterministic unary expression
- No shuffle required
- Can be pushed down to data sources that support binary operations

### Edge Cases
- Returns 0 for empty bitmaps or bitmaps with no set bits
- Strict type checking - throws `DataTypeMismatch` error for non-binary inputs
- Non-nullable return type
- Handles binary data of any length

### Code Generation
Uses `RuntimeReplaceable` with `StaticInvoke`, enabling code generation through Tungsten for optimal performance.

### Examples
```sql
-- Basic usage with hex literals
SELECT bitmap_count(X'1010');  -- Returns 2 (binary: 00010000 00010000)
SELECT bitmap_count(X'FFFF');  -- Returns 16 (all bits set in 2 bytes)
SELECT bitmap_count(X'0');     -- Returns 0

-- With constructed bitmaps
SELECT bitmap_count(bitmap_construct_agg(bitmap_bit_position(id))) 
FROM my_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("bitmap_count(bitmap_column)").alias("bit_count"))
```

### See Also
- `bitmap_construct_agg()` - Creates bitmaps for counting
- `bitmap_or_agg()` - Combines bitmaps that can be counted

---

## BitmapConstructAgg

### Overview
BitmapConstructAgg is an aggregate function that constructs a bitmap by setting bits at positions specified by the input values. It collects all position values from the child expression and creates a single bitmap with those positions set to 1.

### Syntax
```sql
bitmap_construct_agg(child)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BIGINT | The bit positions to set in the constructed bitmap |

### Return Type
`BINARY` - Returns a fixed-size binary bitmap.

### Supported Data Types
- Input: `LongType` (BIGINT) - other numeric types are implicitly cast to BIGINT

### Algorithm
- Initializes a fixed-size bitmap buffer with all zeros
- For each input row, evaluates the child expression to get bit position
- Validates bit position is within valid range (0 to 8 * bitmap.length - 1)
- Sets the corresponding bit in the bitmap using bitwise OR operation
- Calculates byte position (bitPosition / 8) and bit offset (bitPosition % 8)
- Merges partial aggregates using bitwise OR operations

### Partitioning Behavior
- Requires shuffle for global aggregation across partitions
- Partial aggregation can occur within partitions
- Final merge combines bitmaps from all partitions using OR operations

### Edge Cases
- Ignores null input values (skips processing)
- Throws `QueryExecutionErrors.invalidBitmapPositionError` for out-of-range positions
- Returns bitmap with all zeros if no valid inputs provided
- Non-nullable return type - always returns a bitmap
- Duplicate positions are handled naturally (setting same bit multiple times)

### Code Generation
Implements `ImperativeAggregate` - uses interpreted mode for complex bitmap manipulation logic rather than code generation.

### Examples
```sql
-- Basic usage
SELECT hex(bitmap_construct_agg(bitmap_bit_position(col))) 
FROM VALUES (1), (2), (3) AS tab(col);

-- Result shows bitmap with bits 0, 1, 2 set
SELECT substring(hex(bitmap_construct_agg(bitmap_bit_position(col))), 1, 6) 
FROM VALUES (1), (2), (3) AS tab(col);  -- Returns '070000'

-- Duplicate values
SELECT substring(hex(bitmap_construct_agg(bitmap_bit_position(col))), 1, 6) 
FROM VALUES (1), (1), (1) AS tab(col);  -- Returns '010000'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.groupBy("category")
  .agg(expr("bitmap_construct_agg(bitmap_bit_position(id))").alias("bitmap"))
```

### See Also
- `bitmap_bit_position()` - Typically used as input to this function
- `bitmap_count()` - Count bits in the resulting bitmap
- `bitmap_or_agg()` - Aggregate existing bitmaps

---

## BitmapOrAgg

### Overview
BitmapOrAgg performs bitwise OR aggregation on multiple bitmaps, combining them into a single bitmap where each bit position is set if it was set in any of the input bitmaps. This is used to union multiple bitmap sets.

### Syntax
```sql
bitmap_or_agg(child)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BINARY | The bitmap data to aggregate using bitwise OR |

### Return Type
`BINARY` - Returns a fixed-size binary bitmap.

### Supported Data Types
- Input: `BinaryType` only - no implicit casting available
- Strict type checking enforced at analysis time

### Algorithm
- Initializes aggregation buffer with all zeros
- For each input bitmap, performs bitwise OR merge with current buffer
- Uses `BitmapExpressionUtils.bitmapMerge()` for efficient byte-wise OR operations
- Merges partial aggregates from different partitions using same OR logic
- Validates input type during analysis phase

### Partitioning Behavior
- Requires shuffle for global aggregation across partitions
- Partial aggregation can occur within partitions using OR operations
- Final merge combines bitmaps from all partitions preserving all set bits

### Edge Cases
- Ignores null input values (skips processing)
- Returns bitmap with all zeros if no valid inputs provided
- Strict type checking - throws `DataTypeMismatch` error for non-binary inputs
- Non-nullable return type - always returns a bitmap
- Handles bitmaps of fixed size as defined by `BitmapExpressionUtils.NUM_BYTES`

### Code Generation
Implements `ImperativeAggregate` - uses interpreted mode for complex bitmap manipulation rather than code generation.

### Examples
```sql
-- Combine multiple bitmaps using OR
SELECT hex(bitmap_or_agg(col)) 
FROM VALUES (X'10'), (X'20'), (X'40') AS tab(col);  -- Returns '700000...'

-- Duplicate bitmaps
SELECT substring(hex(bitmap_or_agg(col)), 1, 6) 
FROM VALUES (X'10'), (X'10'), (X'10') AS tab(col);  -- Returns '100000'

-- Typical usage with constructed bitmaps
SELECT bitmap_or_agg(bitmap_construct_agg(bitmap_bit_position(id))) 
FROM grouped_table GROUP BY category;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.groupBy("partition_key")
  .agg(expr("bitmap_or_agg(bitmap_column)").alias("combined_bitmap"))
```

### See Also
- `bitmap_construct_agg()` - Creates bitmaps for OR aggregation
- `bitmap_and_agg()` - Alternative aggregation using AND operation
- `bitmap_count()` - Count bits in resulting bitmap

---

## BitmapAndAgg

### Overview
BitmapAndAgg performs bitwise AND aggregation on multiple bitmaps, creating a bitmap where each bit position is set only if it was set in ALL of the input bitmaps. This operation finds the intersection of multiple bitmap sets.

### Syntax
```sql
bitmap_and_agg(child)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BINARY | The bitmap data to aggregate using bitwise AND |

### Return Type
`BINARY` - Returns a fixed-size binary bitmap.

### Supported Data Types
- Input: `BinaryType` only - no implicit casting available
- Strict type checking enforced at analysis time

### Algorithm
- Initializes aggregation buffer with all bits set to 1 (all bytes = -1/0xFF)
- For each input bitmap, performs bitwise AND merge with current buffer
- Uses `BitmapExpressionUtils.bitmapAndMerge()` for efficient byte-wise AND operations
- Merges partial aggregates from different partitions using same AND logic
- Validates input type during analysis phase

### Partitioning Behavior
- Requires shuffle for global aggregation across partitions
- Partial aggregation can occur within partitions using AND operations
- Final merge combines bitmaps from all partitions preserving only commonly set bits

### Edge Cases
- Ignores null input values (skips processing)
- Returns bitmap with all bits set (0xFF bytes) if no valid inputs provided
- Strict type checking - throws `DataTypeMismatch` error for non-binary inputs
- Non-nullable return type - always returns a bitmap
- Handles bitmaps of fixed size as defined by `BitmapExpressionUtils.NUM_BYTES`
- Different initialization from OR agg (starts with all 1s instead of all 0s)

### Code Generation
Implements `ImperativeAggregate` - uses interpreted mode for complex bitmap manipulation rather than code generation.

### Examples
```sql
-- Find intersection of multiple bitmaps using AND
SELECT hex(bitmap_and_agg(col)) 
FROM VALUES (X'F0'), (X'70'), (X'30') AS tab(col);  -- Returns '300000...'

-- All same bitmaps
SELECT substring(hex(bitmap_and_agg(col)), 1, 6) 
FROM VALUES (X'FF'), (X'FF'), (X'FF') AS tab(col);  -- Returns 'FF0000'

-- Intersection of constructed bitmaps
SELECT bitmap_and_agg(bitmap_construct_agg(bitmap_bit_position(id))) 
FROM grouped_table GROUP BY category;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.groupBy("partition_key")
  .agg(expr("bitmap_and_agg(bitmap_column)").alias("intersect_bitmap"))
```

### See Also
- `bitmap_or_agg()` - Alternative aggregation using OR operation  
- `bitmap_construct_agg()` - Creates bitmaps for AND aggregation
- `bitmap_count()` - Count bits in resulting intersection bitmap