# Window Expressions Reference

## Overview

This module defines expressions used for window functions in Apache Spark SQL, including window frame specifications, offset window functions, and aggregate window functions. These expressions enable SQL window operations like `ROW_NUMBER()`, `LAG`, `LEAD`, and various ranking functions that operate over partitioned and ordered data sets.

---

# WindowSpecDefinition

## Overview

Defines a window specification that describes how input rows are partitioned, ordered, and framed for window function evaluation. This corresponds to the `OVER` clause in SQL window functions.

## Syntax

```sql
OVER (PARTITION BY expr1, expr2, ... ORDER BY expr3, expr4, ... frame_spec)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| partitionSpec | Seq[Expression] | Expressions that define how input rows are partitioned |
| orderSpec | Seq[SortOrder] | Expressions that define the ordering of rows within a partition |
| frameSpecification | WindowFrame | Defines the window frame boundaries within a partition |

## Return Type

This is not directly evaluable - it's a specification used by window expressions.

## Supported Data Types

- Partition expressions: Any comparable data types
- Order expressions: Any orderable data types  
- Frame specifications: Numeric types for row frames, numeric/interval types for range frames

## Algorithm

- Validates frame specification compatibility with order specification
- For range frames with value bounds, ensures single ordering column
- Validates data type compatibility between order column and frame boundary values
- Checks frame boundary logical consistency (e.g., no UNBOUNDED FOLLOWING as lower bound)

## Partitioning Behavior

- Defines partitioning scheme for window operations
- Requires shuffle if partitioning doesn't match current distribution
- Window functions execute within each partition independently

## Edge Cases

- Range frames require ORDER BY clause when using value bounds
- Range frames with value bounds limited to single ordering expression
- Frame boundary expressions must be foldable (constant)
- Invalid frame boundaries (e.g., upper < lower) cause analysis errors

## Code Generation

Not directly code-generated as it's a specification expression used during planning.

## Examples

```sql
-- Basic window with partitioning and ordering
SELECT emp_id, salary, 
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) as rank
FROM employees;

-- Window with custom frame
SELECT emp_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id ORDER BY salary 
                        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as avg_salary
FROM employees;
```

## See Also

SpecifiedWindowFrame, WindowExpression, WindowFunction

---

# Lead

## Overview

Returns the value of an input expression evaluated at a row that is a specified number of rows after the current row within the window partition. This is an offset window function that looks "forward" in the partition.

## Syntax

```sql
LEAD(input [, offset [, default]]) OVER (window_spec)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | Expression to evaluate at the offset row |
| offset | Expression | Number of rows after current row (default: 1, must be constant integer) |
| default | Expression | Value to return when offset row doesn't exist (default: null) |
| ignoreNulls | Boolean | Whether to skip null values when counting offset (default: false) |

## Return Type

Same as the input expression's data type.

## Supported Data Types

- Input: Any data type
- Offset: IntegerType only
- Default: Must be compatible with input data type

## Algorithm

- Creates a fake row frame with the specified offset for grouping similar offset functions
- During execution, looks forward by `offset` rows from current position
- Returns input value at target row, or default if target row doesn't exist
- If ignoreNulls=true, skips null input values when counting offset

## Partitioning Behavior

- Preserves partitioning from window specification
- No additional shuffle required beyond window operation
- Operates independently within each partition

## Edge Cases

- Null input values: returned as-is unless ignoreNulls=true
- Offset beyond partition boundary: returns default value
- Negative offset: treated as 0 (current row)
- Non-constant offset: causes analysis error

## Code Generation

Supports code generation through the window execution framework.

## Examples

```sql
-- Basic lead with default offset of 1
SELECT emp_id, salary, LEAD(salary) OVER (ORDER BY emp_id) as next_salary
FROM employees;

-- Lead with custom offset and default
SELECT emp_id, salary, 
       LEAD(salary, 2, 0) OVER (PARTITION BY dept_id ORDER BY salary) as salary_2_ahead
FROM employees;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val window = Window.partitionBy("dept_id").orderBy("salary")
df.select($"emp_id", $"salary", 
         lead($"salary", 2, 0).over(window).alias("salary_2_ahead"))
```

## See Also

Lag, NthValue, FrameLessOffsetWindowFunction

---

# Lag

## Overview

Returns the value of an input expression evaluated at a row that is a specified number of rows before the current row within the window partition. This is an offset window function that looks "backward" in the partition.

## Syntax

```sql
LAG(input [, offset [, default]]) OVER (window_spec)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | Expression to evaluate at the offset row |
| inputOffset | Expression | Number of rows before current row (default: 1, must be constant integer) |
| default | Expression | Value to return when offset row doesn't exist (default: null) |
| ignoreNulls | Boolean | Whether to skip null values when counting offset (default: false) |

## Return Type

Same as the input expression's data type.

## Supported Data Types

- Input: Any data type
- Offset: IntegerType only  
- Default: Must be compatible with input data type

## Algorithm

- Converts positive offset to negative via UnaryMinus for backward lookup
- Creates a fake row frame with the negative offset
- During execution, looks backward by `offset` rows from current position
- Returns input value at target row, or default if target row doesn't exist
- If ignoreNulls=true, skips null input values when counting offset

## Partitioning Behavior

- Preserves partitioning from window specification
- No additional shuffle required beyond window operation
- Operates independently within each partition

## Edge Cases

- Null input values: returned as-is unless ignoreNulls=true
- Offset beyond partition boundary: returns default value
- Negative offset: treated as 0 (current row)
- Non-constant offset: causes analysis error

## Code Generation

Supports code generation through the window execution framework.

## Examples

```sql
-- Basic lag with default offset of 1
SELECT emp_id, salary, LAG(salary) OVER (ORDER BY emp_id) as prev_salary
FROM employees;

-- Lag with custom offset and default
SELECT emp_id, salary,
       LAG(salary, 2, 0) OVER (PARTITION BY dept_id ORDER BY salary) as salary_2_behind
FROM employees;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val window = Window.partitionBy("dept_id").orderBy("salary")
df.select($"emp_id", $"salary", 
         lag($"salary", 2, 0).over(window).alias("salary_2_behind"))
```

## See Also

Lead, NthValue, FrameLessOffsetWindowFunction

---

# RowNumber

## Overview

Assigns a unique, sequential number to each row within a window partition, starting from 1, according to the ordering specified in the window's ORDER BY clause.

## Syntax

```sql
ROW_NUMBER() OVER (window_spec)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| (none) | - | No arguments required |

## Return Type

IntegerType (non-nullable)

## Supported Data Types

No input data types (leaf expression).

## Algorithm

- Maintains a counter (rowNumber) starting at 0
- Initializes buffer with zero value  
- For each row, increments counter by 1
- Returns current counter value as the row number
- Uses RowFrame from UnboundedPreceding to CurrentRow

## Partitioning Behavior

- Preserves partitioning from window specification
- Resets row numbering within each partition
- Requires window execution which may trigger shuffle

## Edge Cases

- Always returns non-null integer values
- Row numbers start at 1 for first row in each partition
- Tied values (same ORDER BY values) get different row numbers
- Empty partitions produce no results

## Code Generation

Supports code generation as part of aggregate window function framework.

## Examples

```sql
-- Basic row numbering
SELECT emp_id, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- Row numbering within partitions  
SELECT emp_id, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) as dept_rank
FROM employees;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val window = Window.partitionBy("dept_id").orderBy(desc("salary"))
df.select($"emp_id", $"dept_id", $"salary",
         row_number().over(window).alias("dept_rank"))
```

## See Also

Rank, DenseRank, NTile, CumeDist

---

# Rank

## Overview

Computes the rank of each row within a window partition. The rank is one plus the number of rows that precede or are equal to the current row. Tied values receive the same rank, with gaps in subsequent rankings.

## Syntax

```sql
RANK() OVER (window_spec)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Order expressions used for ranking (assigned by analyzer) |

## Return Type

IntegerType (non-nullable)

## Supported Data Types

Order expressions can be any comparable data types.

## Algorithm

- Tracks current row number and rank value
- Stores previous values of ORDER BY expressions
- When ORDER BY values change, updates rank to current row number
- When ORDER BY values stay same, keeps previous rank
- Uses RowFrame from UnboundedPreceding to CurrentRow

## Partitioning Behavior

- Preserves partitioning from window specification  
- Ranking resets within each partition
- Requires window execution which may trigger shuffle

## Edge Cases

- Tied values (same ORDER BY values) receive identical ranks
- Subsequent ranks after ties have gaps (e.g., 1, 1, 3, 4)
- Empty partitions produce no results
- Single-row partitions always get rank 1

## Code Generation

Supports code generation as part of aggregate window function framework.

## Examples

```sql
-- Basic ranking
SELECT emp_id, salary, RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;

-- Ranking within departments
SELECT emp_id, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as dept_salary_rank
FROM employees;
```

```scala
// DataFrame API usage  
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val window = Window.partitionBy("dept_id").orderBy(desc("salary"))
df.select($"emp_id", $"dept_id", $"salary",
         rank().over(window).alias("dept_salary_rank"))
```

## See Also

DenseRank, RowNumber, PercentRank, NTile

---

# SpecifiedWindowFrame

## Overview

Defines the specific boundaries of a window frame, specifying both the frame type (ROW or RANGE) and the lower/upper boundaries. Window frames determine which rows are included in aggregate calculations for each row.

## Syntax

```sql
{ROWS | RANGE} BETWEEN lower_bound AND upper_bound
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| frameType | FrameType | Either RowFrame or RangeFrame |
| lower | Expression | Lower boundary (can be SpecialFrameBoundary or foldable Expression) |
| upper | Expression | Upper boundary (can be SpecialFrameBoundary or foldable Expression) |

## Return Type

Not directly evaluable - used as specification for window operations.

## Supported Data Types

- RowFrame: IntegerType for boundaries
- RangeFrame: Numeric and interval types for boundaries, must match ORDER BY column type

## Algorithm

- Validates boundary expressions are foldable (constant values)
- Ensures frame type compatibility with boundary data types
- Checks logical boundary ordering (lower <= upper)
- Validates special boundaries (UNBOUNDED, CURRENT ROW) usage
- For range frames, validates compatibility with ORDER BY expressions

## Partitioning Behavior

- Defines subset of partition rows for aggregate calculations
- Does not affect partitioning scheme itself
- Frame evaluation occurs within existing partitions

## Edge Cases

- UNBOUNDED FOLLOWING cannot be lower boundary
- UNBOUNDED PRECEDING cannot be upper boundary  
- Boundary expressions must be compile-time constants
- Range frame boundaries must match ORDER BY column data type
- Invalid boundary combinations cause analysis errors

## Code Generation

Frame boundary evaluation supports code generation where applicable.

## Examples

```sql
-- Row-based frame
SELECT emp_id, salary,
       AVG(salary) OVER (ORDER BY salary ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as avg_sal
FROM employees;

-- Range-based frame with interval
SELECT date_col, value,
       SUM(value) OVER (ORDER BY date_col RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW)
FROM daily_data;

-- Unbounded frame
SELECT emp_id, salary,
       SUM(salary) OVER (ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_sum
FROM employees;
```

## See Also

WindowSpecDefinition, RowFrame, RangeFrame, UnboundedPreceding, UnboundedFollowing, CurrentRow