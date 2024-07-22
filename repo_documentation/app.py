import utils
import os
import sys
import time
import asyncio

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), './../')))

from code2flow.code2flow import utils as graph_utils
from cache.docs_cache import DocsCache
from autogen_utils import utils as autogen_utils
from documentation_evaluation import evaluate_answer_relevancy
from repo_documentation.prompt import DOCUMENTATION_PROMPT

class RepoDocumentation():
    def __init__(self, root_folder):
        self.root_folder = os.path.abspath(root_folder)
        self.output_dir = os.path.join(self.root_folder, "docs_output")
        self.assistant = autogen_utils.load_assistant_agent()
        self.user = autogen_utils.load_user_agent()

    async def run(self):
        print('Generating documentation...')
        print(f'Root folder: {self.root_folder}')
        print(f'Output folder: {self.output_dir}')
        start_time = time.time()

        # 1. Generate graph
        graph_utils.generate_graph(self.root_folder, self.output_dir)
        graph = graph_utils.get_call_graph(self.output_dir)

        # 2. Build mapping of a file to the functions called within them
        file_to_calls = graph_utils.get_file_to_functions(graph)

        # 3. Build BFS exploration of the call graph
        bfs_explore = graph_utils.explore_call_graph(graph)

        # 4. Prepare cache, where we will map file paths to their respective documentation
        cache = DocsCache()

        # 5. Generate documentation for each file and function within
        for file_path, calls in file_to_calls.items():
            if file_path == 'EXTERNAL':  # Skip all external functions
                continue

            additional_docs = autogen_utils.get_additional_docs_calls(
                calls, graph, bfs_explore)
            file_content = utils.read_file_content(file_path)

            # Generate documentation for the file
            docs = autogen_utils.get_documentation(
                file_path=file_path,
                file_content=file_content,
                additional_docs=additional_docs,
                user=self.user,
                assistant=self.assistant,
                output_dir=self.output_dir,
                root_folder=self.root_folder,
                save_debug=True
            )

            #Collect query and response for evaluation
            query = DOCUMENTATION_PROMPT.format(
                file_name=os.path.basename(file_path),
                file_content=file_content,
                root_folder=self.root_folder,
                additional_docs=additional_docs
            )
            #query = "say my name"
            response = docs

            # Evaluate the documentation
            eval_result = await evaluate_answer_relevancy(query=query, response=response)
            print(f"score: {eval_result.score}, feedback: {eval_result.feedback}")


            # Write the documentation to a file
            docs_filepath = utils.write_file_docs(output_dir=self.output_dir,
                                                  root_folder=self.root_folder,
                                                  file_path=file_path,
                                                  docs=docs)

            # 6. Add the file path and its according documentation to the cache
            cache.add(file_path, file_content, docs_filepath)

        # 7. Save cache to a file
        utils.save_cache(self.output_dir, cache)

        total = round(time.time() - start_time, 3)
        print(f'Generated documentation ({cache.size()} files) can be found in {self.output_dir}')
        print(f"Documentation generation completed in {total}s.")


#RepoDocumentation(root_folder='./../../users/').run()
if __name__ == "__main__":
    # Use asyncio to run the asynchronous main function
    #root_folder = 'D:/UCL/Term 3/unoserver/src/unoserver/comments_removed'
    #root_folder = 'D:/UCL/Term 3/Project/repo-copilot/code2flow/projects/users'
    root_folder = 'D:/UCL/Term 3/SmoothStream'
    repo_documentation = RepoDocumentation(root_folder)
    asyncio.run(repo_documentation.run())