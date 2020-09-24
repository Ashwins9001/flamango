#Token types, EOF indicates no more input for lexical analysis

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token(object):
    def __init__(self, banana, value):
        self.type = banana
        self.value = value

    def __str__(self):
        return 'Token({banana}, {value})'.format(
            banana = self.type,
            value = repr(self.value)
            )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        current_char = text[self.pos]

        if current_char.isdigit():
            token =  Token(INTEGER, int(current_char))
            self.pos = self.pos + 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos = self.pos + 1
            return token

        self.error()

    #Confirm token type and iterate to next 
    def eat(self, token_type):
        print(self.current_token, 'current')
        print(token_type, 'token_type')
        if self.current_token.banana == token_type:
            self.current_token = self.get_next_token()
            

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)
        print('this is left',left)

        op = self.current_token
        self.eat(PLUS)
        print('this is operator',op)

        right = self.current_token
        self.eat(INTEGER)
        print('this is right',right)

        result = left.value + right.value
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
            
