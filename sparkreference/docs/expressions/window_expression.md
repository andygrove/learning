# WindowExpression

## Overview
The `WindowExpression` represents a window function expression that applies a window function over a specified window specification. It serves as a wrapper that combines a window function with its associated window specification (OVER clause), enabling the execution of analytical functions that operate on a sliding window of rows.

## Syntax
```sql
window_function OVER window_specification
```

```scala
// DataFrame API - window functions are typically created through functions like:
col("column_name").over(window_spec)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| windowFunction | Expression | The window function to be applied (e.g., ROW_NUMBER, SUM, AVG, etc.) |
| windowSpec | WindowSpecDefinition | The window specification defining partitioning, ordering, and frame boundaries |

## Return Type
The return type matches the data type of the underlying `windowFunction` expression. The actual type depends on the specific window function being used.

## Supported Data Types
Supports all data types that are supported by the underlying window function. The `WindowExpression` itself is type-agnostic and delegates type validation to the wrapped window function.

## Algorithm
- Acts as a container that combines a window function with its window specification
- Delegates data type determination to the underlying window function
- Preserves nullability characteristics of the wrapped window function  
- Implements `Unevaluable` trait, meaning evaluation is handled by specialized window execution operators
- Uses `BinaryLike` pattern treating window function as left child and window spec as right child

## Partitioning Behavior
Window expressions have significant partitioning implications:
- **Requires shuffle**: Window operations typically require data to be partitioned by the PARTITION BY columns
- **Does not preserve partitioning**: The output partitioning depends on the window specification's PARTITION BY clause
- **Triggers sort**: Most window functions require sorting within partitions based on ORDER BY clause

## Edge Cases
- **Null handling**: Inherits null handling behavior from the underlying window function
- **Empty partitions**: Window functions handle empty partitions according to their specific semantics
- **No frame specification**: Defaults to frame boundaries defined by the window specification
- **Invalid parameters**: Compilation errors are thrown for malformed window specifications during analysis phase

## Code Generation
The `WindowExpression` itself is marked as `Unevaluable`, meaning:
- **No direct code generation**: Does not participate in code generation as it's not directly evaluated
- **Execution delegation**: Actual execution is handled by specialized physical operators like `WindowExec`
- **Code generation support**: The underlying window function may support code generation depending on its implementation

## Examples
```sql
-- Ranking functions
SELECT ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

-- Aggregate functions as window functions  
SELECT SUM(salary) OVER (PARTITION BY department) as dept_total
FROM employees;

-- Moving averages
SELECT AVG(salary) OVER (ORDER BY hire_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
FROM employees;
```

```scala
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

// Ranking with window
val windowSpec = Window.partitionBy("department").orderBy(desc("salary"))
df.select(col("*"), row_number().over(windowSpec).alias("rank"))

// Running totals
val runningSpec = Window.partitionBy("department").orderBy("hire_date")
df.select(col("*"), sum("salary").over(runningSpec).alias("running_total"))
```

## See Also
- `WindowSpecDefinition` - Defines the window specification (OVER clause)
- `WindowFunction` - Base trait for window functions
- `RowNumber`, `Rank`, `DenseRank` - Ranking window functions  
- `Lead`, `Lag` - Offset window functions
- `WindowExec` - Physical operator for window expression execution