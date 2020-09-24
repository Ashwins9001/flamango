#Token types, EOF indicates no more input for lexical analysis

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, datatype, value):
        self.datatype = datatype
        self.value = value

    def __str__(self):
        return 'Token({datatype}, {value})'.format(
            datatype = self.datatype,
            value = repr(self.value)
            )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    #if input exists and is whitespace: skip
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char #concat digit & adv
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            #detect digit, call integer() to find string of digits & concat
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance() #continue if +
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()
        #if EOF then parsing complete 
        return Token(EOF, None)

    #Confirm token type and iterate to next 
    def eat(self, token_type):
        print(self.current_token, 'current')
        print(token_type, 'token_type')
        if self.current_token.datatype == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
            

    def expr(self):
        #get one token at a time 
        self.current_token = self.get_next_token() 
        left = self.current_token
        self.eat(INTEGER)
        print('this is left',left)

        op = self.current_token
        if op.datatype == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)
        print('this is operator',op)

        right = self.current_token
        self.eat(INTEGER)
        print('this is right',right)

        if op.datatype == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
            
