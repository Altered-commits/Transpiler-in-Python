from Token import *
from EvalTypes import *

'''
def deduce_type(value, isFloat = False, forceSigned = False) -> int:
    # Check if the value is a float
    if isFloat:
        # Determine if the float is float32 or float64 based on its length
        return TOKEN_FLOAT32 if len(value) <= 7 else TOKEN_FLOAT64

    numeric_value = int(value)

    # Check if the value is within the range of INT64
    if numeric_value < INT64_MIN or numeric_value > UINT64_MAX:
        raise ValueError(f"Numeric value out of range: '{value}'")

    # Determine the type based on the value
    if not forceSigned and numeric_value >= 0:
        if numeric_value <= 255:
            return TOKEN_UINT8
        if numeric_value <= 65535:
            return TOKEN_UINT16
        if numeric_value <= 4294967295:
            return TOKEN_UINT32
        return TOKEN_UINT64
    else:
        if -128 <= numeric_value <= 127:
            return TOKEN_INT8
        if -32768 <= numeric_value <= 32767:
            return TOKEN_INT16
        if -2147483648 <= numeric_value <= 2147483647:
            return TOKEN_INT32
        return TOKEN_INT64

def promote_type(current_type: int, new_value: str) -> int:
    new_type = deduce_type(new_value, current_type >= TOKEN_INT8 and current_type <= TOKEN_INT64)
    
    promotion_table = {
        TOKEN_INT8: [TOKEN_INT16, TOKEN_INT32, TOKEN_INT64],
        TOKEN_INT16: [TOKEN_INT32, TOKEN_INT64],
        TOKEN_INT32: [TOKEN_INT64],
        TOKEN_UINT8: [TOKEN_UINT16, TOKEN_UINT32, TOKEN_UINT64],
        TOKEN_UINT16: [TOKEN_UINT32, TOKEN_UINT64],
        TOKEN_UINT32: [TOKEN_UINT64],
        TOKEN_FLOAT32: [TOKEN_FLOAT64]
    }

    if current_type == new_type:
        return current_type

    # Check if the new value falls within the valid range of the current type
    if current_type in [TOKEN_INT8, TOKEN_INT16, TOKEN_INT32, TOKEN_INT64]:
        if current_type in [TOKEN_INT8, TOKEN_INT16, TOKEN_INT32, TOKEN_INT64]:
            if new_type in [TOKEN_UINT8, TOKEN_UINT16, TOKEN_UINT32, TOKEN_UINT64]:
                raise TypeError("Cannot promote signed integer to unsigned integer")
            for promotion in promotion_table.get(current_type, []):
                if new_type == promotion:
                    return promotion
        raise TypeError(f"Cannot promote value '{new_value}' to signed integer type {current_type}")
    elif current_type in [TOKEN_UINT8, TOKEN_UINT16, TOKEN_UINT32, TOKEN_UINT64]:
        if current_type in [TOKEN_UINT8, TOKEN_UINT16, TOKEN_UINT32, TOKEN_UINT64]:
            if new_type in [TOKEN_INT8, TOKEN_INT16, TOKEN_INT32, TOKEN_INT64]:
                raise TypeError("Cannot promote unsigned integer to signed integer")
            for promotion in promotion_table.get(current_type, []):
                if new_type == promotion:
                    return promotion
        raise TypeError(f"Cannot promote value '{new_value}' to unsigned integer type {current_type}")
    elif current_type in [TOKEN_FLOAT32, TOKEN_FLOAT64]:
        for promotion in promotion_table.get(current_type, []):
            if new_type == promotion:
                return promotion
    else:
        raise TypeError("Unsupported type promotion")

    raise TypeError(f"Unsupported type promotion from {current_type} to {new_type}")




# Example usage
current_value = "-100" #int8
new_value = "100000"   #uint32

promoted_type = promote_type(deduce_type(current_value), new_value)
print(f"Promoted type: {promoted_type}")  # Should print: Promoted type: 3 (TOKEN_INT32)'''