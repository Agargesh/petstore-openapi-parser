from prance import ResolvingParser

parser = ResolvingParser("specs/petstore.yaml")
specs = parser.specification

print("spec loaded successfully")

for path, methods in specs["paths"].items():
    print(f"\n Path: {path}")

    for method, details in methods.items():
        method_indent = "  |--"
        sub_indent = "  |   "
        print(f"{method_indent} Method: {method.upper()}")

        operation_id = details.get("operationId")
        if operation_id:
            print(f"{sub_indent}|- Operation ID: {operation_id}")

        request_body = details.get("requestBody")
        if request_body:
            print(f"{sub_indent}|- Request Body: {request_body.get('description', '(no description)')}")
            content = request_body.get("content", {})
            for content_type in content:
                print(f"{sub_indent}   |-- Content-type: {content_type}")

        responses = details.get("responses", {})
        if responses:
            print(f"{sub_indent}|- Responses:")
            for status_code, response in responses.items():
                desc = responses.get("description", "")
                print(f"{sub_indent}  |-- {status_code}: {desc}")
                content = response.get("content", {})
                for content_type in content:
                    print(f"{sub_indent}     |- Content-type: {content_type}")
