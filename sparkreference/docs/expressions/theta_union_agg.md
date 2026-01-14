# ThetaUnionAgg

## Overview
ThetaUnionAgg is a Spark SQL aggregate function that unions multiple Theta sketches to produce a single merged sketch. It uses the Apache DataSketches library to perform efficient set union operations on probabilistic data structures, enabling approximate distinct count and set operations on large datasets.

## Syntax
```sql
theta_union_agg(sketch_column [, lg_nom_entries])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch_column | BinaryType | Input column containing Theta sketch data as byte arrays |
| lg_nom_entries | IntegerType | Optional. Log base-2 of nominal entries for the Union buffer (default: from ThetaSketchUtils.DEFAULT_LG_NOM_LONGS) |

## Return Type
BinaryType - Returns a compact Theta sketch as a byte array.

## Supported Data Types

- **Input sketch data**: BinaryType only (compact Theta sketch byte arrays)
- **Configuration parameter**: IntegerType for lg_nom_entries

## Algorithm

- Creates a Union aggregation buffer with specified nominal entries capacity
- Processes each input sketch by wrapping the byte array into a CompactSketch instance
- Updates the Union buffer by calling union() on each input sketch
- Merges partial aggregation results by combining Union objects or integrating finalized sketches
- Serializes the final Union result into a compact binary sketch format

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve input partitioning as it performs aggregation across partitions
- Requires shuffle operation for global aggregation across all partitions during the merge phase
- Uses TypedImperativeAggregate framework for distributed aggregation with custom serialization

## Edge Cases

- **Null handling**: Null input values are ignored and do not affect the aggregation result
- **Empty input**: Returns an empty Union buffer when no valid sketches are processed
- **Invalid sketch format**: Throws QueryExecutionErrors.thetaInvalidInputSketchBuffer for non-binary input types
- **Non-constant lg_nom_entries**: Throws QueryExecutionErrors.thetaLgNomEntriesMustBeConstantError if the parameter is not foldable
- **Buffer type validation**: Validates buffer types during merge operations and throws errors for unexpected buffer states

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode. It extends TypedImperativeAggregate which uses custom update/merge/serialize/deserialize methods that cannot be code-generated.

## Examples
```sql
-- Basic usage with default configuration
SELECT theta_union_agg(sketch_column) FROM sketches_table;

-- With custom nominal entries parameter
SELECT theta_union_agg(sketch_column, 12) FROM sketches_table;

-- Group by aggregation
SELECT category, theta_union_agg(user_sketch, 14) 
FROM user_sketches 
GROUP BY category;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic aggregation
df.agg(expr("theta_union_agg(sketch_column)"))

// With custom lg_nom_entries
df.agg(expr("theta_union_agg(sketch_column, 12)"))

// Grouped aggregation
df.groupBy("category")
  .agg(expr("theta_union_agg(sketch_column, 14)").as("merged_sketch"))
```

## See Also

- ThetaSketchAgg - For creating individual Theta sketches from raw data
- Other DataSketches aggregation functions for HLL and quantiles sketches
- SetOperation.buildUnion() from Apache DataSketches library