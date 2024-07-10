# Starburst Python Client

Typed interaction with [Starburst Enterprise API](https://docs.starburst.io/latest/api/index.html).

## Usage

Install the package from PyPi

```bash
pip install starburst-client
```

Start using the API client:

```python
from starburst_client import Starburst
from starburst_client.auth import BasicAuth


auth = BasicAuth("username", "password")

s = Starburst(base_url="https://{hostname}/api/v1", auth=auth)

# Create a role
role = s.create_role("hr")

# Update role description
role.description = "HR department users"

# Assign role to a user
role.create_user_assignment("alice")

user = s.get_user("alice")
for assignment in user.get_role_assignments():
    print(f"{user} has {assignment.get_role().name} role")  # alice has hr role
    assignment.delete()

role.delete()
```

Error handling:

```python
from starburst_client.exceptions import ConflictError, BadRequestError

role = s.create_role("test_role")

try:
    s.create_role("test_role")
except ConflictError:
    print("role already exists")


try:
    s.create_role("test-role")
except BadRequestError as e:
    # Invalid value for argument: name: may contain only lowercase latin characters ...
    print(e.message)
```

## License

Released under [the Apache License 2.0](LICENSE).
