DOCUMENTATION_PROMPT = """
You are an AI documentation assistant, and your task is to generate documentation based on the given code of an object.
The purpose of the documentation is to help developers and beginners understand the function and specific usage of the code.
Now you need to generate a document for "{file_name}".

The source code is as follows:
{file_content}
(-Source code ends-)

Please note any part of the content you generate SHOULD NOT CONTAIN Markdown hierarchical heading and divider syntax.

The standard format is as follows (If a section does not have any information, you can skip it and move to the next one):

# {file_name}

## ClassDef NameOfClass

The function of the class is XXX. (Only code name and one sentence function description are required)

**Attributes**:

- `attribute1` (`type`): Description of the first attribute.

**Functions**:

- `function_name1`(`param1`: `type`) -> `return_type`
    - Parameters:
        - `param1` (`type`): Description of the first parameter.
    - Returns:
        - `return_type`: Description of the return value.

**Called_functions**:

- `function1`(`param1`: `type`) -> `return_type`: Description of what function1 does and what function1 returns.

**Code Description**: The description of this class. (Detailed and CERTAIN code analysis and description)

**Note**: Points to note about the use of the code according to the returns

**Input Example**: 

```
Provide an input example for a specified data type (e.g., list, double, int) and include a detailed explanation.
```

**Output Example**:

```
Provide an output example for a specified data type (e.g., list, double, int) and include a detailed explanation.
```


## FunctionDef NameOfFunction (functions that do not belong to a class but are still present in the file)

The function of the function is XXX. (Only code name and one sentence function description are required)

**Parameters**:

- `param1` (`type`): Description of the first parameter.

**Returns**:

- `return_type`: Description of the return value.

**Called_functions**:

- `function1`(`param1`: `type`) -> `return_type`: Description of what function1 does and what function1 returns.

**Code Description**: The description of this function. (Detailed and CERTAIN code analysis and description)

**Note**: Points to note about the use of the code according to the returns

**Input Example**: 

```
Provide an input example for a specified data type (e.g., list, double, int) and include a detailed explanation.
```

**Output Example**: 

```
Provide an output example for a specified data type (e.g., list, double, int) and include a detailed explanation.
```

Please generate a detailed explanation document for this object based on the code of the target object itself. 
For the section Called_functions, considering the callee function information below:
{callee_functions}.
"""

DOCUMENTATION_UPDATE_PROMPT = """You are an AI documentation assistant. Your task is to update the existing documentation based on the provided changes in the code. 

Now you need to update the document for "{file_name}".

**Old Documentation**:
{old_file_docs}

**Old Code Content**:
{old_file_content}

**New Code Content**:
{new_file_content}

**Diff between Old and New Code**:
{diff}

**Changes in the Functions**:
{changes}

Please update the documentation accordingly, ensuring it accurately reflects the changes. Provide a comprehensive and clear description for any modified or new functions/classes.

**Note**: DO NOT CHANGE ANYTHING IN THE OLD DOCUMENTATION THAT HAS NOT BEEN AFFECTED BY THE CODE CHANGES.
"""

USR_PROMPT = """You are a documentation generation assistant for Python programs. Keep in mind that your audience is document readers, so use a deterministic tone to generate precise content and don't let them know you're provided with code snippet and documents. AVOID ANY SPECULATION and inaccurate descriptions! Now, provide the documentation for the target object in a professional way."""


PARENT_UPDATE = """

**The following functions:**
{updated_function_contents}

**In the file below:**
{new_content}

Have been updated. These changes influence the current file on the path: 
{path}

Please make sure to update the following functions in the file accordingly.
{functions}
File content:
{parent_content}
Old documentation:
{old_parent_docs}
••Note:••: DO NOT CHANGE ANYTHING IN THE OLD DOCUMENTATION THAT HAS NOT BEEN AFFECTED BY THE CODE CHANGES.

"""

COMENT_UPDATE = """The user has requested an update for the documentation in the file {abs_file_path} with the following comment:
{comment}
Please update the documentation accordingly. The current content of the file is as follows:
{file_content}
The old documentation is as follows:
{old_file_docs}

Please provide the updated documentation content. DO NOT CHANGE ANYTHING IN THE OLD DOCUMENTATION THAT HAS NOT BEEN MENTIONED IN THE COMMENT.
"""