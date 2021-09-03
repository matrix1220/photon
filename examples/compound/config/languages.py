
import yaml
from photon.object_dict import objectify

languages = []
for x in ['language_en.yaml']:
	languages.append(objectify(yaml.load(open(x).read(), Loader=yaml.Loader)))