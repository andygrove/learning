# Luhncheck

## Overview
The `Luhncheck` expression validates whether a given string represents a valid number according to the Luhn algorithm (also known as the "modulus 10" algorithm). This is commonly used to validate credit card numbers, IMEI numbers, and other identification numbers that use Luhn checksum validation.

## Syntax
```sql
luhn_check(input_string)
```

```scala
// DataFrame API
col("column_name").luhn_check()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | String | The string to be validated using the Luhn algorithm |

## Return Type
`BooleanType` - Returns `true` if the input string passes Luhn validation, `false` otherwise.

## Supported Data Types

- String types with collation support (supports trim collation)
- Input values are implicitly cast to string type if not already strings

## Algorithm

- Delegates validation to the `ExpressionImplUtils.isLuhnNumber` static method via `StaticInvoke`
- Implements the Luhn algorithm which processes digits from right to left
- Doubles every second digit from the right, subtracting 9 if the result exceeds 9
- Sums all digits and checks if the total is divisible by 10
- Returns boolean result indicating whether the checksum validates

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling across partitions
- Can be evaluated independently on each partition
- Maintains existing partitioning scheme when used in transformations

## Edge Cases

- **Null handling**: Returns `null` if the input string is `null`
- **Empty string**: Returns `false` for empty strings as they cannot contain valid Luhn numbers
- **Non-numeric characters**: Behavior depends on the underlying `isLuhnNumber` implementation
- **Leading/trailing whitespace**: Handled according to trim collation support
- **Single digit numbers**: May return `false` as Luhn algorithm typically requires multiple digits

## Code Generation
This expression uses `RuntimeReplaceable` pattern with `StaticInvoke`:

- Does not generate custom code via Tungsten code generation
- Falls back to interpreted mode by invoking the static method at runtime
- The `StaticInvoke` provides some optimization by avoiding object creation

## Examples
```sql
-- Valid credit card number
SELECT luhn_check('4532015112830366');
-- Returns: true

-- Invalid number
SELECT luhn_check('79927398714');
-- Returns: false

-- Using with table data
SELECT customer_id, luhn_check(credit_card_number) as is_valid
FROM customers;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("credit_card_number"), 
         expr("luhn_check(credit_card_number)").as("is_valid"))

// Using in filter conditions
df.filter(expr("luhn_check(account_number) = true"))
```

## See Also

- String manipulation functions
- Validation expressions
- `regexp_like` for pattern-based validation
- `length` for string length validation