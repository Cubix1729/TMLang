from pygments.lexer import RegexLexer
from pygments.token import *

class TMLangLexer(RegexLexer):

    tokens = {
        "root": [
            (r"//.*", Comment),
            (r"\s+", Whitespace),
            (r",", Punctuation),
            (r":", Punctuation),
            (r"{", Punctuation),
            (r"}", Punctuation),
            (r"name ", Keyword.Declaration),
            (r"blank ", Keyword.Declaration),
            (r"initial ", Keyword.Declaration),
            (r"final ", Keyword.Declaration),
            (r"startprogr", Keyword.Declaration),
            (r"endprogr", Keyword.Declaration),
            (r"#run", Name.Builtin),
            (r"#runsteps ", Name.Builtin),
            (r"#renderdiagram", Name.Builtin),
            (r"#printdef", Name.Builtin),
        ]
    }