class TreeNode:
    def __init__(self, src_token):
        self.value = src_token[0]
        self.token = src_token[1]
        self.left = None
        self.right = None


def setToken(value):
    match value:
        case "(":
            return "lparen"
        case ")":
            return "rparen"
        case "+":
            return "plus"
        case "-":
            return "minus"
        case "*":
            return "mult"
        case "/":
            return "div"
        case _:
            if value.isdigit():
                return "num"
            else:
                raise ValueError(f"Invalid token: {value}")


def tokenize(src):
    toReturnList = []
    index = 0
    while index < len(src):
        v = src[index]
        templist = []
        templist.append(v)
        if v == " ":
            index += 1
            continue
        token = setToken(v)
        if token == "num":
            num = v
            while index + 1 < len(src) and setToken(src[index + 1]) == "num":
                num += src[index + 1]
                index += 1
            templist[0] = num
        templist.append(token)
        toReturnList.append(templist)
        index += 1
    return toReturnList


def parseEx(lexer_list, p1_precedence):
    precedence_dict = {"lparen": 3, "rparen": 3, "mult": 2, "div": 2, "plus": 1, "minus": 1, "num": 0}
    while lexer_list:  # while there is still items in list,
        if len(lexer_list) == 1:  # base case, if only 1 element left in list
            temp = TreeNode(lexer_list[0])
            lexer_list.pop(0)
            return temp  # return only element left
        if lexer_list[1][1] == "rparen":  # base case, if only 1 element left in parentheses
            temp = TreeNode(lexer_list[0])
            lexer_list.pop(0)
            lexer_list.pop(0)
            return temp  # return only element left
        if lexer_list[0][1] == "lparen":
            lexer_list.pop(0)
            return parseEx(lexer_list, 0)
        if lexer_list[0][1] == "minus":
            zero_list = [0, "num"]
            lexer_list.insert(0, zero_list)
            return parseEx(lexer_list, 0)

        p2_precedence = precedence_dict[lexer_list[1][1]]  # current operator priority value
        op_boolean = p2_precedence > 0  # is there a current operator

        if op_boolean and p1_precedence >= p2_precedence:  # if there is an operation and last op is more important
            temp = TreeNode(lexer_list[0])
            lexer_list.pop(0)
            return temp  # return the rest of the op as the right tree

        if type(lexer_list[0]) is TreeNode:  # if first element in list is an operator
            left_tree = op  # left tree is now previous package
            lexer_list.pop(0)
        else:
            left_tree = TreeNode(lexer_list[0])  # otherwise continue making first elem left tree
            lexer_list.pop(0)
        op = TreeNode(lexer_list[0])
        lexer_list.pop(0)
        right_tree = parseEx(lexer_list, p2_precedence)

        op.left = left_tree
        op.right = right_tree
        if lexer_list:
            object_list = [op, "tree"]
            lexer_list.insert(0, object_list)
    return op


def evaluate(rootnode):
    if not rootnode:
        return 0  # Return 0 if the rootnode is None

    if rootnode.token == "num":
        return float(rootnode.value)

    left_value = evaluate(rootnode.left) if rootnode.left else 0
    right_value = evaluate(rootnode.right) if rootnode.right else 0

    if rootnode.token == "plus":
        return left_value + right_value
    if rootnode.token == "minus":
        return left_value - right_value
    if rootnode.token == "mult":
        return left_value * right_value
    if rootnode.token == "div":
        return left_value / right_value
    if rootnode.token == "tree":
        return evaluate(rootnode.value)

    raise ValueError("Invalid token: " + rootnode.token)


while True:
    srcCode = input(">>> ")
    if srcCode == "exit":
        break
    srcList = tokenize(srcCode)
    rootNode = parseEx(srcList, 0)
    result = evaluate(rootNode)
    print("The result is: ", result)
print("Now it is time to exit")
