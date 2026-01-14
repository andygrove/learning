# WindowSpecDefinition

## Overview

WindowSpecDefinition defines the specification for a window operation in Spark SQL, including how input rows are partitioned, ordered within partitions, and framed for window functions. It serves as a container for the three core components of window operations: partition specification, ordering specification, and frame specification.

## Syntax

```sql
(PARTITION BY partition_expr [, ...] ORDER BY order_expr [ASC|DESC] [, ...] frame_specification)
```

```scala
// Used internally in window function expressions
// Not directly accessible in DataFrame API
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| partitionSpec | Seq[Expression] | Expressions that define how input rows are partitioned |
| orderSpec | Seq[SortOrder] | Expressions with sort direction that define row ordering within partitions |
| frameSpecification | WindowFrame | Defines the window frame boundaries (rows or range) |

## Return Type

This expression is `Unevaluable` and throws `QueryCompilationErrors.dataTypeOperationUnsupportedError()` when dataType is accessed. It serves as a specification container rather than producing actual values.

## Supported Data Types

For RANGE frame type with value boundaries:
- **DateType** ordering with: IntegerType, YearMonthIntervalType, or DayTimeIntervalType(DAY, DAY) boundaries
- **TimestampType/TimestampNTZType** ordering with: CalendarIntervalType, YearMonthIntervalType, or DayTimeIntervalType boundaries
- **Matching types**: Any data type where ordering expression type equals boundary expression type

## Algorithm

- Validates frame specification is not UnspecifiedFrame (converted during analysis)
- For RANGE frames: ensures proper ordering requirements and boundary type compatibility
- Checks that RANGE frames with value bounds have exactly one ordering expression
- Validates data type compatibility between ordering expressions and frame boundaries
- Constructs SQL representation combining partition, order, and frame specifications

## Partitioning Behavior

WindowSpecDefinition itself doesn't affect partitioning but defines it:
- **Partition preservation**: Depends on the partitionSpec expressions
- **Shuffle requirement**: PARTITION BY clauses typically require shuffle unless data is already partitioned correctly
- The partitionSpec determines how data is distributed across partitions for window operations

## Edge Cases

- **Null handling**: Inherits nullable = true, specific null behavior depends on constituent expressions
- **UnspecifiedFrame**: Throws internal error if not converted during analysis phase
- **RANGE without ORDER**: DataTypeMismatch error for RANGE frames without ordering specification
- **Multiple ORDER with RANGE**: Error when RANGE frame has value bounds but multiple ordering expressions
- **Type mismatch**: Error when RANGE frame boundary type incompatible with ordering expression type
- **Empty specifications**: Handles empty partitionSpec and orderSpec sequences gracefully

## Code Generation

This expression is marked as `Unevaluable`, meaning:
- **No code generation**: Does not participate in Tungsten code generation
- **Specification only**: Used during query planning and analysis phases
- **Runtime behavior**: Not evaluated at runtime, only used to configure window operations

## Examples

```sql
-- Basic window specification
ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)

-- With frame specification
SUM(salary) OVER (PARTITION BY department ORDER BY hire_date 
                  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- Range frame with interval
AVG(sales) OVER (PARTITION BY region ORDER BY date 
                 RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW)
```

```scala
// Internal usage in Catalyst expressions
// WindowSpecDefinition is created during SQL parsing/analysis
// Not directly instantiated in DataFrame API

// Equivalent DataFrame operations use Window.partitionBy() and Window.orderBy()
import org.apache.spark.sql.expressions.Window
val windowSpec = Window.partitionBy("department").orderBy("salary")
df.withColumn("row_number", row_number().over(windowSpec))
```

## See Also

- **WindowFrame**: Defines frame boundaries (SpecifiedWindowFrame, UnspecifiedFrame)
- **SortOrder**: Defines ordering expressions with direction
- **WindowFunction**: Functions that use window specifications
- **Window**: DataFrame API for creating window specifications