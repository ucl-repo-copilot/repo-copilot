CODE_CONTEXT_PROMPT = """
First you need to get the content of this file (source code): {file_path}.
Then you need to get the information of the callee function in the same file path.
The information of the callee function can help you understand the context of the APIs.
Your task is to generate a brief explanation for the Python file.

Please use the following output template:

The content of the file (source code) is as follows:
`Put the file content here.`

Explanation of code context:
`Put the description of the code context here.`

Callee function information:
`Put callee function information here.` (Ignore this section if there is no callee function.)
"""

DOCUMENTATION_PROMPT_MD = """
First you can use the code context explainer to get the code context.
Then based on the code contextual explanation, generate a documentation for the source code. 
The purpose of the documentation is to help developers and beginners understand the function and specific usage of the code.
Please note any part of the content you generate SHOULD NOT CONTAIN Markdown hierarchical heading and divider syntax.
The file path is: {file_path}

The standard format is as follows:
(Note:
1. If a section does not have any information, you can skip it and move to the next one;
2. If you are confused about any part, feel free to add notes or comments;
3. If you have any suggestion to the code, also add concise comments.)

# {file_name}

## Source Code
`Put the file content here.`

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
"""

DOCUMENTATION_PROMPT_HTML = """
First you can use the code context explainer to get the code context.
Then based on the code contextual explanation, generate a documentation for the source code. 
The purpose of the documentation is to help developers and beginners understand the function and specific usage of the code.
Please note any part of the content you generate SHOULD NOT CONTAIN Markdown hierarchical heading and divider syntax.
The generated documentation MUST in HTML format as provided in the template below.
The file path is: {file_path}

The standard format is as follows:
(Note:
1. If a section does not have any information, you can skip it and move to the next one;
2. If you are confused about any part, feel free to add notes or comments;
3. If you have any suggestion to the code, also add concise comments.)

HTML Template:
<h1>{file_name}</h1>

<h2> Source Code </h2>
<pre><code>
`Put the file content here.`
</code></pre>

<h2>ClassDef NameOfClass</h2>

<p>The function of the class is XXX. (Only code name and one sentence function description are required)</p>

<h3>Attributes:</h3>

<ul>
<li><code>attribute1</code> (<code>type</code>): Description of the first attribute.</li>
</ul>

<h3>Functions:</h3>

<ul>
<li><code>function_name1</code>(<code>param1</code>: <code>type</code>) -> <code>return_type</code>
    <ul>
    <li>Parameters:
        <ul>
        <li><code>param1</code> (<code>type</code>): Description of the first parameter.</li>
        </ul>
    </li>
    <li>Returns:
        <ul>
        <li><code>return_type</code>: Description of the return value.</li>
        </ul>
    </li>
    </ul>
</li>
</ul>

<h3>Called_functions:</h3>

<ul>
<li><code>function1</code>(<code>param1</code>: <code>type</code>) -> <code>return_type</code>: Description of what function1 does and what function1 returns.</li>
</ul>

<h3>Code Description:</h3>
<p>The description of this class. (Detailed and CERTAIN code analysis and description)</p>

<h3>Note:</h3>
<p>Points to note about the use of the code according to the returns</p>

<h3>Input Example:</h3>

<pre><code>
Provide an input example for a specified data type (e.g., list, double, int) and include a detailed explanation.
</code></pre>

<h3>Output Example:</h3>

<pre><code>
Provide an output example for a specified data type (e.g., list, double, int) and include a detailed explanation.
</code></pre>

<h2>FunctionDef NameOfFunction (functions that do not belong to a class but are still present in the file)</h2>

<p>The function of the function is XXX. (Only code name and one sentence function description are required)</p>

<h3>Parameters:</h3>

<ul>
<li><code>param1</code> (<code>type</code>): Description of the first parameter.</li>
</ul>

<h3>Returns:</h3>

<ul>
<li><code>return_type</code>: Description of the return value.</li>
</ul>

<h3>Called_functions:</h3>

<ul>
<li><code>function1</code>(<code>param1</code>: <code>type</code>) -> <code>return_type</code>: Description of what function1 does and what function1 returns.</li>
</ul>

<h3>Code Description:</h3>
<p>The description of this function. (Detailed and CERTAIN code analysis and description)</p>

<h3>Note:</h3>
<p>Points to note about the use of the code according to the returns</p>

<h3>Input Example:</h3>

<pre><code>
Provide an input example for a specified data type (e.g., list, double, int) and include a detailed explanation.
</code></pre>

<h3>Output Example:</h3>

<pre><code>
Provide an output example for a specified data type (e.g., list, double, int) and include a detailed explanation.
</code></pre>
"""

REVIEWER_PROMPT = """
This is the generated documentation for the source code. Please review it and improve the documentation quality.
(Note:
1. DO NOT CHANGE the structure of the documentation; 
2. DO NOT CHANGE the format of the documentation;
3. DO NOT CHANGE values in the input/output examples;
4. After you are done with all checks of quality and accuracy, PLEASE REMOVE THE "SOURCE CODE" BLOCK.)
"""