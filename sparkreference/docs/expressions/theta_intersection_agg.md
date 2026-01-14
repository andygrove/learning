# ThetaIntersectionAgg

## Overview
ThetaIntersectionAgg is a typed imperative aggregate expression that computes the intersection of Theta sketches. It takes binary-encoded Theta sketches as input and produces a single intersected Theta sketch, useful for approximate set intersection operations on large datasets.

## Syntax
```sql
SELECT theta_intersection_agg(sketch_column) FROM table
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that evaluates to binary-encoded Theta sketches |

## Return Type
`BinaryType` - Returns a binary-encoded compact Theta sketch representing the intersection of all input sketches.

## Supported Data Types

- Input: `BinaryType` only (binary-encoded Theta sketches)

- Output: `BinaryType` (compact Theta sketch)

## Algorithm

- Creates an Intersection instance using SetOperation.builder for aggregation buffer

- For each input sketch, deserializes the binary data into a Compact sketch using ThetaSketchUtils

- Calls intersect() method on the Intersection buffer with each input sketch

- During merge operations, handles both Intersection-to-Intersection and Intersection-to-Sketch merging

- Finalizes by converting the Intersection result into a compact binary sketch

## Partitioning Behavior
How this expression affects partitioning:

- Requires shuffle operations as it's an aggregate function that needs to combine data across partitions

- Does not preserve input partitioning since aggregation consolidates multiple input rows

- Uses mutableAggBufferOffset and inputAggBufferOffset for distributed aggregation coordination

## Edge Cases

- Null input values are ignored and don't affect the intersection result

- Empty buffer during deserialization creates a new aggregation buffer instead of failing

- Non-BinaryType inputs throw QueryExecutionErrors.thetaInvalidInputSketchBuffer

- Invalid sketch buffer states during merge operations throw QueryExecutionErrors.thetaInvalidInputSketchBuffer

- Returns non-nullable result (nullable = false)

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode, as it extends TypedImperativeAggregate which requires custom aggregation buffer management and complex sketch intersection logic.

## Examples
```sql
-- Aggregate Theta sketches to find intersection
SELECT theta_intersection_agg(user_sketch) 
FROM user_activity_sketches 
GROUP BY campaign_id;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.groupBy("campaign_id")
  .agg(expr("theta_intersection_agg(user_sketch)").as("intersected_users"))
```

## See Also

- ThetaUnionAgg - For computing unions of Theta sketches

- ThetaSketchUtils - Utility functions for Theta sketch operations

- SetOperation - Apache DataSketches library for set operations