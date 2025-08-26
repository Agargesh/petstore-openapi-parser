Petstore MCP Server

This project implements the Swagger Petstore OpenAPI 3.0 specification as an MCP (Model Context Protocol) server in Python. It demonstrates how REST API endpoints can be mirrored into MCP tools that can be called by large language models (LLMs) like Anthropic’s Claude.

Features

- Parses Petstore OpenAPI spec using the prance
 library.

- Implements 19 MCP tools in Python, covering all Petstore endpoints:

      - Pet operations (add, update, delete, find, upload image)

      - Store operations (inventory, place order, get/delete order)

      - User operations (create, login/logout, update, delete)

- Stubbed responses that validate inputs and return structured JSON-like outputs.

- Integration with Anthropic Claude via mcphost, enabling natural language prompts to call tools.

- Includes demo scripts and example prompts for testing.

How It Works

1. The Petstore OpenAPI spec is parsed to list all endpoints, methods, and parameters.

2. Each endpoint is converted into an MCP tool using the FastMCP library.

3. The MCP server runs locally (via SSE transport).

4. Claude (through mcphost) can call tools directly when given natural language prompts like:
       Add a new pet named Fido with photo URL http://example.com/fido.jpg
    
