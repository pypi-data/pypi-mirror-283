import re  # noqa: F401

from pydantic import Field
from pydantic import validate_arguments
from typing_extensions import Annotated

from xingchen.api_client import ApiClient
from xingchen.api_response import ApiResponse
from xingchen.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)
from xingchen.models.knowledge_base_create_dto import KnowledgeBaseCreateDTO
from xingchen.models.knowledge_base_delete_dto import KnowledgeBaseDeleteDTO
from xingchen.models.knowledge_base_detail_delete_dto import KnowledgeBaseDetailDeleteDTO
from xingchen.models.knowledge_base_detail_query_dto import KnowledgeBaseDetailQueryDTO
from xingchen.models.knowledge_base_detail_update_dto import KnowledgeBaseDetailUpdateDTO
from xingchen.models.knowledge_base_detail_upload_dto import KnowledgeBaseDetailUploadDTO
from xingchen.models.knowledge_base_query_dto import KnowledgeBaseQueryDTO
from xingchen.models.knowledge_base_update_dto import KnowledgeBaseUpdateDTO
from xingchen.models.result_dto_boolean import ResultDTOBoolean
from xingchen.models.result_dto_knowledge_base_dto import ResultDTOKnowledgeBaseDTO
from xingchen.models.result_dto_page_result_knowledge_base_detail_dto import ResultDTOPageResultKnowledgeBaseDetailDTO
from xingchen.models.result_dto_page_result_knowledge_base_dto import ResultDTOPageResultKnowledgeBaseDTO


class KnowledgeBaseApiSub:
    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    def version(self):
        return self.api_client.api_version()

    @validate_arguments
    def create(self, knowledge_base_create_dto: Annotated[
        KnowledgeBaseCreateDTO, Field(..., description="创建知识库请求")],
               **kwargs) -> ResultDTOKnowledgeBaseDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the create_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.create_with_http_info(knowledge_base_create_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def create_with_http_info(self, knowledge_base_create_dto: Annotated[
        KnowledgeBaseCreateDTO, Field(..., description="创建知识库请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_create_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_create_dto'] is not None:
            _body_params = _params['knowledge_base_create_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOKnowledgeBaseDTO",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/create'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def update(self, knowledge_base_update_dto: Annotated[KnowledgeBaseUpdateDTO, Field(..., description="修改知识库请求")],
               **kwargs) -> ResultDTOBoolean:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.update_with_http_info(knowledge_base_update_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def update_with_http_info(self, knowledge_base_update_dto: Annotated[
        KnowledgeBaseUpdateDTO, Field(..., description="修改知识库请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_update_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_update_dto'] is not None:
            _body_params = _params['knowledge_base_update_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOBoolean",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/update'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def search(self, knowledge_base_query_dto: Annotated[KnowledgeBaseQueryDTO, Field(..., description="查询知识库请求")],
               **kwargs) -> ResultDTOPageResultKnowledgeBaseDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the search_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.search_with_http_info(knowledge_base_query_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def search_with_http_info(self, knowledge_base_query_dto: Annotated[
        KnowledgeBaseQueryDTO, Field(..., description="查询知识库请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_query_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_query_dto'] is not None:
            _body_params = _params['knowledge_base_query_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOPageResultKnowledgeBaseDTO",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/search'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def delete(self, knowledge_base_delete_dto: Annotated[KnowledgeBaseDeleteDTO, Field(..., description="删除知识库")],
               **kwargs) -> ResultDTOBoolean:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the delete_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.delete_with_http_info(knowledge_base_delete_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def delete_with_http_info(self, knowledge_base_delete_dto: Annotated[
        KnowledgeBaseDeleteDTO, Field(..., description="删除知识库请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_delete_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_delete_dto'] is not None:
            _body_params = _params['knowledge_base_delete_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOBoolean",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/delete'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def detail_upload(self,
                      knowledge_base_detail_upload_dto: Annotated[
                          KnowledgeBaseDetailUploadDTO, Field(..., description="知识库文件上传请求")],
                      **kwargs) -> ResultDTOBoolean:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the detail_upload_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.detail_upload_with_http_info(knowledge_base_detail_upload_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def detail_upload_with_http_info(self, knowledge_base_detail_upload_dto: Annotated[
        KnowledgeBaseDetailUploadDTO, Field(..., description="知识库文件上传请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_detail_upload_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method detail_upload" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_detail_upload_dto'] is not None:
            _body_params = _params['knowledge_base_detail_upload_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOBoolean",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/detail/upload'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def detail_update(self,
                      knowledge_base_detail_update_dto: Annotated[
                          KnowledgeBaseDetailUpdateDTO, Field(..., description="修改知识库详情请求")],
                      **kwargs) -> ResultDTOBoolean:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the detail_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.detail_update_with_http_info(knowledge_base_detail_update_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def detail_update_with_http_info(self, knowledge_base_detail_update_dto: Annotated[
        KnowledgeBaseDetailUpdateDTO, Field(..., description="修改知识库详情请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_detail_update_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method detail_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_detail_update_dto'] is not None:
            _body_params = _params['knowledge_base_detail_update_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOBoolean",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/detail/update'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def detail_search(self, knowledge_base_detail_query_dto: Annotated[
        KnowledgeBaseDetailQueryDTO, Field(..., description="查询知识库详情请求")],
                      **kwargs) -> ResultDTOPageResultKnowledgeBaseDetailDTO:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the detail_search_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.detail_search_with_http_info(knowledge_base_detail_query_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def detail_search_with_http_info(self, knowledge_base_detail_query_dto: Annotated[
        KnowledgeBaseDetailQueryDTO, Field(..., description="查询知识库详情请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_detail_query_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method detail_search" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_detail_query_dto'] is not None:
            _body_params = _params['knowledge_base_detail_query_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOPageResultKnowledgeBaseDetailDTO",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/detail/search'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def detail_delete(self, knowledge_base_detail_delete_dto: Annotated[
        KnowledgeBaseDetailDeleteDTO, Field(..., description="删除知识库详情请求")], **kwargs) -> ResultDTOBoolean:  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the detail_delete_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.detail_delete_with_http_info(knowledge_base_detail_delete_dto, **kwargs)  # noqa: E501

    @validate_arguments
    def detail_delete_with_http_info(self, knowledge_base_detail_delete_dto: Annotated[
        KnowledgeBaseDetailDeleteDTO, Field(..., description="删除知识库详情请求")], **kwargs) -> ApiResponse:  # noqa: E501

        _params = locals()

        _all_params = [
            'knowledge_base_detail_delete_dto'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method detail_delete" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['knowledge_base_detail_delete_dto'] is not None:
            _body_params = _params['knowledge_base_detail_delete_dto']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
                                          self.api_client.select_header_content_type(
                                              ['application/json']))
        if _content_types_list:
            _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['Authorization']  # noqa: E501

        _response_types_map = {
            '200': "ResultDTOBoolean",
        }

        return self.api_client.call_api(
            '/{0}/api/knowledge_base/detail/delete'.format(self.version()), 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
