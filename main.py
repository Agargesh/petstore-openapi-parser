from mcp.server.fastmcp import FastMCP
from typing import List, Union

server = FastMCP(
    name="Petstore MCP Server",
    instructions="Tools that mirror Swagger Petstore operations (stubbed for now)."
)


@server.tool()
async def update_Pet(pet: dict) -> dict:
    """
    Update an existing pet by Id.
    Path: PUT /pet, operationId: updatePet

    Parameters:
      pet (dict): Pet object (must include 'id', 'name', 'photoUrls').
                  Optional fields per spec: 'category', 'tags', 'status'

    Returns:
      dict: Stubbed successful response echoing the pet payload.
    """
    # minimal validation to match the spec's required fields
    required = ["id", "name", "photoUrls"]
    missing = [k for k in required if k not in pet]
    if missing:
        return {"error": f"Missing required fields: {', '.join(missing)}"}

    return {
        "status": 200,
        "operationId": "updatePet",
        "method": "PUT",
        "path": "/pet",
        "contentType": "application/json",
        "pet": pet
    }


@server.tool()
async def add_Pet(pet: dict) -> dict:
    """
    Add a new pet to the store.
    Parameters:
        pet (dict): Pet object containing at least 'name' and 'photoUrls'.
    """
    required_fields = ["name", "photoUrls"]
    missing_fields = [f for f in required_fields if f not in pet]

    if missing_fields:
        return {
            "error": f"Missing required fields: {', '.join(missing_fields)}",
            "status": 400
        }

    return {
        "message": "Pet added successfully",
        "pet": pet,
        "status": 200
    }


@server.tool()
async def find_Pet_By_Status(status: str = "available")-> dict:
    """
    Finds pets by status. Allowed: available, pending, sold.
    """
    allowed_status = ["available", "pending", "sold"]

    if status not in allowed_status:  # <-- fix here
        return {
            "error": f"Invalid status '{status}'. Must be one of {allowed_status}.",
            "status": 400
        }

    pets = [
        {"id": 1, "name": "Doggo", "status": "available"},
        {"id": 2, "name": "Kitty", "status": "pending"},
        {"id": 3, "name": "Birdy", "status": "sold"},
    ]
    filtered_pets = [p for p in pets if p["status"] == status]
    return {
        "message": f"Found {len(filtered_pets)} pets with status '{status}'.",
        "pets": filtered_pets,
        "status": 200
    }


@server.tool()
async def find_pets_by_tags(tags: Union[str, List[str], None] =  None) -> dict:
    """
        Find pets by tags (OpenAPI: /pet/findByTags GET).
        'tags' can be a comma-separated string or a list of strings.
        """
    try:
        if tags is None or (isinstance(tags, str) and not tags.strip()):
            return {"error": "Provide at least one tag (e.g., 'tag1,tag2')."}

        if isinstance(tags, str):
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        else:
            tag_list = [str(t).strip() for t in tags if str(t).strip()]

        return {
            "operationId": "findPetsByTags",
            "request": {"tags": tag_list},
            "result": [
                {"id": 101, "name": "doggie", "tags": tag_list[:1] or ["tag1"]},
                {"id": 202, "name": "mittens", "tags": tag_list[:1] or ["tag1"]},
            ],
        }

    except Exception as e:
        return {"error": str(e)}


@server.tool()
async def get_pet_by_id(petId: int) -> dict:
    """
    Returns a single pet by ID.
    Path: /pet/{petId}
    Method: GET
    Description: Returns a single pet.
    Parameters:
        petId (path) - integer, required: ID of pet to return
    """
    try:
        # Simulated responses based on spec
        if petId <= 0:
            return {"code": 400, "description": "Invalid ID supplied"}
        elif petId == 9999:
            return {"code": 404, "description": "Pet not found"}
        else:
            return {
                "code": 200,
                "description": f"Pet data for ID {petId}",
                "content_types": ["application/json", "application/xml"]
            }
    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def update_pet_with_form(petId: int, name: str = None, status: str = None) -> dict:
    """
    Update a pet resource based on form data.
    Path: POST /pet/{petId}

    Parameters:
        petId (int, required): ID of the pet to be updated.
        name (str, optional): New name for the pet.
        status (str, optional): New status for the pet.

    Returns:
        dict: Simulated response indicating the update result.
    """
    try:
        # Validate required path parameter
        if petId <= 0:
            return {"code": 400, "description": "Invalid ID supplied"}

        # Stubbed logic: just echo back what was sent
        update_fields = {}
        if name:
            update_fields["name"] = name
        if status:
            update_fields["status"] = status

        if not update_fields:
            return {
                "code": 400,
                "description": "No update fields provided (name or status required)."
            }

        return {
            "code": 200,
            "description": f"Pet {petId} updated successfully.",
            "updated_fields": update_fields,
            "content_types": ["application/json", "application/xml"]
        }
    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def deletePet(petId: int) -> dict:
    """
    Deletes a pet by ID.
    Path: DELETE /pet/{petId}, operationId: deletePet

    Parameters:
        petId (int): ID of the pet to delete.

    Returns:
        dict: Stubbed response confirming deletion or error.
    """
    try:
        if petId <= 0:
            return {
                "status": 400,
                "message": "Invalid ID supplied"
            }
        elif petId == 9999:
            return {
                "status": 404,
                "message": f"Pet with ID {petId} not found"
            }
        else:
            return {
                "status": 200,
                "message": f"Pet with ID {petId} deleted successfully"
            }
    except Exception as e:
        return {
            "status": 500,
            "message": "Unexpected error occurred",
            "error": str(e)
        }


@server.tool()
async def upload_pet_image(
        petId: int,
        additionalMetadata: str = None,
        image: bytes = None
) -> dict:
    """
    Upload an image for a pet.
    Path: POST /pet/{petId}/uploadImage

    Parameters:
        petId (int): ID of pet to update (required, path parameter).
        additionalMetadata (str, optional): Additional metadata about the image.
        image (bytes, optional): Binary image data (stubbed here as raw bytes).

    Returns:
        dict: Stubbed response echoing parameters.
    """
    # Validate petId
    if petId <= 0:
        return {"code": 400, "description": "Invalid ID supplied"}

    # uploading the image
    response = {
        "code": 200,
        "description": f"Image uploaded for pet {petId}",
        "metadata": additionalMetadata or "None provided",
        "imageSize": len(image) if image else 0
    }

    # Simulate errors
    if petId == 9999:
        return {"code": 404, "description": "Pet not found"}

    return response


@server.tool()
async def getInventory() -> dict:
    """
        Returns pet inventories by status.
        Path: GET /store/inventory
        OperationId: getInventory

        Description:
            Returns a map of status codes to quantities.

        Parameters:

        Returns:
            dict: Stubbed response mapping pet statuses to inventory counts.
        """
    try:
        inventory = {
            "available": 12,
            "pending": 5,
            "sold": 7
        }

        return {
            "code": 200,
            "description": "Inventory counts retrieved successfully.",
            "inventory": inventory,
            "content_type": "application/json"
        }
    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected Error",
            "error": str(e)
        }

@server.tool()
async def placeOrder(order: dict)-> dict:
    """
        Place a new order in the store.
        Path: POST /store/order
        OperationId: placeOrder

        Description:
            Places an order for a pet in the store.

        Parameters:
            order (dict): Order object containing at least 'id', 'petId', and 'quantity'.
                          Optional fields: 'shipDate', 'status', 'complete'

        Returns:
            dict: Stubbed response echoing the order payload with status code.
        """
    required_fields = ["id", "petId", "quantity"]
    missing_fields = [f for f in required_fields if f not in order]

    if missing_fields:
        return {
        "error": f"Missing required fields: {', '.join(missing_fields)}",
        "status": 400
        }

    return {
        "status": 200,
        "message": "Order placed successfully",
        "order": order,
        "content_type": "application/json"
    }


@server.tool()
async def get_order_by_Id(orderId: int) -> dict:
    """
        Find purchase order by ID.
        Path: GET /store/order/{orderId}
        OperationId: getOrderById

        Description:
            For valid response try integer IDs with value <= 5 or > 10.
            Other values will generate exceptions.

        Parameters:
            orderId (int): ID of order that needs to be fetched (required).

        Returns:
            dict: Stubbed response containing order details or error message.
        """
    try:
        if orderId <= 0:
            return {"code": 400, "description": "Invalid ID supplied"}
        elif 6 <= orderId <= 10:
            return {"code": 404, "description": "Order not found"}
        else:
            return {
                "code": 200,
                "description": f"Order data for ID {orderId}",
                "order": {
                    "id": orderId,
                    "petId": 123,
                    "quantity": 2,
                    "status": "approved",
                    "complete": False
                },
                "content_types": ["application/json", "application/xml"]
            }
    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def deleteOrder(orderId: int) -> dict:
    """
        Delete purchase order by ID.
        Path: DELETE /store/order/{orderId}
        OperationId: deleteOrder

        Description:
            For valid response try integer IDs with value < 1000.
            Anything above 1000 or non-integers will generate API errors.

        Parameters:
            orderId (int): ID of the order that needs to be deleted (required).

        Returns:
            dict: Stubbed response confirming deletion or error message.
        """
    try:
        if orderId <= 0:
            return {"code": 400, "description": "Invalid ID supplied"}
        elif orderId > 1000:
            return {"code": 404, "description": f"Order {orderId} not found"}
        else:
            return {
                "code": 200,
                "description": f"Order {orderId} deleted successfully",
                "status": "deleted"
            }

    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def createUser(user: dict) -> dict:
    """
        Create a new user.
        Path: POST /user
        OperationId: createUser

        Description:
            This can only be done by the logged in user.

        Parameters:
            user (dict): User object containing at least 'id', 'username', and 'password'.
                         Optional fields: 'firstName', 'lastName', 'email', 'phone', 'userStatus'

        Returns:
            dict: Stubbed response echoing the created user with status code.
        """
    required_fields = ["id", "username", "password"]
    missing_fields = [f for f in required_fields if f not in user]

    if missing_fields:
        return {
            "error": f"Missing required fields: {', '.join(missing_fields)}",
            "status": 400
        }

    return {
        "status": 200,
        "message": "User created successfully",
        "user": user,
        "content_types": ["application/json", "application/xml"]
    }


@server.tool()
async def create_users_with_list_input(users: list) -> dict:
    """
        Creates list of users with given input array.
        Path: POST /user/createWithList
        OperationId: createUsersWithListInput

        Description:
            Creates multiple users with the provided list.

        Parameters:
            users (list): List of user objects. Each user should contain at least
                          'id', 'username', and 'password'.
                          Optional fields: 'firstName', 'lastName', 'email',
                          'phone', 'userStatus'

        Returns:
            dict: Stubbed response echoing the list of created users.
        """
    if not users or not isinstance(users, list):
        return {"error": "Users list is required", "status": 400}

        # Check that each user has the required fields
    required_fields = ["id", "username", "password"]
    invalid_users = [
        u for u in users if not all(field in u for field in required_fields)
    ]

    if invalid_users:
        return {
            "error": "One or more users missing required fields (id, username, password)",
            "status": 400
        }

    return {
        "status": 200,
        "message": f"{len(users)} users created successfully",
        "users": users,
        "content_types": ["application/json", "application/xml"]
    }


@server.tool()
async def loginUser(username: str = None, password: str = None) -> dict:
    """
        Log into the system.
        Path: GET /user/login
        OperationId: loginUser

        Description:
            Logs a user into the system with username and password.

        Parameters:
            username (str, optional): The username for login.
            password (str, optional): The password for login in clear text.

        Returns:
            dict: Stubbed login response with a session token or error message.
        """
    try:
        # Validate input
        if not username or not password:
            return {"code": 400, "description": "Username and password are required"}

        # Stubbed success response
        return {
            "code": 200,
            "description": "Login successful",
            "username": username,
            "token": f"session-{username}-12345",
            "content_types": ["application/json", "application/xml"]
        }
    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def logoutUser() -> dict:
    """
        Log user out of the system.
        Path: GET /user/logout
        OperationId: logoutUser

        Description:
            Logs the current user out of the system.

        Parameters:
            None

        Returns:
            dict: Stubbed response confirming logout.
        """
    try:
        # Stubbed logout success response
        return {
            "code": 200,
            "description": "User logged out successfully",
            "status": "logged_out"
        }
    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def get_user_by_name(username: str) ->dict:
    """
        Get user detail based on username.
        Path: GET /user/{username}
        OperationId: getUserByName

        Description:
            Retrieves a user's details by their username.

        Parameters:
            username (str): The name of the user to be fetched (required).

        Returns:
            dict: Stubbed response with user details or error message.
        """
    try:
        if not username or username.strip() == "":
            return {"code": 400, "description": "Invalid username supplied"}
        elif username == "unknown":
            return {"code": 404, "description": f"User '{username}' not found"}
        else:
            return {
                "code": 200,
                "description": f"User data for {username}",
                "user": {
                    "id": 1,
                    "username": username,
                    "firstName": "John",
                    "lastName": "Doe",
                    "email": f"{username}@example.com",
                    "phone": "123-456-7890",
                    "userStatus": 1
                },
                "content_types": ["application/json", "application/xml"]
            }

    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }

@server.tool()
async def updateUser(username: str, user: dict) -> dict:
    """
        Update user resource.
        Path: PUT /user/{username}
        OperationId: updateUser

        Description:
            This can only be done by the logged in user.

        Parameters:
            username (str): The username (path parameter) of the user to update. (required)
            user (dict):    User object payload to update the resource with.
                            Optional fields per spec: id, firstName, lastName, email,
                            password, phone, userStatus, etc.

        Returns:
            dict: Stubbed response indicating update result or error.
        """
    try:
        if not username or username.strip == "":
            return {"code": 400, "description": "Invalid username supplied"}

        if username == "unknown":
            return {"code": 404, "description": f"User '{username}' not found"}

        if not isinstance(user, dict) or len(user) == 0:
            return {"code": 400, "description": "Request body is required with at least one field"}

        # Stubbed success response (echo the payload)
        return {
            "code": 200,
            "description": f"User '{username}' updated successfully",
            "username": username,
            "updated_user": user
        }

    except Exception as e:
        return {
            "code": "default",
            "description": "Unexpected error",
            "error": str(e)
        }


@server.tool()
async def deleteUser(username: str) -> dict:
    """
        Delete user resource.
        Path: DELETE /user/{username}
        OperationId: deleteUser

        Description:
            This can only be done by the logged inuser.

        Parameters:
            username (str): The username (path parameter) of the user to delete. (required)

        Returns:
            dict: Stubbed response confirming deletion or error.
        """
    try:
        if not username or username.strip() == "":
            return {"code": 400, "description": "Invalid username supplied"}

        if username == "unknown":
            return {"code": 404, "description": f"User '{username}' not found"}

        return {
            "code": 200,
            "description": f"User '{username}' deleted successfully",
            "status": "deleted"
        }

    except Exception as e:
        return {
            "code": "default",
            "descrption": "unexpected error",
            "error": str(e)
        }


if __name__ == "__main__":
    print("Starting MCP server...")
    server.run(transport="sse")
