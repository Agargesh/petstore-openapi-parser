from prance import ResolvingParser

parser = ResolvingParser("specs/petstore.yaml")

print("spec loaded successfully")
specs = parser.specification

print("\nEndpoints in the Petstore API:\n")

for path, methods in specs["paths"].items():
    print(f"Path: {path}")
    for method in methods:
        print(f"  - Method: {method.upper()}")
