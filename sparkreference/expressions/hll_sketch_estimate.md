# DataSketches HLL Expressions Reference

## HllSketchEstimate

### Overview
The `HllSketchEstimate` expression extracts the estimated cardinality (number of unique values) from a binary representation of a DataSketches HyperLogLog (HLL) sketch. This expression is typically used to get the final count estimate from an HLL sketch that was previously aggregated using `hll_sketch_agg`.

### Syntax
```sql
hll_sketch_estimate(sketch_binary)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch_binary | BinaryType | Binary representation of a DataSketches HllSketch object |

### Return Type
`LongType` - Returns the estimated cardinality as a long integer, rounded to the nearest whole number.

### Supported Data Types
- Input: `BinaryType` only (must be a valid HllSketch binary representation)
- Output: `LongType`

### Algorithm
- Deserializes the input binary data into an HllSketch object using `HllSketch.heapify()`
- Calls `getEstimate()` on the deserialized sketch to get the cardinality estimate
- Rounds the estimate to the nearest long integer using `Math.round()`
- Throws an exception if the binary data is not a valid HllSketch representation

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation on individual rows
- Does not require shuffle operations
- Can be applied partition-locally

### Edge Cases
- **Null handling**: Expression is null-intolerant, meaning null inputs will result in null output
- **Invalid binary data**: Throws `QueryExecutionErrors.hllInvalidInputSketchBuffer` for malformed sketch data
- **Empty sketches**: Returns 0 for sketches with no data
- **Memory errors**: Catches both `SketchesArgumentException` and `java.lang.Error` during deserialization

### Code Generation
Uses `CodegenFallback` - this expression falls back to interpreted mode and does not generate optimized bytecode.

### Examples
```sql
-- Get estimated unique count from aggregated sketch
SELECT hll_sketch_estimate(hll_sketch_agg(user_id)) 
FROM user_events;

-- Combined with grouping
SELECT region, hll_sketch_estimate(hll_sketch_agg(user_id)) as unique_users
FROM user_events 
GROUP BY region;
```

```scala
// DataFrame API usage
df.select(expr("hll_sketch_estimate(sketch_column)"))

// With aggregation
df.groupBy("category")
  .agg(expr("hll_sketch_estimate(hll_sketch_agg(user_id))").alias("unique_users"))
```

---

## HllUnion

### Overview
The `HllUnion` expression merges two binary representations of DataSketches HLL sketches using a DataSketches Union object. This allows combining cardinality estimates from different sketches while maintaining approximation accuracy. The expression supports an optional parameter to control whether sketches with different precision parameters can be merged.

### Syntax
```sql
hll_union(first_sketch, second_sketch [, allowDifferentLgConfigK])
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| first_sketch | BinaryType | Binary representation of the first HllSketch object |
| second_sketch | BinaryType | Binary representation of the second HllSketch object |
| allowDifferentLgConfigK | BooleanType | Optional. Whether to allow union of sketches with different lgConfigK values (defaults to false) |

### Return Type
`BinaryType` - Returns a binary representation of the merged HLL sketch.

### Supported Data Types
- Input: Two `BinaryType` parameters (HLL sketches) and one optional `BooleanType` parameter
- Output: `BinaryType` (merged HLL sketch)

### Algorithm
- Deserializes both input binary arrays into HllSketch objects using `HllSketch.heapify()`
- Validates lgConfigK compatibility if `allowDifferentLgConfigK` is false
- Creates a Union object with the minimum lgConfigK from both sketches
- Updates the union with both sketches sequentially
- Returns the union result as a binary array using HLL_8 target type

### Partitioning Behavior
- Preserves partitioning as it operates on individual rows
- Does not require shuffle operations
- Commonly used after shuffle phases where sketches from different partitions need merging

### Edge Cases
- **Null handling**: Expression is null-intolerant, null inputs result in null output
- **Invalid binary data**: Throws `QueryExecutionErrors.hllInvalidInputSketchBuffer` for either malformed sketch
- **lgConfigK mismatch**: Throws `QueryExecutionErrors.hllUnionDifferentLgK` when sketches have different precision and `allowDifferentLgConfigK` is false
- **Memory errors**: Catches both `SketchesArgumentException` and `java.lang.Error` during deserialization
- **Different precisions**: When allowed, uses the minimum lgConfigK value for the union result

### Code Generation
Uses `CodegenFallback` - this expression falls back to interpreted mode and does not generate optimized bytecode.

### Examples
```sql
-- Basic union of two sketches
SELECT hll_sketch_estimate(
  hll_union(sketch1, sketch2)
) FROM sketch_table;

-- Union with different lgConfigK allowed
SELECT hll_union(sketch_col1, sketch_col2, true) 
FROM combined_sketches;

-- Complex example: union sketches from different groups
SELECT hll_sketch_estimate(
  hll_union(
    hll_sketch_agg(col1), 
    hll_sketch_agg(col2)
  )
) as total_unique
FROM VALUES (1, 4), (1, 4), (2, 5), (2, 5), (3, 6) tab(col1, col2);
```

```scala
// DataFrame API usage
df.select(expr("hll_union(sketch1, sketch2)"))

// With allowDifferentLgConfigK parameter
df.select(expr("hll_union(sketch1, sketch2, true)"))

// Chaining operations
df.select(
  expr("hll_sketch_estimate(hll_union(sketch_a, sketch_b))").alias("merged_estimate")
)
```

### See Also
- `hll_sketch_estimate` - Extract cardinality estimates from HLL sketches
- `hll_sketch_agg` - Aggregate function to create HLL sketches from column data
- DataSketches HLL documentation for lgConfigK parameter tuning