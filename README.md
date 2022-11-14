# CC7220-project


## tarql commands



* create tags: `./tarql/bin/tarql --ntriples ./sparql/tags.sparql ./clean_dataset/tags.csv > ./rdf_dataset/tags.ttl`
* create video triples: `./tarql/bin/tarql --ntriples ./sparql/videos.sparql ./clean_dataset/videos.csv > ./rdf_dataset/videos.ttl`

* create video_tags: `./tarql/bin/tarql --ntriples ./sparql/video_tags.sparql ./clean_dataset/video_tags.csv > ./rdf_dataset/video_tags.ttl`