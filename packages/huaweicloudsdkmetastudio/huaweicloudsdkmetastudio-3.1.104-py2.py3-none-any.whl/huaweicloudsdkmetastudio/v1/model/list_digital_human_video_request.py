# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListDigitalHumanVideoRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'x_app_user_id': 'str',
        'offset': 'int',
        'limit': 'int',
        'state': 'str',
        'sort_key': 'str',
        'sort_dir': 'str',
        'create_until': 'str',
        'create_since': 'str',
        'script_id': 'str',
        'asset_name': 'str',
        'job_type': 'str',
        'job_id': 'str'
    }

    attribute_map = {
        'x_app_user_id': 'X-App-UserId',
        'offset': 'offset',
        'limit': 'limit',
        'state': 'state',
        'sort_key': 'sort_key',
        'sort_dir': 'sort_dir',
        'create_until': 'create_until',
        'create_since': 'create_since',
        'script_id': 'script_id',
        'asset_name': 'asset_name',
        'job_type': 'job_type',
        'job_id': 'job_id'
    }

    def __init__(self, x_app_user_id=None, offset=None, limit=None, state=None, sort_key=None, sort_dir=None, create_until=None, create_since=None, script_id=None, asset_name=None, job_type=None, job_id=None):
        """ListDigitalHumanVideoRequest

        The model defined in huaweicloud sdk

        :param x_app_user_id: 第三方用户ID。不允许输入中文。
        :type x_app_user_id: str
        :param offset: 偏移量，表示从此偏移量开始查询。
        :type offset: int
        :param limit: 每页显示的条目数量。
        :type limit: int
        :param state: 任务状态，默认所有状态。  可多个状态查询，使用英文逗号分隔。  如state&#x3D;CREATING,PUBLISHED
        :type state: str
        :param sort_key: 排序字段，目前只支持create_time。
        :type sort_key: str
        :param sort_dir: 排序方式。 * asc：升序 * desc：降序  默认asc升序。
        :type sort_dir: str
        :param create_until: 过滤创建时间&lt;&#x3D;输入时间的记录。
        :type create_until: str
        :param create_since: 过滤创建时间&gt;&#x3D;输入时间的记录。
        :type create_since: str
        :param script_id: 剧本ID。
        :type script_id: str
        :param asset_name: 输出视频资产名称。
        :type asset_name: str
        :param job_type: 任务类型。 * 2D_DIGITAL_HUMAN_VIDEO: 分身数字人视频制作任务 * PHOTO_DIGITAL_HUMAN_VIDEO: 照片数字人视频制作任务
        :type job_type: str
        :param job_id: 任务ID。
        :type job_id: str
        """
        
        

        self._x_app_user_id = None
        self._offset = None
        self._limit = None
        self._state = None
        self._sort_key = None
        self._sort_dir = None
        self._create_until = None
        self._create_since = None
        self._script_id = None
        self._asset_name = None
        self._job_type = None
        self._job_id = None
        self.discriminator = None

        if x_app_user_id is not None:
            self.x_app_user_id = x_app_user_id
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit
        if state is not None:
            self.state = state
        if sort_key is not None:
            self.sort_key = sort_key
        if sort_dir is not None:
            self.sort_dir = sort_dir
        if create_until is not None:
            self.create_until = create_until
        if create_since is not None:
            self.create_since = create_since
        if script_id is not None:
            self.script_id = script_id
        if asset_name is not None:
            self.asset_name = asset_name
        if job_type is not None:
            self.job_type = job_type
        if job_id is not None:
            self.job_id = job_id

    @property
    def x_app_user_id(self):
        """Gets the x_app_user_id of this ListDigitalHumanVideoRequest.

        第三方用户ID。不允许输入中文。

        :return: The x_app_user_id of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._x_app_user_id

    @x_app_user_id.setter
    def x_app_user_id(self, x_app_user_id):
        """Sets the x_app_user_id of this ListDigitalHumanVideoRequest.

        第三方用户ID。不允许输入中文。

        :param x_app_user_id: The x_app_user_id of this ListDigitalHumanVideoRequest.
        :type x_app_user_id: str
        """
        self._x_app_user_id = x_app_user_id

    @property
    def offset(self):
        """Gets the offset of this ListDigitalHumanVideoRequest.

        偏移量，表示从此偏移量开始查询。

        :return: The offset of this ListDigitalHumanVideoRequest.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ListDigitalHumanVideoRequest.

        偏移量，表示从此偏移量开始查询。

        :param offset: The offset of this ListDigitalHumanVideoRequest.
        :type offset: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this ListDigitalHumanVideoRequest.

        每页显示的条目数量。

        :return: The limit of this ListDigitalHumanVideoRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListDigitalHumanVideoRequest.

        每页显示的条目数量。

        :param limit: The limit of this ListDigitalHumanVideoRequest.
        :type limit: int
        """
        self._limit = limit

    @property
    def state(self):
        """Gets the state of this ListDigitalHumanVideoRequest.

        任务状态，默认所有状态。  可多个状态查询，使用英文逗号分隔。  如state=CREATING,PUBLISHED

        :return: The state of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ListDigitalHumanVideoRequest.

        任务状态，默认所有状态。  可多个状态查询，使用英文逗号分隔。  如state=CREATING,PUBLISHED

        :param state: The state of this ListDigitalHumanVideoRequest.
        :type state: str
        """
        self._state = state

    @property
    def sort_key(self):
        """Gets the sort_key of this ListDigitalHumanVideoRequest.

        排序字段，目前只支持create_time。

        :return: The sort_key of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._sort_key

    @sort_key.setter
    def sort_key(self, sort_key):
        """Sets the sort_key of this ListDigitalHumanVideoRequest.

        排序字段，目前只支持create_time。

        :param sort_key: The sort_key of this ListDigitalHumanVideoRequest.
        :type sort_key: str
        """
        self._sort_key = sort_key

    @property
    def sort_dir(self):
        """Gets the sort_dir of this ListDigitalHumanVideoRequest.

        排序方式。 * asc：升序 * desc：降序  默认asc升序。

        :return: The sort_dir of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._sort_dir

    @sort_dir.setter
    def sort_dir(self, sort_dir):
        """Sets the sort_dir of this ListDigitalHumanVideoRequest.

        排序方式。 * asc：升序 * desc：降序  默认asc升序。

        :param sort_dir: The sort_dir of this ListDigitalHumanVideoRequest.
        :type sort_dir: str
        """
        self._sort_dir = sort_dir

    @property
    def create_until(self):
        """Gets the create_until of this ListDigitalHumanVideoRequest.

        过滤创建时间<=输入时间的记录。

        :return: The create_until of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._create_until

    @create_until.setter
    def create_until(self, create_until):
        """Sets the create_until of this ListDigitalHumanVideoRequest.

        过滤创建时间<=输入时间的记录。

        :param create_until: The create_until of this ListDigitalHumanVideoRequest.
        :type create_until: str
        """
        self._create_until = create_until

    @property
    def create_since(self):
        """Gets the create_since of this ListDigitalHumanVideoRequest.

        过滤创建时间>=输入时间的记录。

        :return: The create_since of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._create_since

    @create_since.setter
    def create_since(self, create_since):
        """Sets the create_since of this ListDigitalHumanVideoRequest.

        过滤创建时间>=输入时间的记录。

        :param create_since: The create_since of this ListDigitalHumanVideoRequest.
        :type create_since: str
        """
        self._create_since = create_since

    @property
    def script_id(self):
        """Gets the script_id of this ListDigitalHumanVideoRequest.

        剧本ID。

        :return: The script_id of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """Sets the script_id of this ListDigitalHumanVideoRequest.

        剧本ID。

        :param script_id: The script_id of this ListDigitalHumanVideoRequest.
        :type script_id: str
        """
        self._script_id = script_id

    @property
    def asset_name(self):
        """Gets the asset_name of this ListDigitalHumanVideoRequest.

        输出视频资产名称。

        :return: The asset_name of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._asset_name

    @asset_name.setter
    def asset_name(self, asset_name):
        """Sets the asset_name of this ListDigitalHumanVideoRequest.

        输出视频资产名称。

        :param asset_name: The asset_name of this ListDigitalHumanVideoRequest.
        :type asset_name: str
        """
        self._asset_name = asset_name

    @property
    def job_type(self):
        """Gets the job_type of this ListDigitalHumanVideoRequest.

        任务类型。 * 2D_DIGITAL_HUMAN_VIDEO: 分身数字人视频制作任务 * PHOTO_DIGITAL_HUMAN_VIDEO: 照片数字人视频制作任务

        :return: The job_type of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._job_type

    @job_type.setter
    def job_type(self, job_type):
        """Sets the job_type of this ListDigitalHumanVideoRequest.

        任务类型。 * 2D_DIGITAL_HUMAN_VIDEO: 分身数字人视频制作任务 * PHOTO_DIGITAL_HUMAN_VIDEO: 照片数字人视频制作任务

        :param job_type: The job_type of this ListDigitalHumanVideoRequest.
        :type job_type: str
        """
        self._job_type = job_type

    @property
    def job_id(self):
        """Gets the job_id of this ListDigitalHumanVideoRequest.

        任务ID。

        :return: The job_id of this ListDigitalHumanVideoRequest.
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this ListDigitalHumanVideoRequest.

        任务ID。

        :param job_id: The job_id of this ListDigitalHumanVideoRequest.
        :type job_id: str
        """
        self._job_id = job_id

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
        if not isinstance(other, ListDigitalHumanVideoRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
