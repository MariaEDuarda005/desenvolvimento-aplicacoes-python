# meu_dicionario = {}
# meu_dic = dict()

# alunos = {
#     1: { 
#         "nome": "João", 
#         "idade": 20, 
#         "curso": "Engenharia"
#     },
#     2: { 
#         "nome": "Maria", 
#         "idade": 22, 
#         "curso": "Medicina"
#     },
#     3: { 
#         "nome": "Pedro", 
#         "idade": 19, 
#         "curso": "Direito"
#     },
#     4: { 
#         "nome": "Carol", 
#         "idade": 21, 
#         "curso": "Enfermagem"
#     }
# }

# alunos[3]["nome"] = "Carlos"
# print(alunos)
# print(alunos[2]["nome"])

# for id, nome in alunos.items():
#     print(f"ID: {id}")
#     print(f"Nome: {nome['nome']}")
#     print("-" * 20)

# num_alunos = int(input("Quantos alunos vai ter na sua sala: "))
# alunos = {}

# for i in range(num_alunos):
#     print("Adicionando o aluno", i + 1)
#     nome = input("Digite o nome do aluno: ")
#     idade = int(input("Digite a idade do aluno: "))
#     curso = input("Digite o curso do aluno: ")

#     alunos[i] = {
#         "nome": nome,
#         "idade": idade,
#         "curso": curso
#     }

# print(alunos)

# ------------------------------------------------------------------- #

# i = range(5) # Quando coloca só um numero ele entende que começa no 0 e vai até o numero -1. Por exemplo vai de 0 a 4.

# for x in i:
#     print(x+1)

for m in range(2,15, 5):
    print(m) # 2,17,32,47... (começa no 2 e vai somando 15 a cada iteração)

print("-----------------")
for i in range(2,5):
    print(i) # 2,3,4

tupla = ("pera", "uva", "maça")
for fruta in range(len(tupla)):
    lista_formatada = [item.capitalize() for item in tupla]
    print(f"Indice: {fruta} - Fruta: {lista_formatada[fruta]}")


pares = [x for x in range(10) if (x % 2 ==0)]
print(pares)

idade = int(input("Digite sua idade:"))

if idade <= 18:
    print("Você é menor de idade")
else:
    print("Você é maior de idade")

senha_protegida = "senha123"

senha = str(input("Digite sua senha: "))

if senha == senha_protegida:
    print("Acesso permitido")
else:
    print("Acesso negado")
