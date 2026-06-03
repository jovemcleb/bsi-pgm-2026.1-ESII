# main.py: interface CLI do sistema.
from repositories import RepositorioEmprestimo
from services import Notificador, ServicoEmprestimo


def main():
	repositorio = RepositorioEmprestimo()
	notificador = Notificador()
	servico = ServicoEmprestimo(repositorio, notificador)

	while True:
		print("\n1-Registrar  2-Devolver  3-Atrasados  0-Sair")
		op = input("Opção: ")
		if op == "1":
			registrado = servico.registrar(
				int(input("ID equipamento: ")),
				input("Nome: "),
				input("Email: "),
				int(input("Dias: ")),
			)
			if not registrado:
				print("Equipamento inválido ou indisponível")
		elif op == "2":
			multa = servico.devolver(int(input("ID empréstimo: ")))
			if multa is None:
				print("Empréstimo inválido ou já devolvido")
			else:
				print(f"Devolução registrada. Multa: R${multa:.2f}")
		elif op == "3":
			atrasados = servico.listar_atrasados()
			for atraso in atrasados:
				print(f"{atraso.emprestimo.usuario_nome} — {atraso.dias_atraso} dias — R${atraso.multa:.2f}")
		elif op == "0":
			break


if __name__ == "__main__":
	main()
