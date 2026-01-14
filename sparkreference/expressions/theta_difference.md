# ThetaDifference

## Overview

`ThetaDifference` is a binary expression that computes the set difference (A - B) between two Theta sketches using Apache DataSketches library. It returns a new Theta sketch containing elements that exist in the first sketch but not in the second sketch, enabling efficient approximate set operations on large datasets.

## Syntax

```sql
theta_difference(sketch1, sketch2)
```

```scala
// DataFrame API
df.select(expr("theta_difference(sketch_col1, sketch_col2)"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| first | BinaryType | The first Theta sketch as a byte array (minuend) |
| second | BinaryType | The second Theta sketch as a byte array (subtrahend) |

## Return Type

`BinaryType` - Returns a compressed byte array representation of the resulting Theta sketch containing the set difference.

## Supported Data Types

- **Input**: `BinaryType` only - both arguments must be valid Theta sketch byte arrays
- **Output**: `BinaryType` - compressed Theta sketch byte array

## Algorithm

- Wraps input byte arrays into CompactSketch objects using `ThetaSketchUtils.wrapCompactSketch()`
- Creates a SetOperation builder and configures it for A-NOT-B (difference) operation
- Executes `aNotB(sketch1, sketch2)` to compute elements in sketch1 but not in sketch2
- Compresses and returns the result as a byte array using `toByteArrayCompressed()`
- Uses Apache DataSketches library's optimized set difference algorithms for probabilistic data structures

## Partitioning Behavior

- **Preserves partitioning**: No - this is a binary expression that operates on individual rows
- **Shuffle requirements**: No shuffle required - operates locally on co-located sketch data
- **Partitioning impact**: Neutral - does not affect downstream partitioning schemes

## Edge Cases

- **Null handling**: `nullIntolerant = true` - returns null if either input sketch is null
- **Invalid sketch data**: Throws exception if byte arrays cannot be deserialized as valid Theta sketches
- **Empty sketches**: Handles empty sketches gracefully - difference with empty sketch returns original sketch
- **Memory constraints**: Large sketches may cause memory pressure during operation
- **Sketch compatibility**: Requires compatible Theta sketch formats from the same DataSketches version

## Code Generation

This expression uses **CodegenFallback**, meaning it does not support Tungsten code generation and falls back to interpreted mode for evaluation. The complex nature of Theta sketch operations and external library dependencies make code generation impractical.

## Examples

```sql
-- Calculate difference between user activity sketches for two time periods
SELECT theta_difference(
    theta_sketch_agg(user_id) FILTER (WHERE date_range = 'current'),
    theta_sketch_agg(user_id) FILTER (WHERE date_range = 'previous')
) as user_churn_sketch
FROM user_activities;

-- Find elements unique to the first dataset
SELECT theta_difference(sketch_a, sketch_b) as unique_elements
FROM sketch_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Compute sketch difference
df.select(expr("theta_difference(sketch_col1, sketch_col2)").as("diff_sketch"))

// Chain with other sketch operations
df.select(
  expr("theta_sketch_estimate(theta_difference(sketch_a, sketch_b))").as("unique_count")
)
```

## See Also

- `theta_sketch_agg` - For creating Theta sketches from data
- `theta_union` - For computing union of Theta sketches  
- `theta_intersection` - For computing intersection of Theta sketches
- `theta_sketch_estimate` - For extracting cardinality estimates from Theta sketches