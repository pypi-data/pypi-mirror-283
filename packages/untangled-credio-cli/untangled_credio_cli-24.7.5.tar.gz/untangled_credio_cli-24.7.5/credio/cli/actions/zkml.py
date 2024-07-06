import subprocess
import typer


action = typer.Typer()


@action.command(name="compile", help="Convert an ML model to a ZKML model.")
def compile_circuit(
    model: str = "network.onnx",
    circuit: str = "model.compiled",
    settings: str = "settings.json",
):
    subprocess.run(
        [
            "ezkl",
            "compile-circuit",
            "--model",
            model,
            "--compiled-circuit",
            circuit,
            "--settings-path",
            settings,
        ]
    )


@action.command(
    name="submit", help="[WIP] Submit a specific ZKML model to Credio platform."
)
def submit_model(circuit: str = "model.compiled", settings: str = "settings.json"):
    raise Exception("Not implemented yet")


@action.command(
    name="serve",
    help="Start serving a specific ML model (tunnelly connect to Credio platform).",
)
def serve(model_id: str, port: int = 8080):
    raise Exception("Not implemented yet")
