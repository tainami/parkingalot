import click
from werkzeug.security import generate_password_hash

from app import db
from app.models.guarda import Guarda


def register_cli(app):
    @app.cli.command("criar-guarda")
    @click.option("--cpf", prompt=True)
    @click.option("--nome", prompt=True)
    @click.option("--turno", prompt=True)
    @click.option("--senha", prompt=True, hide_input=True, confirmation_prompt=True)
    def criar_guarda(cpf, nome, turno, senha):
        """Cria o primeiro guarda direto no banco, sem passar pela API."""
        if db.session.get(Guarda, cpf) is not None:
            click.echo("Já existe um guarda com esse CPF.")
            return

        guarda = Guarda(
            cpf_guarda=cpf,
            nome_guarda=nome,
            turno=turno,
            senha=generate_password_hash(senha),
        )
        db.session.add(guarda)
        db.session.commit()

        click.echo(f"Guarda '{nome}' criado com sucesso.")
