# PandasProduct

## Overview

`PandasProduct` is a declarative aggregate expression that computes the product of numeric values in a group. It provides enhanced numerical stability for fractional inputs using logarithmic computation, handles integral inputs with LongType variables internally, and offers configurable NULL handling behavior through the `ignoreNA` parameter.

## Syntax

```sql
pandas_product(column, ignoreNA)
```

```scala
// DataFrame API usage would require custom function registration
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `child` | Expression (Numeric) | The input expression/column to compute the product over |
| `ignoreNA` | Boolean | Whether to ignore NULL values (true) or propagate them (false) |

## Return Type

The return type depends on the input data type:

- **IntegralType inputs**: Returns `LongType`
- **Fractional/other numeric inputs**: Returns `DoubleType`

## Supported Data Types

- All numeric types (IntegralType, FractionalType)
- Input must satisfy `NumericType` constraint through `ImplicitCastInputTypes`

## Algorithm

- **For IntegralType**: Maintains a running product using LongType multiplication and tracks NULL presence
- **For FractionalType**: Uses logarithmic computation for numerical stability - maintains `logSum` (sum of log absolute values), tracks sign changes via `positive` flag, and monitors zero/null occurrences
- **Zero handling**: Short-circuits computation when zero is encountered to avoid unnecessary calculations
- **NULL propagation**: Configurable via `ignoreNA` - either skips NULLs or propagates them to final result
- **Final evaluation**: For fractional types, reconstructs product using `exp(logSum)` with appropriate sign

## Partitioning Behavior

- **Preserves partitioning**: No, this is an aggregate function that requires grouping
- **Requires shuffle**: Yes, when used with GROUP BY operations across partitions
- **Merge capability**: Supports partial aggregation through `mergeExpressions` for distributed computation

## Edge Cases

- **Null handling**: Configurable via `ignoreNA` parameter - when false, any NULL input makes result NULL; when true, NULLs are ignored
- **Empty input behavior**: Returns initial values (1 for integral, 1.0 for fractional)
- **Zero values**: Result becomes 0, handled efficiently by `containsZero` flag without further computation
- **Overflow behavior**: IntegralType uses LongType internally which can still overflow; FractionalType uses logarithmic computation to minimize overflow risk
- **Negative values**: For fractional inputs, tracks sign changes through `positive` flag to determine final result sign

## Code Generation

This expression extends `DeclarativeAggregate`, which supports Tungsten code generation. The aggregate buffer operations and expressions can be code-generated for improved performance rather than falling back to interpreted mode.

## Examples

```sql
-- Calculate product ignoring NULLs
SELECT pandas_product(sales_amount, true) FROM sales_table;

-- Calculate product propagating NULLs  
SELECT pandas_product(quantity, false) FROM inventory_table;

-- Group by with product aggregation
SELECT category, pandas_product(price, true) 
FROM products 
GROUP BY category;
```

```scala
// Example DataFrame API usage (requires custom function registration)
import org.apache.spark.sql.functions.expr

df.select(expr("pandas_product(amount, true)"))
df.groupBy("category").agg(expr("pandas_product(price, false)"))
```

## See Also

- Standard `Product` aggregate function
- `Sum` and other aggregate expressions
- `DeclarativeAggregate` base class
- Other pandas-compatible aggregate functions