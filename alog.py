import datetime
import csv
from graphviz import Digraph

DATA_FILE = "relationships.dat"

if __name__ == "__main__":
    graph = Digraph("G", filename="graph.gv", format="svg", engine="neato")
    graph.attr(overlap="false")

    relationships = []
    posts = set()

    with open(DATA_FILE, "r") as fobj:
        reader = csv.reader(fobj, delimiter="\t")
        for source_id, target_slug, label, datestr in reader:
            date = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
            source_id = str(source_id)
            target_id = str(target_slug).lstrip("reference-to-post-id-")

            relationships.append((source_id, target_id, date))
            posts.add((source_id, label, date))
            posts.add((target_id, label, date))

    for source_id, target_id, _ in relationships:
        graph.edge(source_id, target_id)
    
    for post, label, date in posts:
        graph.node(post, label=f"{date:%Y-%m-%d}: {label[:30]}", href=f"https://alog.ligo-wa.caltech.edu/aLOG/index.php?callRep={post}", shape="rectangle")
    
    graph.view()
