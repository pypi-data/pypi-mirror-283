# coding: utf-8

"""
    everai/volumes/v1/message.proto

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: version not set
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from generated.volumes.models.v1_list_response import V1ListResponse  # noqa: E501

class TestV1ListResponse(unittest.TestCase):
    """V1ListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> V1ListResponse:
        """Test V1ListResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `V1ListResponse`
        """
        model = V1ListResponse()  # noqa: E501
        if include_optional:
            return V1ListResponse(
                volumes = [
                    generated.volumes.models.v1_volume.v1Volume(
                        id = '', 
                        name = '', 
                        revision = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        labels = {
                            'key' : ''
                            }, 
                        size = '', 
                        files = '', 
                        status = 'Unspecified', 
                        username = '', )
                    ]
            )
        else:
            return V1ListResponse(
        )
        """

    def testV1ListResponse(self):
        """Test V1ListResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
