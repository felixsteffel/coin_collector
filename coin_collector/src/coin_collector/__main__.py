import typer
from .game import run_game

app = typer.Typer(help="Coin Collector – Einfache 2D-Sammelspiel-Übung")

@app.command()
def play(
    level: str = typer.Option(..., help="Pfad zur Level-JSON"),
    fps: int = 60,
    debug: bool = False,
):
    """Startet das Spiel mit den angegebenen Parametern."""
    run_game(level_path=level, fps=fps, debug=debug)

if __name__ == "__main__":
    app()