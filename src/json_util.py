'''
convert all items in a json object from unicode to utf8
'''
def byteify(json_obj):
	if isinstance(json_obj, dict):
		return {byteify(key):byteify(value) for key,value in json_obj.iteritems()}
	elif isinstance(json_obj, list):
		return [byteify(element) for element in json_obj]
	elif isinstance(json_obj, unicode):
		return json_obj.encode('utf-8')
	else:
		return json_obj
