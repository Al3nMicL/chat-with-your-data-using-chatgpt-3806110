import sys
import os
import runpy
from pathlib import Path


def main():
    """
    Load and execute a Python script with automatic working directory management.
    
    Usage: python main.py <script_path>
    
    This function:
    1. Takes a script path as a command-line argument
    2. Extracts the directory containing the script
    3. Changes the current working directory to that directory
    4. Executes the script from that directory
    
    This allows scripts using relative paths to work correctly without modification.
    """
    
    # Check if an argument was provided
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py <script_path>")
            print("Example: python main.py 01_03/01_03.py")
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        sys.exit(1)
    
    script_path = sys.argv[1]
    
    # Validate that the script file exists
    try:
        script_file = Path(script_path)
        if not script_file.exists():
            print(f"Error: Script file '{script_path}' does not exist")
            sys.exit(1)
        
        if not script_file.is_file():
            print(f"Error: '{script_path}' is not a file")
            sys.exit(1)
    except Exception as e:
        print(f"Error validating script path: {e}")
        sys.exit(1)
    
    # Get the absolute path and directory of the script
    try:
        script_abs_path = script_file.resolve()
        script_directory = script_abs_path.parent
    except Exception as e:
        print(f"Error resolving script path: {e}")
        sys.exit(1)
    
    # Save the original working directory for reference
    original_cwd = Path.cwd()
    
    # Change to the script's directory
    try:
        os.chdir(script_directory)
        print(f"Changed working directory to: {script_directory}")
    except Exception as e:
        print(f"Error changing working directory: {e}")
        sys.exit(1)
    
    # Execute the script
    try:
        runpy.run_path(str(script_abs_path), run_name="__main__")
    except FileNotFoundError as e:
        print(f"Error: Script file not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing script: {e}")
        sys.exit(1)
    finally:
        # Optionally restore the original working directory (for REPL environments)
        try:
            os.chdir(original_cwd)
        except Exception as e:
            print(f"Warning: Could not restore original directory: {e}")


if __name__ == "__main__":
    main()
