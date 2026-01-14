# ThetaIntersection

## Overview
The `ThetaIntersection` expression computes the intersection of two Theta sketches, returning a new Theta sketch containing the elements that appear in both input sketches. This is commonly used for approximate set intersection operations on large datasets where exact computation would be prohibitively expensive.

## Syntax
```sql
theta_intersection(sketch1, sketch2)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("theta_intersection(sketch_col1, sketch_col2)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| first | BinaryType | First Theta sketch as a byte array |
| second | BinaryType | Second Theta sketch as a byte array |

## Return Type
`BinaryType` - Returns a compressed byte array representation of the intersected Theta sketch.

## Supported Data Types
- **Input**: `BinaryType` only - expects serialized Theta sketch byte arrays
- **Output**: `BinaryType` - compressed Theta sketch byte array

## Algorithm
- Wraps input byte arrays into CompactSketch objects using `ThetaSketchUtils.wrapCompactSketch`
- Creates a SetOperation intersection builder from the Theta Sketches library
- Performs intersection operation on the two sketches using `intersect(sketch1, sketch2)`
- Serializes the result to a compressed byte array format using `toByteArrayCompressed`
- Leverages probabilistic data structures for approximate but memory-efficient set operations

## Partitioning Behavior
- **Preserves partitioning**: No, this is a binary expression that operates on two sketches
- **Requires shuffle**: Depends on the distribution of input sketches across partitions
- **Partitioning impact**: Does not inherently change partitioning scheme but may require data movement if sketches to be intersected are on different partitions

## Edge Cases
- **Null handling**: `nullIntolerant = true` means if either input is null, the result is null
- **Invalid sketch data**: If input byte arrays are not valid Theta sketches, `ThetaSketchUtils.wrapCompactSketch` will handle the error
- **Empty sketches**: Intersection of empty sketches results in an empty sketch
- **Mismatched sketch parameters**: The underlying Theta Sketches library handles compatibility between sketches with different configurations

## Code Generation
This expression uses `CodegenFallback`, meaning it **does not support** Tungsten code generation and falls back to interpreted evaluation mode. All computation happens through the `nullSafeEval` method at runtime.

## Examples
```sql
-- Intersect two Theta sketches to find common elements
SELECT theta_intersection(user_sketch, product_sketch) as common_sketch
FROM analytics_table;

-- Use with other Theta sketch functions
SELECT theta_sketch_estimate(theta_intersection(sketch_a, sketch_b)) as intersection_size
FROM sketch_data;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.table("sketch_table")
val result = df.select(
  expr("theta_intersection(sketch_column1, sketch_column2)").alias("intersected_sketch")
)

// Chain with other operations
val estimatedSize = df.select(
  expr("theta_sketch_estimate(theta_intersection(sketch_a, sketch_b))").alias("intersection_count")
)
```

## See Also
- `ThetaUnion` - Union operation for Theta sketches
- `ThetaSketchEstimate` - Extract cardinality estimates from Theta sketches  
- `ThetaSketchBuild` - Create Theta sketches from raw data
- Apache DataSketches Theta Sketch documentation for underlying algorithm details