
import ast
import operator

print(" ----CALCULADORA----")
print(" --- Operações Suportadas ---")
print(" ---- Adição = '+' ----")
print(" ---- Subtração = '-' ----")
print(" ---- Multiplicação = '*' ----")
print(" ---- Divisão = '/' ----")
print(" ---- Potência = '**' ----")
print(" ---- Resto da divisão = '%' ----")

operacoes = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}


def calcular(expressao):
    arvore = ast.parse(expressao, mode="eval")

    def avaliar(no):
        if isinstance(no, ast.Expression):
            return avaliar(no.body)

        if isinstance(no, ast.Constant) and type(no.value) in (int, float):
            return no.value

        if isinstance(no, ast.BinOp) and type(no.op) in operacoes:
            esquerda = avaliar(no.left)
            direita = avaliar(no.right)

            if isinstance(no.op, ast.Div) and direita == 0:
                raise ZeroDivisionError(
                    "Não é possível dividir por zero."
                )

            return operacoes[type(no.op)](esquerda, direita)

        if isinstance(no, ast.UnaryOp) and isinstance(
            no.op, (ast.UAdd, ast.USub)
        ):
            valor = avaliar(no.operand)
            return valor if isinstance(no.op, ast.UAdd) else -valor

        raise ValueError("Expressão matemática não permitida.")

    return avaliar(arvore)


while True:
    expressao = input("\nDigite a expressão ou 'sair': ").strip()

    if expressao.lower() == "sair":
        print("Calculadora encerrada!")
        break

    try:
        resultado = calcular(expressao)
        print("Resultado:", resultado)

    except ZeroDivisionError as erro:
        print("Erro:", erro)

    except (ValueError, SyntaxError, OverflowError) as erro:
        print("Expressão inválida:", erro)

    except ArithmeticError:
        print("Erro matemático: não foi possível realizar o cálculo.")
