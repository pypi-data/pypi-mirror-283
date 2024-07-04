# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateResSceneRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'content_type': 'str',
        'scene_id': 'str',
        'workspace_id': 'str',
        'body': 'UpdateResSceneRequestBody'
    }

    attribute_map = {
        'content_type': 'Content-Type',
        'scene_id': 'scene_id',
        'workspace_id': 'workspace_id',
        'body': 'body'
    }

    def __init__(self, content_type=None, scene_id=None, workspace_id=None, body=None):
        """UpdateResSceneRequest

        The model defined in huaweicloud sdk

        :param content_type: 内容类型，取值为application/json。
        :type content_type: str
        :param scene_id: 场景id。
        :type scene_id: str
        :param workspace_id: 工作空间id。
        :type workspace_id: str
        :param body: Body of the UpdateResSceneRequest
        :type body: :class:`huaweicloudsdkres.v1.UpdateResSceneRequestBody`
        """
        
        

        self._content_type = None
        self._scene_id = None
        self._workspace_id = None
        self._body = None
        self.discriminator = None

        self.content_type = content_type
        self.scene_id = scene_id
        self.workspace_id = workspace_id
        if body is not None:
            self.body = body

    @property
    def content_type(self):
        """Gets the content_type of this UpdateResSceneRequest.

        内容类型，取值为application/json。

        :return: The content_type of this UpdateResSceneRequest.
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """Sets the content_type of this UpdateResSceneRequest.

        内容类型，取值为application/json。

        :param content_type: The content_type of this UpdateResSceneRequest.
        :type content_type: str
        """
        self._content_type = content_type

    @property
    def scene_id(self):
        """Gets the scene_id of this UpdateResSceneRequest.

        场景id。

        :return: The scene_id of this UpdateResSceneRequest.
        :rtype: str
        """
        return self._scene_id

    @scene_id.setter
    def scene_id(self, scene_id):
        """Sets the scene_id of this UpdateResSceneRequest.

        场景id。

        :param scene_id: The scene_id of this UpdateResSceneRequest.
        :type scene_id: str
        """
        self._scene_id = scene_id

    @property
    def workspace_id(self):
        """Gets the workspace_id of this UpdateResSceneRequest.

        工作空间id。

        :return: The workspace_id of this UpdateResSceneRequest.
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this UpdateResSceneRequest.

        工作空间id。

        :param workspace_id: The workspace_id of this UpdateResSceneRequest.
        :type workspace_id: str
        """
        self._workspace_id = workspace_id

    @property
    def body(self):
        """Gets the body of this UpdateResSceneRequest.

        :return: The body of this UpdateResSceneRequest.
        :rtype: :class:`huaweicloudsdkres.v1.UpdateResSceneRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateResSceneRequest.

        :param body: The body of this UpdateResSceneRequest.
        :type body: :class:`huaweicloudsdkres.v1.UpdateResSceneRequestBody`
        """
        self._body = body

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateResSceneRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
