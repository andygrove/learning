# EWM

## Overview

EWM (Exponentially Weighted Moving average) is a Spark Catalyst window expression that computes weighted moving averages over a window of data. Currently, only weighted moving average is supported, providing a way to calculate time-series smoothing with exponential decay weights.

## Syntax

```scala
EWM(input: Expression, alpha: Double, ignoreNA: Boolean)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `input` | Expression | The input expression containing numeric values to compute the weighted moving average over |
| `alpha` | Double | The smoothing factor that determines the rate of exponential decay for weights |
| `ignoreNA` | Boolean | Flag indicating whether to ignore null/NA values in the computation |

## Return Type

Returns a numeric data type (typically Double) representing the exponentially weighted moving average.

## Supported Data Types

- Numeric types (Integer, Long, Float, Double, Decimal)
- Input expression must evaluate to numeric values for meaningful computation

## Algorithm

- Implements weighted moving average using the formula: `y_t = (Σ(w_i * x_{t-i})) / (Σ w_i)` where i ranges from 0 to t
- Uses exponential weighting scheme where weights decay exponentially based on the alpha parameter
- Processes input values sequentially within the window frame
- Accumulates weighted sums in both numerator and denominator
- Handles null value exclusion based on the `ignoreNA` parameter

## Partitioning Behavior

- Preserves input partitioning as this is a window function that operates within partitions
- Does not require shuffle if used with proper window specification
- Computation is performed locally within each partition's window frames
- Requires proper ordering within the window specification for meaningful results

## Edge Cases

- **Null handling**: Behavior depends on `ignoreNA` parameter - nulls are either skipped or propagated
- **Empty input**: Returns null when no valid input values are present in the window
- **Single value**: Returns the input value itself when only one value exists in the window  
- **Alpha bounds**: Alpha parameter should typically be between 0 and 1 for standard exponential weighting
- **Numeric overflow**: May experience precision issues with very large numeric values or extreme alpha values

## Code Generation

This expression likely supports Spark's Tungsten code generation framework for optimized execution, though the specific implementation would depend on the complexity of the weighted average computation and null handling logic.

## Examples

```sql
-- Example SQL usage (hypothetical, as EWM may not have direct SQL syntax)
SELECT value, 
       EWM(value, 0.3, true) OVER (ORDER BY timestamp ROWS UNBOUNDED PRECEDING) as ewm_avg
FROM time_series_data
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val windowSpec = Window.orderBy("timestamp").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df.withColumn("ewm_avg", new Column(EWM(col("value").expr, 0.3, true)).over(windowSpec))
```

## See Also

- Window functions and expressions
- Moving average aggregation functions
- Time series analysis expressions
- Statistical window functions