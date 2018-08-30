
# from djgpa.api import GooglePlay

# api = GooglePlay().auth()

# def get_related_app_names(app_name):
# 	details = api.details(app_name)
# 	related = api._executeRequestApi2(details.docV2.annotations.sectionCrossSell.listUrl).payload.listResponse.doc._values[0].child
# 	retlist = []
# 	for item in related:
# 		retlist.append({ 'package_name':item.docid, 
# 						 'app_name'    :item.title, 
# 						 'versionCode' :item.details.appDetails.versionCode, 
# 						 'uploadDate'  :item.details.appDetails.uploadDate,
# 						 'numDownloads':item.details.appDetails.numDownloads})
# 	return retlist


