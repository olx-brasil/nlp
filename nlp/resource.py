# -*- coding: utf-8 -*-

import pkg_resources, os

class Resource:
    @staticmethod
    def getPackage():
        return __name__

    @staticmethod
    def getResourcePath(*path_relative_array):
        resource_relative = os.path.join(*path_relative_array)
        return pkg_resources.resource_filename(Resource.getPackage(), resource_relative)
