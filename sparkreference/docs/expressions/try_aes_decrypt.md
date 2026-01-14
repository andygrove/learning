# TryAesDecrypt

## Overview
TryAesDecrypt is a RuntimeReplaceable expression that provides a safe version of AES decryption functionality. Unlike the regular AesDecrypt function, it returns a replacement value (typically NULL) instead of throwing an exception when decryption fails due to invalid input, wrong key, or corrupted data.

## Syntax
```sql
try_aes_decrypt(input, key [, mode [, padding [, aad]]])
```

```scala
// DataFrame API usage would depend on the specific SQL function registration
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | The encrypted binary data to decrypt |
| key | Expression | The decryption key |
| mode | Expression | The encryption mode (defaults to "GCM") |
| padding | Expression | The padding scheme (defaults to "DEFAULT") |
| aad | Expression | Additional authenticated data (defaults to empty string) |

## Return Type
Binary data type (typically `BinaryType`) or the replacement value type when decryption fails.

## Supported Data Types

- **input**: Binary data types containing encrypted content
- **key**: Binary or string types representing the decryption key
- **mode**: String type specifying the AES mode (e.g., "GCM", "CBC")
- **padding**: String type specifying the padding scheme
- **aad**: String or binary type for additional authenticated data

## Algorithm

- Wraps the underlying AesDecrypt expression with TryEval functionality
- Attempts to decrypt the input using the specified AES parameters
- Returns the decrypted result if successful
- Returns the replacement value (typically NULL) if decryption fails for any reason
- Leverages the RuntimeReplaceable pattern to delegate actual computation to the wrapped expression

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates row-by-row
- Maintains the same partitioning scheme as the input DataFrame
- Can be evaluated independently on each partition

## Edge Cases

- **Null inputs**: Returns NULL if any required input parameter is NULL
- **Invalid key length**: Returns replacement value instead of throwing exception
- **Corrupted encrypted data**: Returns replacement value for malformed input
- **Mismatched mode/padding**: Returns replacement value for incompatible parameter combinations
- **Authentication failures**: In authenticated modes like GCM, returns replacement value for authentication failures

## Code Generation
As a RuntimeReplaceable expression, TryAesDecrypt delegates code generation to its replacement expression (TryEval wrapping AesDecrypt). The actual code generation support depends on the underlying AesDecrypt implementation and TryEval wrapper capabilities.

## Examples
```sql
-- Basic usage with default parameters
SELECT try_aes_decrypt(encrypted_column, 'my-secret-key') FROM table;

-- With explicit mode and padding
SELECT try_aes_decrypt(data, key_col, 'GCM', 'PKCS') FROM encrypted_table;

-- With additional authenticated data
SELECT try_aes_decrypt(payload, secret, 'GCM', 'DEFAULT', aad_column) FROM secure_data;
```

```scala
// Scala usage would depend on SQL function registration
// This is a RuntimeReplaceable expression primarily used via SQL
```

## See Also

- AesDecrypt - The underlying decryption function that throws exceptions on failure
- AesEncrypt - The corresponding encryption function
- TryEval - The wrapper that provides exception-safe evaluation
- Other cryptographic functions in the misc_funcs group