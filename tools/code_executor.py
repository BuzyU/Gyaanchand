# tools/code_executor.py

def execute_code(code_str: str, input_data: str = ""):
    try:
        # Redirect input() if needed
        import io
        import sys
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        sys.stdout = io.StringIO()
        sys.stdin = io.StringIO(input_data)

        # Execute code
        exec_globals = {}
        exec(code_str, exec_globals)

        # Get output
        output = sys.stdout.getvalue()

        # Restore std
        sys.stdout = old_stdout
        sys.stdin = old_stdin

        return output.strip()

    except Exception as e:
        return f"Error during execution: {e}"
