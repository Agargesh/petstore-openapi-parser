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

        operation_id = details.get("operationId", "(no operationId)")

        if "description" in details:
            print(f"{sub_indent}|- Description: {details['description']}")

        if "parameters" in details:
            print(f"{sub_indent}|- Parameters:")
            for parameter in details["parameters"]:
                name = parameter.get("name", "(no name)")
                param_in = parameter.get("in", "(no location)")
                required = parameter.get("required", False)
                schema = parameter.get("schema", {})
                param_type = schema.get("type", "(no type)")
                enum = schema.get("enum", None)
                default = schema.get("default", None)
                desc = parameter.get("description", "(no description)")

                print(f"{sub_indent}   |- {name} ({param_in})")
                print(f"{sub_indent}      |- Type: {param_type}")
                print(f"{sub_indent}      |- Required: {required}")
                print(f"{sub_indent}      |- Description: {desc}")

                if enum:
                    print(f"{sub_indent}      |- Enum: {enum}")
                if default is not None:
                    print(f"{sub_indent}      |- Default: {default}")

        if "requestBody" in details:
            req_body = details["requestBody"]
            desc = req_body.get("description", "(no description)")
            print(f"{sub_indent}|- Request Body: {desc}")
            content = req_body.get("content", {})
            for content_type in content.keys():
                print(f"{sub_indent}   |-- Content-type: {content_type}")

        if "responses" in details:
            print(f"{sub_indent}|- Responses:")
            for code, response in details["responses"].items():
                print(f"{sub_indent}  |-- {code}:")
                content = response.get("content", {})
                for content_type in content.keys():
                    print(f"{sub_indent}     |- Content-type: {content_type}")
