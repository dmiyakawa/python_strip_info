# Note regarding the INDENT token: The tokenize module does
# not label indentation inside of an operator (parens,
# brackets, and curly braces) as actual indentation.


def foo():
    "The spaces before this docstring are tokenize.INDENT"
    test = [
        "The spaces before this string do not get a token"
    ]
    print(test)


foo()
