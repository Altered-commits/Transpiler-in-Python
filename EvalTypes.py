'''
The home to Functions and CONSTANTS which will be used in Semantic Analysis
Contains Functions to determine expression type, promote types if possible, check valid types for specific operators, etc.
'''
from Token import *
from Printer import printError, printWarning

#MAX NUMERIC VALUES ALLOWED FOR EACH TYPE
INT64_MAX  = 9223372036854775807
INT64_MIN  = -9223372036854775808
UINT64_MAX = 18446744073709551615

#Integer Unsigned
EVAL_UINT8  = 0
EVAL_UINT16 = 1
EVAL_UINT32 = 2
EVAL_UINT64 = 3

#Integer Signed
EVAL_INT8  = 4
EVAL_INT16 = 5
EVAL_INT32 = 6
EVAL_INT64 = 7

#Float
EVAL_FLOAT32 = 8
EVAL_FLOAT64 = 9

'''
evalTypeToString: EVAL_ type converted to string format
'''
def evalTypeToString(evalType):
    evalToStringMapper = {
        EVAL_UINT8:   "uint8_t",
        EVAL_UINT16:  "uint16_t",
        EVAL_UINT32:  "uint32_t",
        EVAL_UINT64:  "uint64_t",
        EVAL_INT8:    "int8_t",
        EVAL_INT16:   "int16_t",
        EVAL_INT32:   "int32_t",
        EVAL_INT64:   "int64_t",
        EVAL_FLOAT32: "float",
        EVAL_FLOAT64: "double"
    }
    
    return evalToStringMapper.get(evalType)

'''
invertIntegerType: Converts uint to int and viceversa.
'''
def invertIfIntegerType(valueType):
    #Should only work on Integer types, flip 4th bit to get uint or int
    return valueType ^ 4 if valueType <= EVAL_INT64 else valueType

'''
deduceType: Given a value in string format, it tries to deduce its type to some Integer / Float.
'''
def deduceType(value, isFloat = False, isChar = False) -> int:
    if isFloat:
        try:
            # Determine if the float is float32 or float64 based on its length
            return [float(value), EVAL_FLOAT32] if len(value) <= 7 else [float(value), EVAL_FLOAT64]
        except ValueError:
            printError("TypeDeductionError", f"Invalid floating point number: '{value}'")

    if isChar:
        codePoint = ord(value)
        
        #7-bit ASCII
        if codePoint <= 0x7F:
            returnType = EVAL_UINT8
        # 16-bit Unicode
        elif codePoint <= 0xFFFF:
            returnType = EVAL_UINT16
        # 32-bit Unicode
        else:
            returnType = EVAL_UINT32
        
        return [codePoint, returnType]

    integerValue = int(value)
    returnType = None

    errorMsg = "Numeric value out of range for {IntType} Integer: '{Value}'\n\
[AdditionalInfo]: {IntType} Integer range -> MIN: {MinValue}, MAX: {MaxValue}"

    if integerValue >= 0:
        if integerValue < UINT64_MAX:
            if integerValue <= 255:
                returnType = EVAL_UINT8
            elif integerValue <= 65535:
                returnType = EVAL_UINT16
            elif integerValue <= 4294967295:
                returnType = EVAL_UINT32
            else:
                returnType = EVAL_UINT64
        else:
            printError("TypeDeductionError",
                    errorMsg.format(IntType = "Unsigned", Value = integerValue, MinValue = 0, MaxValue = UINT64_MAX))
    else:
        if integerValue > INT64_MIN and integerValue < INT64_MAX:
            if -128 <= integerValue <= 127:
                returnType = EVAL_INT8
            elif -32768 <= integerValue <= 32767:
                returnType = EVAL_INT16
            elif -2147483648 <= integerValue <= 2147483647:
                returnType = EVAL_INT32
            else:
                returnType = EVAL_INT64
        else:
            printError("TypeDeductionError",
                       errorMsg.format(IntType = "Signed", Value = integerValue, MinValue = INT64_MIN, MaxValue = INT64_MAX))
    
    return [integerValue, returnType]

'''
determineExpressionType: Given left and right expression types and operator,
                         it determines the resultant type based on some rules provided.
Example:
    uint8 + uint8 -> uint8
    int8 - uint8 -> int8
    uint64 + int16 -> uint64
    int32 == uint8 -> uint8 (see the third point)

    and so on....

    -Basically if operator isn't '-' then it returns highest bit width of both left and right expr
    -Else it returns Integer (signed) type if operator is '-'

    -For comparision and logical operators it always returns uint8, as they return a boolean (1 or 0)
'''
categorizedTypePriority = {
    EVAL_UINT8: 0, EVAL_UINT16: 1, EVAL_UINT32: 2, EVAL_UINT64: 3,
    EVAL_INT8: 0, EVAL_INT16: 1, EVAL_INT32: 2, EVAL_INT64: 3,
    #Floating point numbers will be given higher priority, always
    EVAL_FLOAT32: 4, EVAL_FLOAT64: 5
}

typeCategory = {
    EVAL_UINT8: 0, EVAL_UINT16: 0, EVAL_UINT32: 0, EVAL_UINT64: 0,
    EVAL_INT8: 1, EVAL_INT16: 1, EVAL_INT32: 1, EVAL_INT64: 1,
    EVAL_FLOAT32: 2, EVAL_FLOAT64: 2
}

def determineExpressionType(leftType, rightType, operator) -> int:
    LTP = categorizedTypePriority.get(leftType)
    RTP = categorizedTypePriority.get(rightType)
    LTC = typeCategory[leftType]
    RTC = typeCategory[rightType]

    isMinusOperator   = (operator == TOKEN_SUB)
    leftIsNotUnsigned = (leftType >= EVAL_INT8)

    #If operator is either *, /, %
    if(tokenInGroup(operator, TERM_GROUP)):
        evalByTypePriority = leftType if LTP > RTP else rightType
        if LTC == RTC:
            return invertIfIntegerType(evalByTypePriority) if LTC == 1 else evalByTypePriority
        
        #Mixed types, return signed integer if not signed but with highest bitwidth
        return invertIfIntegerType(evalByTypePriority) if evalByTypePriority <= EVAL_UINT64 else evalByTypePriority

    #Comparision or logical operators
    if(tokenInGroup(operator, COMPARISION_AND_LOGICAL_GROUP)):
        return EVAL_UINT8

    #Rest of the operators
    if LTP > RTP:
        return leftType
    if LTP < RTP:
        return rightType + 4 if (RTC == 0 and isMinusOperator) else rightType
    #Priority is same for both, check their categories
    if(LTC == RTC):
        #Both are same type so (for - operator)[if its uint, return int version, else return the type itself]
        return leftType + 4 if (not leftIsNotUnsigned and isMinusOperator) else leftType
    
    #If both arent in same category then return whichever one is signed
    return leftType if leftIsNotUnsigned else rightType

'''
promoteType: Given a inital type and a new type, it will safely promote the initial type to new type
             based on certain rules provided
            -Will throw an error if it cannot be promoted to the given type
'''

#Mapping from unsigned to signed types with the same bit width
uintToInt = {
    EVAL_UINT8: EVAL_INT8,
    EVAL_UINT16: EVAL_INT16,
    EVAL_UINT32: EVAL_INT32,
    EVAL_UINT64: EVAL_INT64
}

def promoteType(initialType, newType, identifier):
    if initialType == newType:
        return initialType

    initialPriority = categorizedTypePriority[initialType]
    newPriority = categorizedTypePriority[newType]

    #If any type is float, promote to float
    if initialType >= EVAL_FLOAT32 or newType >= EVAL_FLOAT32:
        printWarning("TypePromotionWarning", f"Promotion of identifier '{identifier}' to floating type may cause it's previous values to loose their precision")
        return EVAL_FLOAT32 if newPriority <= categorizedTypePriority[EVAL_FLOAT32] else EVAL_FLOAT64
    
    #Unsigned to signed conversion is allowed, with at least the same bit width
    if initialType <= EVAL_UINT64 and newType >= EVAL_INT8:
        correspondingSignedType = uintToInt.get(initialType, EVAL_INT64)
        return max(correspondingSignedType, newType, key=lambda t: categorizedTypePriority[t])
    
    #Prevent signed to unsigned conversion
    if initialType >= EVAL_INT8 and newType <= EVAL_UINT64:
        errorMsg = f"Cannot promote signed integer '{evalTypeToString(initialType)}' to unsigned type '{evalTypeToString(newType)}'\n"
        errorMsg += f"[AdditionalInfo]: Tried to assign '{evalTypeToString(newType)}' type expression to identifier '{identifier}' which was previously deduced to '{evalTypeToString(initialType)}' by Transpiler"
        printError("TypePromotionError", errorMsg)

    #Promote to larger bitwidth if necessary
    if newPriority > initialPriority:
        return newType

    return initialType