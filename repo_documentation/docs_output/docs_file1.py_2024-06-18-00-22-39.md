# file1.py

## manage_searches_view

The function of this view is to manage policy searches for authenticated users. This view retrieves a list of policy searches performed by the user, groups them by country and policy, and renders a template with the grouped data.

**Attributes**:

- `context` (`dict`): The context dictionary that contains the search data.
- `data_by_search` (`list`): A list of dictionaries containing information about each policy search.

**Functions**:

- `PolicySearch.objects.filter(account=request.user).order_by('-created_at')`: Filters the PolicySearch objects by account and sorts them in descending order based on created at.
- `static(file_path_excel)`: Returns a static file path Excel.
- `pd.read_csv(file)`: Reads the contents of an Excel file using pandas.

**Called_functions**:

- `parse_content(row['Content'])`: Parses the content of an entry to extract information and source.
- `PolicySearch`: The PolicySearch class is used to filter and retrieve policy searches based on user account.

**Code Description**: This view manages policy searches for authenticated users. It retrieves a list of policy searches performed by the user, groups them by country and policy, and renders a template with the grouped data.

**Note**: The view checks if the user is authenticated before allowing access to manage search views.

**Input Example**:

```
{
    "policy_search_data": [
        {
            "id": 1,
            "name": "Search Policy",
            "object_id": "12345"
        },
        {
            "id": 2,
            "name": "Another Search Policy",
            "object_id": "67890"
        }
    ]
}
```

**Output Example**:

The view renders a template with the grouped data, for example:

```
{
    "data_by_search": [
        {
            "search_name": "Search Policy",
            "search_id": 1,
            "grouped_data_by_policy": {
                "Policy1": [
                    {"country": "Country1", "entries": [...]},
                    {"country": "Country2", "entries": [...] }
                ],
                "Policy2": [
                    {"country": "Country3", "entries": [...]}
                ]
            },
            "grouped_data_by_country": {
                "Country1": [...],
                "Country2": [...]
            }
        }
    ]
}
```