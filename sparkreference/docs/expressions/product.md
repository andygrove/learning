# Product

## Overview
The `Product` expression is a Spark Catalyst unary expression that multiplies numerical values within an aggregation group. It is typically used as an aggregate function to compute the product of all non-null values in a column across rows in a group.

## Syntax
```sql
PRODUCT(column_name)
```

```scala
// DataFrame API
df.agg(expr("product(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that evaluates to numeric values to be multiplied |

## Return Type
Returns a numeric data type based on the input type:

- `IntegralType` inputs return `LongType`
- `DoubleType` and other numeric types return `DoubleType`

## Supported Data Types
Supports all numeric data types that extend `NumericType`:

- `ByteType`
- `ShortType` 
- `IntegerType`
- `LongType`
- `FloatType`
- `DoubleType`
- `DecimalType`

## Algorithm
The Product expression evaluates using the following approach:

- Initializes the product accumulator to 1 (multiplicative identity)
- Iterates through all non-null values in the aggregation group
- Multiplies each value with the running product accumulator
- Skips null values during computation
- Returns the final accumulated product value

## Partitioning Behavior
As an aggregate function, Product has specific partitioning requirements:

- Does not preserve input partitioning since it reduces multiple rows to a single value
- Requires a shuffle operation when used with `GROUP BY` to co-locate rows by grouping key
- In global aggregation (no GROUP BY), all data must be collected to a single partition

## Edge Cases

- **Null handling**: Null values are ignored during multiplication; does not affect the result
- **Empty input**: Returns null when no non-null values are present in the group
- **Zero values**: Any zero value in the group results in a product of zero
- **Overflow behavior**: Integer products that exceed Long.MAX_VALUE will overflow and wrap around
- **Floating-point behavior**: Follows IEEE 754 standards for infinity and NaN propagation

## Code Generation
This expression supports Spark's Tungsten code generation for optimized performance. The generated code eliminates virtual function calls and optimizes the multiplication loop for better CPU efficiency.

## Examples
```sql
-- Calculate product of sales amounts by region
SELECT region, PRODUCT(sales_amount) as total_product
FROM sales_table 
GROUP BY region;

-- Product of all values in a column
SELECT PRODUCT(quantity) as overall_product
FROM inventory;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Group by product and calculate product of quantities
df.groupBy("product_id")
  .agg(expr("product(quantity)").alias("quantity_product"))

// Global product calculation
df.agg(expr("product(price)").alias("price_product"))
```

## See Also

- `Sum` - Aggregate function for addition
- `Avg` - Aggregate function for arithmetic mean
- `Count` - Aggregate function for counting rows
- `Min`/`Max` - Aggregate functions for minimum/maximum values