#-------------------------------------------------------------------------------
# Name:        lexhtml
# Purpose:
#
# Author:      TRINITI
#
# Created:     22-07-2014
# Copyright:   (c) TRINITI 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import ply.lex as lex
    #import re
tokens=('LANGLE','LANGLESLASH','RANGLE','SLASHRANGLE',
            'EQUAL',
            'STRING','WORD','NUMBER',
            'JAVASCRIPT',)


states = (   ('htmlcomment', 'exclusive') ,  # <-- HTML COMMENTS  -->
                        ('javascript','exclusive'),  ) # JAVASCRIPT <script>.....

t_ignore = ' \t\v\r'  # whitespace

def t_javascript(token):
    r'\<script\ type=\"text\/javascript\"\>'
    token.lexer.code_start=token.lexer.lexpos
    token.lexer.begin("javascript")

def t_javascript_end(token):
    r'\<\/script\>'
    token.value=token.lexer.lexdata[token.lexer.code_start:token.lexer.lexpos-9]
    token.type='JAVASCRIPT'
    token.lexer.lineno+=token.value.count('\n')
    token.lexer.begin('INITIAL')
    return token

def t_javascript_error(token):
    token.lexer.skip(1)

def t_htmlcomment(token):
    r'<!--'
    token.lexer.begin('htmlcomment')

def t_htmlcomment_newline(token):
    r'\n'
    token.lexer.lineno += 1

def t_htmlcomment_end(token):
    r'-->'
    token.lexer.lineno += token.value.count('\n')#there is bug in this code thats why i added another function above to count newlines
    token.lexer.begin('INITIAL')

def t_htmlcomment_error(token):
    token.lexer.skip(1)

def t_newline(token):
    r'\n'
    token.lexer.lineno +=1
    pass

def t_comment(token):
    r'/<--(.|\n)*?\-->'
    token.lexer.lineno += token.value.count('\n')


t_htmlcomment_ignore    = ' \t\v\r'
t_javascript_ignore     = ' \t\v\r'


t_LANGLESLASH= r'</'
t_LANGLE= r'<'
t_RANGLE= r'>'
t_SLASHRANGLE= 'r/>'
t_EQUAL= r'='


def t_STRING(token):
    r'(?:"[^"]*"|\'[^\']*\')'
    token.value = token.value[1:-1] # concat the ' or " around string
    return token

def t_WORD(token):
    r'[^<>\n=]+'
    return token


def t_error(t):
        print "HTML Lexer: Illegal character " + t.value[0]
        t.lexer.skip(1)


webpage="""this is
                                                     <b> my<!---
    Nishant Oli---> </b>webpage!<script type="text/javascript"> int + * =
                                                     //nishant
                                                     goli </script>
                                                      hi"""
htmllexer=lex.lex()
htmllexer.input(webpage)
while True:
    tok=htmllexer.token()
    if not tok:
        break
    print tok

