# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'
)


class Token(object):
    def __init__(self, datatype, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.datatype = datatype
        # token value: non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({datatype}, {value})'.format(
            datatype=self.datatype,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

class AST(object):
    pass

#Define structure nodes of type: BinOp
#AST will contain BinOp nodes and INTEGER nodes that are used for evaluation
#BinOp nodes adopt existing nodes as left children and new term or factor as right
#Term & factor refers to production rules defined in grammar
#Construction of AST thus gives higher precedence to lower nodes!
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        #Retrieve tokens from lexer that assigns tokens & ignores whitespace
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    #Compare current with passed token to ensure structure of sentence correct
    #Iterate to following token
    def eat(self, token_type):
        if self.current_token.datatype == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    #lowest, most essential level of grammar
    def factor(self):
        token = self.current_token
        if token.datatype == INTEGER:
            self.eat(INTEGER)
            return Num(token)

    def term(self):
        node = self.factor()
        while self.current_token.datatype in (MUL, DIV):
            token = self.current_token
            if token.datatype == MUL:
                self.eat(MUL)
            elif token.datatype == DIV:
                self.eat(DIV)

            node = BinOp(left = node, op = token, right = self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.datatype in (PLUS, MINUS):
            token = self.current_token
            if token.datatype == PLUS:
                self.eat(PLUS)
            elif token.datatype == MINUS:
                self.eat(MINUS)
            node = BinOp(left = node, op = token, right = self.term())

        return node

    def parse(self):
        return self.expr()

#BinOp and Num are seperate classes, prod sep objects
#Thus type(node) identifies correct class & derives method name from that !
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

#NodeVisitor objects get passed to interpreter from visit() method
#Map methods to node's datatype and visit recursively using post-order
#Traversal to ensure operands evaluated before operator and
#Precedence for lower nodes is followed 
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.datatype == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.datatype == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.datatype == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.datatype == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
    
def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()
