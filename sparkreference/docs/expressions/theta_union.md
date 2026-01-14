# ThetaUnion

## Overview
The `ThetaUnion` expression computes the union of two Theta sketches, which are probabilistic data structures used for cardinality estimation. This function combines two distinct sketch representations into a single unified sketch that represents the approximate union of the underlying datasets.

## Syntax
```sql
theta_union(sketch1, sketch2)
theta_union(sketch1, sketch2, log_nominal_entries)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `sketch1` | Binary | First Theta sketch as a byte array |
| `sketch2` | Binary | Second Theta sketch as a byte array |
| `log_nominal_entries` | Integer | Optional. Log base-2 of the nominal number of entries for the resulting sketch. Defaults to `ThetaSketchUtils.DEFAULT_LG_NOM_LONGS` |

## Return Type
`Binary` - Returns a compressed byte array representation of the unified Theta sketch.

## Supported Data Types
- **Input**: Binary type for sketch parameters, Integer type for log nominal entries
- **Output**: Binary type (compressed Theta sketch)

## Algorithm
- Validates the `log_nominal_entries` parameter using `ThetaSketchUtils.checkLgNomLongs`
- Wraps the input byte arrays as CompactSketch objects using `ThetaSketchUtils.wrapCompactSketch`
- Creates a SetOperation Union builder with the specified log nominal entries configuration
- Performs the union operation on both sketches using the Apache DataSketches library
- Compresses and returns the resulting sketch as a byte array

## Partitioning Behavior
- **Preserves partitioning**: No, this is a transformation that combines data from multiple sketches
- **Requires shuffle**: Depends on the data distribution; if sketches to be unioned are in different partitions, a shuffle may be required

## Edge Cases
- **Null handling**: Expression is null-intolerant (`nullIntolerant = true`), meaning it returns null if any input is null
- **Invalid sketches**: Throws exception if input byte arrays cannot be wrapped as valid CompactSketch objects
- **Invalid log nominal entries**: Validates the `log_nominal_entries` parameter and throws exception if out of valid range
- **Empty sketches**: Handles empty sketches gracefully through the underlying DataSketches library

## Code Generation
This expression uses **CodegenFallback**, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode for all operations.

## Examples
```sql
-- Union two theta sketches with default configuration
SELECT theta_union(sketch_col1, sketch_col2) FROM sketches_table;

-- Union two theta sketches with custom log nominal entries
SELECT theta_union(sketch_col1, sketch_col2, 12) FROM sketches_table;
```

```scala
// DataFrame API usage with default parameters
df.select(expr("theta_union(sketch1, sketch2)"))

// DataFrame API usage with custom log nominal entries  
df.select(expr("theta_union(sketch1, sketch2, 10)"))

// Using constructor overloads in expression building
val union1 = ThetaUnion(sketch1Expr, sketch2Expr)
val union2 = ThetaUnion(sketch1Expr, sketch2Expr, Literal(8))
```

## See Also
- Other Theta sketch expressions for cardinality estimation
- `SetOperation.builder` from Apache DataSketches library
- `ThetaSketchUtils` utility functions for sketch validation and wrapping