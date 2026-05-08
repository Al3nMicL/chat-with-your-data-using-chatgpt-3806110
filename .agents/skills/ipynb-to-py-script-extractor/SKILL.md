---
name: ipynb-to-py-script-extractor
description: Extracts code from Jupyter Notebooks (.ipynb) into standard Python scripts (.py). Handles skipping dependency installations, adding explicit print statements for implicit cell outputs, and creating a wrapper execution script. Use when asked to convert or extract code from a notebook.
---

# Jupyter to Python Extractor Workflow

This skill outlines the procedure for reliably converting Jupyter Notebooks into standard Python scripts.

## Step-by-Step Instructions

1. **Read and Analyze the Notebook**: 
   - Parse the `.ipynb` file (which is a JSON structure) to extract the source code from cells where `"cell_type" == "code"`.
   - You can use the provided script `scripts/extract.py` to quickly dump the code cells to the terminal, omitting simple installation cells.

2. **Filter Out Installations**:
   - Skip any lines or cells that perform environment installations (e.g., `pip install ...`, `uv pip install ...`). Dependencies should generally be managed via global requirements files.

3. **Add Explicit `print()` Statements**:
   - Jupyter implicitly prints the result of the last line in a cell. Standard Python scripts do not.
   - Identify exploratory outputs and wrap them in `print()` statements.
   - For long lists or large objects, slice them (e.g., `[:5]`) or format the output nicely to prevent flooding the CLI.

4. **Save the Target File**:
   - Save the consolidated code into a new `.py` file with the same base name as the notebook (e.g., `folder/notebook.py`). 
   - Do NOT delete the original `.ipynb` file unless explicitly asked to do so.

5. **Create Execution Wrapper (`main.py`)**:
   - To ensure that relative paths within the scripts resolve correctly, ensure a `main.py` wrapper script exists at the project root. If it doesn't exist, create it using the template found in `assets/main.py.template`.
   - This wrapper uses `runpy` to execute target scripts in their respective local working directories.

6. **Test the Script**:
   - Run the script to verify the extraction using the execution wrapper.
   - Example: `. .venv/bin/activate && python3 main.py <path_to_script.py>`.