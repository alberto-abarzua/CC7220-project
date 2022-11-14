import subprocess
from pathlib import Path

"""
------------------------------------------------------------------------

Uses tarql to create RDF from CSV files

------------------------------------------------------------------------

"""

# cur path of file
cur_path = Path(__file__).parent

dest = cur_path / "rdf_dataset"

if not dest.exists():
    dest.mkdir()


C2  = "./tarql/bin/tarql --ntriples ./sparql/videos.sparql ./clean_dataset/videos.csv > ./rdf_dataset/videos.ttl"
C3 = "./tarql/bin/tarql --ntriples ./sparql/video_tags.sparql ./clean_dataset/video_tags.csv > ./rdf_dataset/video_tags.ttl"
C4 = "cat ./rdf_dataset/videos.ttl ./rdf_dataset/video_tags.ttl > ./rdf_dataset/all.ttl"

subprocess.call(C2, shell=True)
subprocess.call(C3, shell=True)
subprocess.call(C4, shell=True)