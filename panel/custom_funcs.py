import rstr


def generate_code(symbol_qnt):
    code = ''
    for i in range(symbol_qnt):
        code = code + rstr.xeger(r'([A-Z]|[a-z]|[1-9])')
    return code



