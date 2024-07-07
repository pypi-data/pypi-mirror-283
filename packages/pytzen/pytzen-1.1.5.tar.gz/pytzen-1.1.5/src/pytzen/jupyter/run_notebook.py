import nbformat
from nbclient import NotebookClient

def run_notebook(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
        client = NotebookClient(nb, timeout=600)
        client.execute()

if __name__ == "__main__":
    import sys
    run_notebook(sys.argv[1])
