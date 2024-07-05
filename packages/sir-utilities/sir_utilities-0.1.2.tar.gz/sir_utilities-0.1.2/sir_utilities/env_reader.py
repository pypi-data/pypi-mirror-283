from dotenv import load_dotenv
import os


def get_env_variable(variable: str, group: str | None = None) -> str:
    load_dotenv()
    if group:
        grouped_variable = f"{variable}_{group}"
        if result := os.getenv(grouped_variable):
            return result
        else:
            raise NameError(f"Variable {grouped_variable} not found.")

    elif result := os.getenv(variable):
        return result
    else:
        raise NameError(f"Variable {variable} not found.")
