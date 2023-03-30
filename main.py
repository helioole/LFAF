from lexer.lexer import Lexer

correct = '''
function gcd(a, b) {
    if b == 0{
        return a;
    else {
        return gcd(b, a % b);
    }
    }
    }

 '''

lexer = Lexer()
output1 = lexer.tokenize(correct)
for token in output1:
    print(token)

wrong1 = '''
function gcd(a, b) {
    if b! == 0{
        return a;
    else {
        return gcd(b, a % b);
    }
    }

 '''

output2 = lexer.tokenize(wrong1)
for token in output2:
    print(token)

wrong2 = '''
function gcd(a, b) {
    if b == 0{
        return a;
    else {
        return gcd(b, a # b);
    }
    }
    }
'''

output3 = lexer.tokenize(wrong2)
for token in output3:
    print(token)

