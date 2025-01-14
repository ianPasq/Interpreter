INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)

class Token(object):
    def __init__(self, type, value):
        self.type= type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type = self.type, value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
        while (
            self.current_char is not None and
            self.current_char.isdigit()
        ):
            result += self.current_char
            self.advance()
            token = Token('REAL_CONST', float(result))
        else:
            token = Token('INTEGER_CONST', int(result))
        return token

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]
            RESERVED_KEYWORDS = {
            'PROGRAM': Token('PROGRAM', 'PROGRAM'),
            'VAR': Token('VAR', 'VAR'),
            'DIV': Token('INTEGER_DIV', 'DIV'),
            'INTEGER': Token('INTEGER', 'INTEGER'),
            'REAL': Token('REAL', 'REAL'),
            'BEGIN': Token('BEGIN', 'BEGIN'),
            'END': Token('END', 'END'),
            }
    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
            token = RESERVED_KEYWORDS.get(result, Token(ID, result))
            return token
        def get_next_token(self):
            while self.current_char is not None:
                if self.current_char.isalpha():
                    return self._id()
                if self.current_char == '{':
                    self.advance()
                    self.skip_comment()
                continue
            if self.current_char == ':' and self.peek() == '=':

                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')
            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')
            if self.current_char.isdigit():
                return self.number()
            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            if self.current_char.isspace():
                self.skip_whitespace()
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
                return Token(FLOAT_DIV, '/')
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            self.error()

        return Token(EOF, None)

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block  

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Compound(AST):    
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass
