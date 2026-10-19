class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for token in tokens:
            if token in "+-*/":
                a = stack.pop()
                b = stack.pop()
                match token:
                    case '+': stack.append(b + a)
                    case '-': stack.append(b - a)
                    case '*': stack.append(b * a)
                    case '/': stack.append(int(b / a))
            else:
                stack.append(int(token))
        return stack[0]