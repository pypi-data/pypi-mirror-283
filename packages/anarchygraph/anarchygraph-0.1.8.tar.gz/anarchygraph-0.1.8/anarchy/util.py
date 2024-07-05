import json

import ipycytoscape


def configure_cytoscape(path):
    with open(path) as fi:
        json_file = json.load(fi)
    cytoscapeobj = ipycytoscape.CytoscapeWidget()
    cytoscapeobj.graph.add_graph_from_json(json_file["elements"])
    cytoscapeobj.set_layout(name="grid")
    cytoscapeobj.set_style(
        [
            {
                "selector": "node",
                "style": {"height": 20, "width": 20, "background-color": "#30c9bc"},
            },
            {
                "selector": "edge",
                "style": {
                    "curve-style": "haystack",
                    "haystack-radius": 0,
                    "width": 5,
                    "opacity": 0.5,
                    "line-color": "#a8eae5",
                },
            },
        ]
    )

    # Disable zooming and panning
    cytoscapeobj.zoomingEnabled = False
    cytoscapeobj.userZoomingEnabled = False
    cytoscapeobj.panningEnabled = False
    cytoscapeobj.userPanningEnabled = False

    return cytoscapeobj


def convert_to_cytoscape_json(graph_data: dict) -> str:
    cytoscape_data = {
        "elements": {"nodes": [], "edges": []},
        "style": [
            {
                "selector": "node",
                "style": {
                    "background-color": "#666",
                    "label": "data(label)",
                    "width": 20,
                    "height": 20,
                },
            },
            {
                "selector": "edge",
                "style": {
                    "width": 3,
                    "line-color": "#ccc",
                    "target-arrow-color": "#ccc",
                    "target-arrow-shape": "triangle",
                    "label": "data(label)",
                },
            },
        ],
        "layout": {
            "name": "grid",
        },
    }

    # Add nodes
    for node in graph_data["nodes"]:
        cytoscape_node = {
            "data": {"id": node["id"], "label": node["id"]},
            "position": {
                "x": 0,  # random.randint(0, 100),
                "y": 0,  # random.randint(0, 100)
            },
            "group": "nodes",
            "removed": False,
            "selected": False,
            "selectable": True,
            "locked": False,
            "grabbable": True,
            "classes": node.get("classes", ""),
        }
        cytoscape_data["elements"]["nodes"].append(cytoscape_node)

    # Add edges
    for edge in graph_data["edges"]:
        cytoscape_edge = {
            "data": {
                "id": edge["id"],
                "source": edge["source"],
                "target": edge["target"],
                "label": edge["id"],
                "width": 3,
                "line-color": "#ccc",
                "target-arrow-color": "#ccc",
                "target-arrow-shape": "triangle",
            },
            "group": "edges",
            "removed": False,
            "selected": False,
            "selectable": True,
            "locked": False,
            "grabbable": True,
            "classes": edge.get("classes", ""),
        }
        cytoscape_data["elements"]["edges"].append(cytoscape_edge)

    return json.dumps(cytoscape_data, indent=2)


# Convert and save to a JSON file
def save_cytoscape_json(graph_data: dict, filename: str) -> None:
    cytoscape_json = convert_to_cytoscape_json(graph_data)
    with open(filename, "w") as f:
        f.write(cytoscape_json)
