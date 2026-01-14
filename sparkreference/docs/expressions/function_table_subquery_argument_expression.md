# FunctionTableSubqueryArgumentExpression

## Overview
FunctionTableSubqueryArgumentExpression is a specialized subquery expression that represents a TABLE argument passed to User-Defined Table Functions (UDTFs) in Spark SQL. It encapsulates a logical plan along with partitioning, ordering, and column selection specifications that control how the table data is processed before being passed to the UDTF.

## Syntax
```sql
-- Used within UDTF calls with TABLE arguments
SELECT * FROM my_udtf(
  TABLE(SELECT * FROM source_table) 
  PARTITION BY col1, col2 
  ORDER BY col3 
  WITH SINGLE PARTITION
)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| plan | LogicalPlan | The logical plan representing the table data to be processed |
| outerAttrs | Seq[Expression] | Expressions from outer query scope (default: empty) |
| exprId | ExprId | Unique expression identifier (default: auto-generated) |
| partitionByExpressions | Seq[Expression] | Expressions used for partitioning the data (default: empty) |
| withSinglePartition | Boolean | Whether to force all data into a single partition (default: false) |
| orderByExpressions | Seq[SortOrder] | Sort orders to apply within partitions (default: empty) |
| selectedInputExpressions | Seq[PythonUDTFSelectedExpression] | Specific expressions to evaluate for UDTF input (default: empty) |

## Return Type
Returns a DataType that matches the schema of the underlying logical plan (`plan.schema`). The expression is marked as non-nullable and returns data structured for UDTF consumption.

## Supported Data Types
Supports all Spark SQL data types since it operates at the logical plan level rather than on specific column types. The actual data type support depends on the underlying table schema and the expressions used in partitioning and selection clauses.

## Algorithm

- Validates that `withSinglePartition` and `partitionByExpressions` are mutually exclusive
- Creates an evaluable logical plan by applying repartitioning operations when needed
- Adds projection operations for partition expressions that aren't already in the plan output
- Applies sorting operations to ensure proper partition boundary detection in Python UDTFs
- Wraps the final result in a struct format suitable for UDTF consumption

## Partitioning Behavior
How this expression affects partitioning:

- **Requires shuffle**: When `partitionByExpressions` is non-empty, uses `RepartitionByExpression` 
- **Single partition**: When `withSinglePartition` is true, forces all data into one partition via `Repartition`
- **Preserves ordering**: Adds global sorting operations to maintain order within and across partitions
- **Partition detection**: Includes partition expression indexes to help Python UDTFs detect partition boundaries

## Edge Cases

- **Mutual exclusion**: Throws assertion error if both `withSinglePartition=true` and `partitionByExpressions` are provided
- **Missing aliases**: Throws `QueryCompilationErrors` when selected expressions lack required aliases
- **Empty partitions**: Handles empty partition expressions by skipping repartitioning operations
- **Expression deduplication**: Avoids projecting partition expressions that already exist in plan output
- **Null handling**: Inherits null handling behavior from the underlying logical plan

## Code Generation
This expression extends `Unevaluable`, meaning it cannot be directly executed and does not support Tungsten code generation. It must be resolved and replaced with concrete operators during query planning before execution.

## Examples
```sql
-- UDTF with partitioned table argument
SELECT * FROM my_python_udtf(
  TABLE(SELECT customer_id, order_date, amount FROM orders)
  PARTITION BY customer_id
  ORDER BY order_date
);

-- UDTF with single partition requirement
SELECT * FROM aggregating_udtf(
  TABLE(SELECT * FROM sales_data)
  WITH SINGLE PARTITION
  ORDER BY timestamp
);
```

```scala
// This is an internal expression used during query planning
// Not directly accessible through DataFrame API
// Created internally when parsing UDTF TABLE arguments
val tableArg = FunctionTableSubqueryArgumentExpression(
  plan = logicalPlan,
  partitionByExpressions = Seq(col("customer_id").expr),
  orderByExpressions = Seq(SortOrder(col("order_date").expr, Ascending))
)
```

## See Also

- SubqueryExpression - Parent class for subquery-related expressions
- RepartitionByExpression - Used internally for hash-based partitioning
- PythonUDTFSelectedExpression - Represents selected input expressions for UDTFs
- LogicalPlan - The underlying plan structure being wrapped