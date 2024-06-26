import os
import datetime
import sys
import time
from autogen import AssistantAgent, UserProxyAgent
from prompt import DOCUMENTATION_PROMPT, USR_PROMPT

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), './../')))

from code2flow.code2flow import utils

class RepoDocumentation():
    __llm_config = {
        "model": "llama3",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }

    def __init__(self, root_folder, output_dir='code2flow_output'):
        self.root_folder = root_folder
        self.output_dir = output_dir
        self.assistant = self._load_assistant_agent()
        self.user = self._load_user_agent()

    def run(self):
        print("Starting the documentation generation process...")
        start_time = time.time()

        # 1. Generate graph (call_graph.json and cache.json)
        utils.generate_graph(self.root_folder, self.output_dir)
        cache = utils.get_cache(self.output_dir)
        graph = utils.get_call_graph(self.output_dir)

        # 2. Build mapping of a file to the functions called within them
        file_to_calls = utils.get_file_to_functions(graph)

        # 3. Build BFS exploration of the call graph
        bfs_explore = utils.explore_call_graph(graph)

        # 4. Generate documentation for each file and function within
        for file_path, calls in file_to_calls.items():
            print(f"Generating documentation for file={file_path}")
            if file_path == 'EXTERNAL':
                continue

            additional_docs = self._generate_additional_docs(calls, graph, bfs_explore)
            file_content = self._read_file_content(file_path)
            file_docs = self._generate_file_docs(file_path, file_content, additional_docs)
            self._write_file_docs(file_path, file_docs)

            for call in calls:
                call = graph[call]
                name = call['name']

                # Core functionality to generate documentation
                if 'EXTERNAL' in call['file_name']:
                    docs = self._generate_docs_internal(name)
                else:
                    docs = self._generate_docs_external(name, graph, cache,
                                                       file_path, call['content'], bfs_explore[name])

                # Store the generated documentation in the cache (TODO: change impl)
                self._update_cache(cache, name, docs)

        # 5. Write the generated documentation back to the cache file
        utils.write_json(f'{self.output_dir}/cache_docs.json', cache)

        total = round(time.time() - start_time, 3)
        print(f"Total time taken to execute doc generation: {total}s.")

    def _load_assistant_agent(self):
        return AssistantAgent(
            name="assistant",
            system_message=USR_PROMPT,
            llm_config=self.__llm_config,
            human_input_mode="NEVER"
        )

    def _load_user_agent(self):
        return UserProxyAgent(
            name="user",
            code_execution_config=False,
        )

    def _generate_additional_docs(self, calls, graph, bfs_explore):
        additional_docs = ""
        for call_name in calls:
            call = graph[call_name]
            if 'EXTERNAL' in call['file_name']:
                continue
            for callee in bfs_explore[call_name]:
                callee_call = graph[callee]
                additional_docs += f"\nFunction/Class {callee_call['name']}:\n{callee_call['content']}\n"
        return additional_docs

    def _read_file_content(self, file_path):
        full_path = file_path
        print(f"Reading file: {full_path}")
        try:
            with open(full_path, 'r') as file:
                content = file.read()
                return content
            
        except FileNotFoundError:
            return ""

    def _generate_file_docs(self, file_path, file_content, additional_docs):
        prompt_message = DOCUMENTATION_PROMPT.format(
            file_name=os.path.basename(file_path),
            file_content=file_content,
            root_folder=self.root_folder,
            additional_docs=additional_docs
        )

        self.user.initiate_chat(
            self.assistant,
            message=prompt_message,
            max_turns=1,
            silent=True
        )

        file_name = self.output_dir + "/" + os.path.basename(file_path) + ".txt"

        with open(file_name, 'w') as file:
            file.write(prompt_message)

        return self.assistant.last_message()['content']

    def _write_file_docs(self, file_path, docs):
        # Generate the output file path based on the input file path
        relative_path = os.path.relpath(file_path, self.root_folder)
        output_file_path = os.path.join(self.output_dir, relative_path)
        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)

        # Add .md extension to the output file
        output_file_path += ".md"

        # Write the documentation to the output file
        with open(output_file_path, 'w') as file:
            file.write(docs)

    def _generate_docs_internal(self, name):
        return f'(empty docs for {name})'

    def _generate_docs_external(self, name, graph, cache, file_path, source_code, callees_dict):
        print(f"Generating documentation for function={name}")
        additional_docs = ""

        # 0. Check for cache-hit
        cached_docs = cache.get(name, None)

        # 1. Open the file and read all of its contents for additional documentation, as needed
        file = open(file_path, 'r')

        for item in callees_dict:
            call = graph[item]  # Access the call information
            call_name = call['name']
            
            if 'EXTERNAL' in call_name:
                # TODO: additional_docs += (handle external functions here)
                continue
            
            call_source_code = call['content']
            call_callees = call['callees']
            call_parent_file = open(call['file_name'], 'r')

            # TODO: Here we could either read the entire file or just the function/class definition
            additional_docs += f"\nFunction/Class {call_name}:\n{call_source_code}\n"

            # Close the file
            call_parent_file.close()

        prompt_message = DOCUMENTATION_PROMPT.format(
            file_name=os.path.basename(file_path),
            file_content=source_code,
            root_folder=self.root_folder,
            additional_docs=additional_docs
        )

        self.user.initiate_chat(
            self.assistant,
            message=prompt_message,
            max_turns=1,
            silent=True
        )

        file.close()

        # Return the last message from the assistant, which is the generated documentation
        return self.assistant.last_message()['content']

    # TODO: Change the implementation as required
    def _update_cache(self, cache, function_name, docs):
        if function_name not in cache:
            cache[function_name] = {}
        cache[function_name]['version'] = 1
        cache[function_name]['generated_on'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')
        cache[function_name]['generated_docs'] = docs


repo_doc = RepoDocumentation(
    root_folder='../code2flow/projects/users',
    output_dir='./../code2flow_output_users')
repo_doc.run()
