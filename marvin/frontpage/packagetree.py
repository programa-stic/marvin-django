#packagetree.py: Makes a dictionary-based tree from a list of package names

def getpackagetree(myPackages):
	myDict = {}
	for root_name in get_first_level(myPackages):
		myDict[root_name] = recursive_dict(myPackages, root_name)
	return myDict

def recursive_dict(myPackages, key):
	# print "entro a recursive_dict, key: " + key
	myDict = []
	newkeys = filter ( lambda item: item != key, get_more_levels(myPackages, key))
	if len(newkeys) == 0:
		return key
	for subkey in newkeys:
		if subkey.count('.')>key.count('.'):
			subdict = recursive_dict(myPackages, subkey)
			if isinstance(subdict, str) or isinstance(subdict,unicode):
				myDict.append(subdict)
			else:
				myDict.append({subkey:subdict})
	return myDict

def get_first_level(myPackages):
	mySet = set(map (lambda package: package.package_name.split('.')[0], myPackages))
	return mySet

def get_level_2(packagetree):
	myList = []
	for item in packagetree.keys():
		if isinstance(packagetree[item], unicode):
			myList.append(item)
		else:
			for it2 in packagetree[item]:
				if isinstance(it2, dict):
					myList.extend(it2.keys())
				if isinstance(it2, unicode):
					myList.append(it2)
	return myList
	            


def matches_to_nth(package_name, prefix, segments):
	package_segments = package_name.count('.')+1
	if package_segments >= segments:
		str1 = '.'.join(package_name.split('.')[0:segments])
		if str1 == prefix:
			return True
	return False

def get_more_levels(myPackages, prefix):
	prefLen = len(prefix.split('.'))
	mySet = set(filter(lambda package: matches_to_nth(package.package_name, prefix, prefLen), myPackages))
	mySet = set(map (lambda package: '.'.join(package.package_name.split('.')[0:prefLen+1]), mySet))
	return mySet
