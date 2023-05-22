import sys

DATABASE_PATH = "clientes.csv"

# La primera posicion es el nombre del script
if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/clientes_test.csv"
