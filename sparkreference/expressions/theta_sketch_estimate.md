# ThetaSketch Expressions Reference

## ThetaSketchEstimate

### Overview
The `theta_sketch_estimate` expression returns the estimated number of unique values from a binary representation of a DataSketches ThetaSketch. It provides probabilistic cardinality estimation by decoding a compressed theta sketch and returning a rounded estimate of distinct elements.

### Syntax
```sql
theta_sketch_estimate(sketch_binary)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch_binary | BinaryType | Binary representation of a DataSketches ThetaSketch object |

### Return Type
`LongType` - Returns the estimated cardinality as a long integer.

### Supported Data Types
- Input: `BinaryType` only (serialized ThetaSketch)
- Output: `LongType`

### Algorithm
- Deserializes the input binary array into a ThetaSketch compact sketch object
- Calls the sketch's `getEstimate()` method to retrieve the probabilistic cardinality estimate
- Rounds the floating-point estimate to the nearest long integer using `Math.round()`
- Returns the rounded estimate as the final cardinality count

### Partitioning Behavior
- Preserves partitioning as it's a deterministic unary transformation
- No shuffle required - operates independently on each partition
- Can be applied after sketch aggregation operations

### Edge Cases
- **Null handling**: Null intolerant - returns null if input sketch is null
- **Invalid binary data**: Throws exception if binary data cannot be deserialized as a valid ThetaSketch
- **Empty sketch**: Returns 0 for sketches with no recorded elements
- **Estimation accuracy**: Accuracy depends on the original sketch configuration and data distribution

### Code Generation
Uses `CodegenFallback` - falls back to interpreted mode rather than generating Tungsten bytecode.

### Examples
```sql
-- Estimate unique values from aggregated sketch
SELECT theta_sketch_estimate(theta_sketch_agg(col)) 
FROM VALUES (1), (1), (2), (2), (3) AS tab(col);
-- Result: 3
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("theta_sketch_estimate(sketch_column)"))
```

---

## ThetaUnion

### Overview
The `theta_union` expression merges two binary representations of DataSketches ThetaSketch objects using a ThetaSketch Union operation. It creates a unified sketch containing the union of distinct elements from both input sketches with configurable buffer size.

### Syntax
```sql
theta_union(sketch1, sketch2 [, lgNomEntries])
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch1 | BinaryType | First binary ThetaSketch representation |
| sketch2 | BinaryType | Second binary ThetaSketch representation |
| lgNomEntries | IntegerType | Log base-2 of nominal entries (4-26, defaults to 12) |

### Return Type
`BinaryType` - Returns a compressed binary representation of the union sketch.

### Supported Data Types
- Input: Two `BinaryType` sketches and optional `IntegerType` for buffer size
- Output: `BinaryType` (compressed union sketch)

### Algorithm
- Validates the lgNomEntries parameter is within acceptable range (4-26)
- Deserializes both input binary arrays into ThetaSketch compact sketch objects
- Creates a SetOperation Union builder with specified log nominal entries
- Performs union operation on both sketches using DataSketches library
- Returns compressed binary representation of the resulting union sketch

### Partitioning Behavior
- Does not preserve partitioning inherently (combines data from multiple sketches)
- Typically used after sketch aggregation, may require shuffle depending on query pattern
- Output can be further aggregated across partitions

### Edge Cases
- **Null handling**: Null intolerant - returns null if any input sketch is null
- **Invalid lgNomEntries**: Throws exception if lgNomEntries is outside 4-26 range
- **Mismatched sketch parameters**: May produce suboptimal results if input sketches have different configurations
- **Empty sketches**: Handles empty sketches gracefully, union with empty sketch returns the non-empty sketch

### Code Generation
Uses `CodegenFallback` - falls back to interpreted mode rather than generating Tungsten bytecode.

### Examples
```sql
-- Union two sketch aggregations
SELECT theta_sketch_estimate(theta_union(theta_sketch_agg(col1), theta_sketch_agg(col2))) 
FROM VALUES (1, 4), (1, 4), (2, 5), (2, 5), (3, 6) AS tab(col1, col2);
-- Result: 6

-- Union with custom buffer size
SELECT theta_union(sketch1, sketch2, 16) FROM sketch_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("theta_union(sketch_col1, sketch_col2, 14)"))
```

---

## ThetaDifference

### Overview
The `theta_difference` expression computes the set difference between two binary representations of DataSketches ThetaSketch objects using a ThetaSketch AnotB operation. It returns a sketch containing elements present in the first sketch but not in the second sketch.

### Syntax
```sql
theta_difference(sketch1, sketch2)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch1 | BinaryType | First binary ThetaSketch representation (minuend) |
| sketch2 | BinaryType | Second binary ThetaSketch representation (subtrahend) |

### Return Type
`BinaryType` - Returns a compressed binary representation of the difference sketch.

### Supported Data Types
- Input: Two `BinaryType` sketches
- Output: `BinaryType` (compressed difference sketch)

### Algorithm
- Deserializes both input binary arrays into ThetaSketch compact sketch objects
- Creates a SetOperation AnotB builder for set difference computation
- Performs A-not-B operation (elements in sketch1 but not in sketch2)
- Returns compressed binary representation of the resulting difference sketch

### Partitioning Behavior
- Does not preserve partitioning (combines data from multiple sketches)
- Non-commutative operation - order of arguments matters
- May require shuffle depending on how sketches are distributed across partitions

### Edge Cases
- **Null handling**: Null intolerant - returns null if either input sketch is null
- **Empty sketches**: Returns empty sketch if first sketch is empty; returns first sketch if second sketch is empty
- **Identical sketches**: Returns empty sketch when subtracting identical sketches
- **Order sensitivity**: `theta_difference(A, B)` ≠ `theta_difference(B, A)`

### Code Generation
Uses `CodegenFallback` - falls back to interpreted mode rather than generating Tungsten bytecode.

### Examples
```sql
-- Find elements in col1 sketches but not in col2 sketches
SELECT theta_sketch_estimate(theta_difference(theta_sketch_agg(col1), theta_sketch_agg(col2))) 
FROM VALUES (5, 4), (1, 4), (2, 5), (2, 5), (3, 1) AS tab(col1, col2);
-- Result: 2
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("theta_difference(sketch_col1, sketch_col2)"))
```

---

## ThetaIntersection

### Overview
The `theta_intersection` expression computes the set intersection between two binary representations of DataSketches ThetaSketch objects using a ThetaSketch Intersect operation. It returns a sketch containing only elements present in both input sketches.

### Syntax
```sql
theta_intersection(sketch1, sketch2)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch1 | BinaryType | First binary ThetaSketch representation |
| sketch2 | BinaryType | Second binary ThetaSketch representation |

### Return Type
`BinaryType` - Returns a compressed binary representation of the intersection sketch.

### Supported Data Types
- Input: Two `BinaryType` sketches
- Output: `BinaryType` (compressed intersection sketch)

### Algorithm
- Deserializes both input binary arrays into ThetaSketch compact sketch objects
- Creates a SetOperation Intersection builder for set intersection computation
- Performs intersection operation to find common elements between both sketches
- Returns compressed binary representation of the resulting intersection sketch

### Partitioning Behavior
- Does not preserve partitioning (combines data from multiple sketches)
- Commutative operation - order of arguments doesn't affect result
- May require shuffle depending on how sketches are distributed across partitions

### Edge Cases
- **Null handling**: Null intolerant - returns null if either input sketch is null
- **Empty sketches**: Returns empty sketch if either input sketch is empty
- **Disjoint sketches**: Returns empty sketch when sketches share no common elements
- **Identical sketches**: Returns equivalent sketch when intersecting identical sketches

### Code Generation
Uses `CodegenFallback` - falls back to interpreted mode rather than generating Tungsten bytecode.

### Examples
```sql
-- Find common elements between col1 and col2 sketches
SELECT theta_sketch_estimate(theta_intersection(theta_sketch_agg(col1), theta_sketch_agg(col2))) 
FROM VALUES (5, 4), (1, 4), (2, 5), (2, 5), (3, 1) AS tab(col1, col2);
-- Result: 2
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("theta_intersection(sketch_col1, sketch_col2)"))
```

## See Also
- `theta_sketch_agg` - Aggregation function for creating ThetaSketch objects
- DataSketches library documentation for underlying algorithm details
- Spark SQL aggregate functions for cardinality estimation