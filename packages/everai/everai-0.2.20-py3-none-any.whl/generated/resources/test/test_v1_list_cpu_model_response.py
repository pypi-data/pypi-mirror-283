# coding: utf-8

"""
    everai/resources/v1/message.proto

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: version not set
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from generated.resources.models.v1_list_cpu_model_response import V1ListCpuModelResponse  # noqa: E501

class TestV1ListCpuModelResponse(unittest.TestCase):
    """V1ListCpuModelResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> V1ListCpuModelResponse:
        """Test V1ListCpuModelResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `V1ListCpuModelResponse`
        """
        model = V1ListCpuModelResponse()  # noqa: E501
        if include_optional:
            return V1ListCpuModelResponse(
                gpus = [
                    ''
                    ]
            )
        else:
            return V1ListCpuModelResponse(
        )
        """

    def testV1ListCpuModelResponse(self):
        """Test V1ListCpuModelResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
