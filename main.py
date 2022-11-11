import sys

# Tokens
TOKEN_EOF = -1
TOKEN_IDENT = 1
TOKEN_CONST = 2
TOKEN_ASMT = 3
TOKEN_SEMI_COLON = 4
TOKEN_ADD = 5
TOKEN_MULT = 6
TOKEN_LEFT_PAREN = 7
TOKEN_RIGHT_PAREN = 8

# Lexical Analyzer Index
INDEX = 0

# Lexeme Value, Token
tokenNext = 0
tokenString = ""

# Variables for Saving Calculation Value
calcProcessDict = {}
stkIdent = []
stkConst = []
stkOperation = []

# Warning Message
isLogicWarning = False
msgLogicWarning = ""
isNameWarning = False
msgNameWarning = ""

# Count of ID, TOKEN_CONST, OP
cntIdent = 0
cntConst = 0
cntOperator = 0


def main(argv):
    scriptFile = open(argv[1], "r")

    inputString = ""
    for curLine in scriptFile.readlines():
        inputString += curLine.strip()

    inputString += "@"
    checkLexical(inputString)
    checkStatements(inputString)

    scriptFile.close()


# Lexical Analyzer
def checkLexical(inputString):
    global INDEX, tokenNext, tokenString
    lexeme = ""
    if inputString[INDEX].isalpha():
        # Check IDENT
        while inputString[INDEX].isalpha() or inputString[INDEX].isdigit():
            lexeme += inputString[INDEX]
            INDEX += 1
        tokenNext = TOKEN_IDENT
        tokenString = lexeme
    elif inputString[INDEX].isdigit():
        # Check CONST
        while inputString[INDEX].isdigit():
            lexeme += inputString[INDEX]
            INDEX += 1
        tokenNext = TOKEN_CONST
        tokenString = lexeme
    elif inputString[INDEX] == ":":
        # Check Assignment Operator
        tokenNext = TOKEN_ASMT
        tokenString = ":="
        INDEX += 2
    elif inputString[INDEX] == ";":
        # Check Semicolon
        tokenNext = TOKEN_SEMI_COLON
        tokenString = inputString[INDEX]
        INDEX += 1
    elif inputString[INDEX] == "+" or inputString[INDEX] == "-":
        # Check Add Operator
        tokenNext = TOKEN_ADD
        tokenString = inputString[INDEX]
        INDEX += 1
    elif inputString[INDEX] == "*" or inputString[INDEX] == "/":
        # Check Multiply Operator
        tokenNext = TOKEN_MULT
        tokenString = inputString[INDEX]
        INDEX += 1
    elif inputString[INDEX] == "(":
        # Check Left Paren
        tokenNext = TOKEN_LEFT_PAREN
        tokenString = inputString[INDEX]
        INDEX += 1
    elif inputString[INDEX] == ")":
        # Check Right Paren
        tokenNext = TOKEN_RIGHT_PAREN
        tokenString = inputString[INDEX]
        INDEX += 1
    elif inputString[INDEX] == "@":
        # Check File End
        tokenNext = TOKEN_EOF
        tokenString = inputString[INDEX]
    else:
        INDEX += 1
        checkLexical(inputString)


# Check Statements
def checkStatements(inputString):
    checkStatement(inputString)
    if tokenNext == 4:
        checkLexical(inputString)
        checkStatements(inputString)


# Check Statement
def checkStatement(inputString):
    global isLogicWarning, cntIdent, cntConst, cntOperator, isNameWarning, msgNameWarning, msgLogicWarning
    if tokenNext == 1:
        calcProcessDict[tokenString] = "Unknown"
        stkIdent.append(tokenString)

        print(f"{tokenString} ", end="")

        cntIdent += 1
        checkLexical(inputString)
        if tokenNext == 3:
            print(f"{tokenString} ", end="")

            checkLexical(inputString)
            checkExpr(inputString)
            if stkConst[-1] == "Unknown":
                calcProcessDict[stkIdent[-1]] = "Unknown"
            else:
                calcProcessDict[stkIdent[-1]] = int(stkConst[-1])
            stkIdent.pop()
            stkConst.pop()
        else:
            print("Error")
    else:
        print("Error")

    if tokenNext != -1:
        print(tokenString)

        if isLogicWarning:
            print(f"ID : {str(cntIdent)}; TOKEN_CONST : {str(cntConst)}; OP : {str(cntOperator)};")
            print("(Warning) 중복 연산자({msgLogicWarning}) 제거")

            isLogicWarning = False
            msgLogicWarning = ""
        elif isNameWarning:
            print(f"ID : {str(cntIdent)}; TOKEN_CONST : {str(cntConst)}; OP : {str(cntOperator)};")
            print("(Error) 정의되지 않은 변수({msgNameWarning})가 참조됨")

            isNameWarning = False
            msgNameWarning = ""
        else:
            print(f"ID : {str(cntIdent)}; TOKEN_CONST : {str(cntConst)}; OP : {str(cntOperator)};")
            print("(OK)")
    else:
        print()

        if isLogicWarning:
            print(f"ID : {str(cntIdent)}; TOKEN_CONST : {str(cntConst)}; OP : {str(cntOperator)};")
            print(f"(Warning) 중복 연산자({msgLogicWarning}) 제거")

            isLogicWarning = False
            msgLogicWarning = ""
        else:
            print(f"ID : {str(cntIdent)}; TOKEN_CONST : {str(cntConst)}; OP : {str(cntOperator)};")
            print("(OK)")


        print(f"Result == > operand1 : {str(calcProcessDict['operand1'])}; operand2 : {str(calcProcessDict['operand2'])}; target : {str(calcProcessDict['target'])};")

    cntIdent = 0
    cntConst = 0
    cntOperator = 0


# Check Expression
def checkExpr(inputString):
    checkTerm(inputString)
    checkTermTail(inputString)


# Check Term
def checkTerm(inputString):
    checkFactor(inputString)
    checkFactorTail(inputString)


# Check Term Tail
def checkTermTail(inputString):
    global isLogicWarning, cntOperator, msgLogicWarning
    if tokenNext == 5:
        print(f"{tokenString} ", end="")

        cntOperator += 1
        stkOperation.append(tokenString)
        checkLexical(inputString)
        if tokenNext == 5:
            print(f"{tokenString} ", end="")

            isLogicWarning = True
            msgLogicWarning = tokenString
            checkLexical(inputString)
        checkTerm(inputString)
        checkTermTail(inputString)


# Check Factor
def checkFactor(inputString):
    global cntIdent, cntConst, isNameWarning, msgNameWarning
    if tokenNext == 7:
        print(f"{tokenString} ", end="")

        checkLexical(inputString)
        checkExpr(inputString)
        if tokenNext == 8:
            print(f"{tokenString} ", end="")

            checkLexical(inputString)
        else:
            print("Error")

    elif tokenNext == 1:
        print(f"{tokenString} ", end="")

        cntIdent += 1
        if tokenString not in calcProcessDict:
            # Un-initialized Variable
            calcProcessDict[tokenString] = "Unknown"
            isNameWarning = True
            msgNameWarning = tokenString
            stkIdent.append(tokenString)
        else:
            stkIdent.append(tokenString)
        checkLexical(inputString)
    elif tokenNext == 2:
        print(f"{tokenString} ", end="")

        cntConst += 1
        stkConst.append(tokenString)
        if len(stkConst) == 2:
            tempConst = int(stkConst[-1]) + int(stkConst[-2])
            stkConst.pop()
            stkConst.pop()
            stkConst.append(tempConst)
        while len(stkIdent) >= 2:
            if calcProcessDict[stkIdent[-1]] == "Unknown":
                stkIdent.pop()
                stkConst.pop()
                stkOperation.pop()
                stkConst.append("Unknown")
            else:
                if stkOperation[-1] == "+":
                    temp = (int(calcProcessDict[stkIdent[-1]]) + int(stkConst[-1]))
                    stkIdent.pop()
                    stkConst.pop()
                    stkOperation.pop()
                    stkConst.append(temp)
                elif stkOperation[-1] == "-":
                    temp = (int(calcProcessDict[stkIdent[-1]]) - int(stkConst[-1]))
                    stkIdent.pop()
                    stkConst.pop()
                    stkOperation.pop()
                    stkConst.append(temp)
                elif stkOperation[-1] == "*":
                    temp = (int(calcProcessDict[stkIdent[-1]]) * int(stkConst[-1]))
                    stkIdent.pop()
                    stkConst.pop()
                    stkOperation.pop()
                    stkConst.append(temp)
                else:
                    temp = (int(calcProcessDict[stkIdent[-1]]) / int(stkConst[-1]))
                    stkIdent.pop()
                    stkConst.pop()
                    stkOperation.pop()
                    stkConst.append(temp)
        checkLexical(inputString)
    else:
        print("Error")


# Check Factor Tail
def checkFactorTail(inputString):
    global cntOperator, isLogicWarning, msgLogicWarning
    if tokenNext == 6:
        print(f"{tokenString} ", end="")

        cntOperator += 1
        stkOperation.append(tokenString)
        checkLexical(inputString)
        if tokenNext == 6:
            # Duplicate Operator Removal
            print(f"{tokenString} ", end="")

            isLogicWarning = True
            msgLogicWarning = tokenString
            checkLexical(inputString)
        checkFactor(inputString)
        checkFactorTail(inputString)


if __name__ == "__main__":
    main(sys.argv)
