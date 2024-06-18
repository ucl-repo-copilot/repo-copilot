from cache import cache
from graph.graph_manager import build_graph, save_graph_to_json

graph = build_graph('./program_examples/simple')
save_graph_to_json(graph)

visited = set()
result = []
queue = ['C.methodC1']

while queue:
    current = queue.pop(0)
    cached = cache.get(current)
    method = cached.method
    if current in visited:
        continue
    visited.add(current)
    
    result.append(f"""
## {f'{cached.class_name}.' if cached.class_name else ''}{method.name}
```python
{method.content.replace('\n\n', '').strip()}
```
Internal calls: ``{method.internal}`` <br/>
External calls: ``{method.external}`` <br/>
Documentation generated: ``{'✓' if method.docs else 'X'}``
<br/>
    """)
    queue.extend(method.internal)
    
# Write result
with open('./result.md', 'w') as file:
    file.write('\n'.join(result))
    