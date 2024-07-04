# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class VideoConfig:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'clip_mode': 'str',
        'codec': 'str',
        'bitrate': 'int',
        'width': 'int',
        'height': 'int',
        'frame_rate': 'str',
        'is_subtitle_enable': 'bool',
        'subtitle_config': 'SubtitleConfig',
        'dx': 'int',
        'dy': 'int',
        'is_enable_super_resolution': 'bool'
    }

    attribute_map = {
        'clip_mode': 'clip_mode',
        'codec': 'codec',
        'bitrate': 'bitrate',
        'width': 'width',
        'height': 'height',
        'frame_rate': 'frame_rate',
        'is_subtitle_enable': 'is_subtitle_enable',
        'subtitle_config': 'subtitle_config',
        'dx': 'dx',
        'dy': 'dy',
        'is_enable_super_resolution': 'is_enable_super_resolution'
    }

    def __init__(self, clip_mode=None, codec=None, bitrate=None, width=None, height=None, frame_rate=None, is_subtitle_enable=None, subtitle_config=None, dx=None, dy=None, is_enable_super_resolution=None):
        """VideoConfig

        The model defined in huaweicloud sdk

        :param clip_mode: 输出视频的剪辑方式。默认值RESIZE。 * RESIZE：视频缩放。 * CROP：视频裁剪。
        :type clip_mode: str
        :param codec: 视频编码格式及视频文件格式。 * H264: h264编码，输出mp4文件 * VP8：vp8编码，输出webm文件
        :type codec: str
        :param bitrate: 输出平均码率。  单位：kbps。  最小值40，最大值30000。 &gt; * 分身数字人视频制作采用质量优先，可能会超过设置的码率。 &gt; * 分身数字人直播码率范围[1000, 8000]。
        :type bitrate: int
        :param width: 视频宽度。  单位：像素。  &gt; * clip_mode&#x3D;RESIZE时，当前支持1920x1080、1080x1920、1280x720、720x1280、3840x2160、2160x3840六种分辨率。4K分辨率视频需要分身数字人模型支持4K的情况下才能使用。 &gt; * clip_mode&#x3D;CROP，裁剪后视频，（dx,dy）为原点，保留视频像宽度为width。 &gt; * 分身数字人直播目前只支持1080x1920。
        :type width: int
        :param height: 视频高度。  单位：像素。  &gt; * clip_mode&#x3D;RESIZE时，当前支持1920x1080、1080x1920、1280x720、720x1280、3840x2160、2160x3840六种分辨率分辨率。 &gt; * clip_mode&#x3D;CROP，裁剪后视频，（dx,dy）为原点，保留视频像高度为height。 &gt; * 分身数字人直播目前只支持1080x1920。
        :type height: int
        :param frame_rate: 帧率。  单位：FPS。 &gt; *  分身数字人视频固定25FPS。
        :type frame_rate: str
        :param is_subtitle_enable: 输出的视频是否带字幕。默认false。 &gt; true: 打开字幕 &gt; false: 关闭字幕
        :type is_subtitle_enable: bool
        :param subtitle_config: 
        :type subtitle_config: :class:`huaweicloudsdkmetastudio.v1.SubtitleConfig`
        :param dx: 裁剪视频左上角像素点坐标。  clip_mode&#x3D; CROP时生效。 &gt; * 以模特分辨率为画布大小，比如1920*1080分辨率的模特，dx最小值是0，最大值是1920。
        :type dx: int
        :param dy: 裁剪视频左上角像素点坐标。  clip_mode&#x3D; CROP时生效。 &gt; * 以模特分辨率为画布大小，比如1920*1080分辨率的模特，dy最小值是0，最大值是1080
        :type dy: int
        :param is_enable_super_resolution: 视频是否开启超分。 &gt; true: 开启 &gt; false: 不开启
        :type is_enable_super_resolution: bool
        """
        
        

        self._clip_mode = None
        self._codec = None
        self._bitrate = None
        self._width = None
        self._height = None
        self._frame_rate = None
        self._is_subtitle_enable = None
        self._subtitle_config = None
        self._dx = None
        self._dy = None
        self._is_enable_super_resolution = None
        self.discriminator = None

        if clip_mode is not None:
            self.clip_mode = clip_mode
        self.codec = codec
        self.bitrate = bitrate
        self.width = width
        self.height = height
        if frame_rate is not None:
            self.frame_rate = frame_rate
        if is_subtitle_enable is not None:
            self.is_subtitle_enable = is_subtitle_enable
        if subtitle_config is not None:
            self.subtitle_config = subtitle_config
        if dx is not None:
            self.dx = dx
        if dy is not None:
            self.dy = dy
        if is_enable_super_resolution is not None:
            self.is_enable_super_resolution = is_enable_super_resolution

    @property
    def clip_mode(self):
        """Gets the clip_mode of this VideoConfig.

        输出视频的剪辑方式。默认值RESIZE。 * RESIZE：视频缩放。 * CROP：视频裁剪。

        :return: The clip_mode of this VideoConfig.
        :rtype: str
        """
        return self._clip_mode

    @clip_mode.setter
    def clip_mode(self, clip_mode):
        """Sets the clip_mode of this VideoConfig.

        输出视频的剪辑方式。默认值RESIZE。 * RESIZE：视频缩放。 * CROP：视频裁剪。

        :param clip_mode: The clip_mode of this VideoConfig.
        :type clip_mode: str
        """
        self._clip_mode = clip_mode

    @property
    def codec(self):
        """Gets the codec of this VideoConfig.

        视频编码格式及视频文件格式。 * H264: h264编码，输出mp4文件 * VP8：vp8编码，输出webm文件

        :return: The codec of this VideoConfig.
        :rtype: str
        """
        return self._codec

    @codec.setter
    def codec(self, codec):
        """Sets the codec of this VideoConfig.

        视频编码格式及视频文件格式。 * H264: h264编码，输出mp4文件 * VP8：vp8编码，输出webm文件

        :param codec: The codec of this VideoConfig.
        :type codec: str
        """
        self._codec = codec

    @property
    def bitrate(self):
        """Gets the bitrate of this VideoConfig.

        输出平均码率。  单位：kbps。  最小值40，最大值30000。 > * 分身数字人视频制作采用质量优先，可能会超过设置的码率。 > * 分身数字人直播码率范围[1000, 8000]。

        :return: The bitrate of this VideoConfig.
        :rtype: int
        """
        return self._bitrate

    @bitrate.setter
    def bitrate(self, bitrate):
        """Sets the bitrate of this VideoConfig.

        输出平均码率。  单位：kbps。  最小值40，最大值30000。 > * 分身数字人视频制作采用质量优先，可能会超过设置的码率。 > * 分身数字人直播码率范围[1000, 8000]。

        :param bitrate: The bitrate of this VideoConfig.
        :type bitrate: int
        """
        self._bitrate = bitrate

    @property
    def width(self):
        """Gets the width of this VideoConfig.

        视频宽度。  单位：像素。  > * clip_mode=RESIZE时，当前支持1920x1080、1080x1920、1280x720、720x1280、3840x2160、2160x3840六种分辨率。4K分辨率视频需要分身数字人模型支持4K的情况下才能使用。 > * clip_mode=CROP，裁剪后视频，（dx,dy）为原点，保留视频像宽度为width。 > * 分身数字人直播目前只支持1080x1920。

        :return: The width of this VideoConfig.
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this VideoConfig.

        视频宽度。  单位：像素。  > * clip_mode=RESIZE时，当前支持1920x1080、1080x1920、1280x720、720x1280、3840x2160、2160x3840六种分辨率。4K分辨率视频需要分身数字人模型支持4K的情况下才能使用。 > * clip_mode=CROP，裁剪后视频，（dx,dy）为原点，保留视频像宽度为width。 > * 分身数字人直播目前只支持1080x1920。

        :param width: The width of this VideoConfig.
        :type width: int
        """
        self._width = width

    @property
    def height(self):
        """Gets the height of this VideoConfig.

        视频高度。  单位：像素。  > * clip_mode=RESIZE时，当前支持1920x1080、1080x1920、1280x720、720x1280、3840x2160、2160x3840六种分辨率分辨率。 > * clip_mode=CROP，裁剪后视频，（dx,dy）为原点，保留视频像高度为height。 > * 分身数字人直播目前只支持1080x1920。

        :return: The height of this VideoConfig.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this VideoConfig.

        视频高度。  单位：像素。  > * clip_mode=RESIZE时，当前支持1920x1080、1080x1920、1280x720、720x1280、3840x2160、2160x3840六种分辨率分辨率。 > * clip_mode=CROP，裁剪后视频，（dx,dy）为原点，保留视频像高度为height。 > * 分身数字人直播目前只支持1080x1920。

        :param height: The height of this VideoConfig.
        :type height: int
        """
        self._height = height

    @property
    def frame_rate(self):
        """Gets the frame_rate of this VideoConfig.

        帧率。  单位：FPS。 > *  分身数字人视频固定25FPS。

        :return: The frame_rate of this VideoConfig.
        :rtype: str
        """
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, frame_rate):
        """Sets the frame_rate of this VideoConfig.

        帧率。  单位：FPS。 > *  分身数字人视频固定25FPS。

        :param frame_rate: The frame_rate of this VideoConfig.
        :type frame_rate: str
        """
        self._frame_rate = frame_rate

    @property
    def is_subtitle_enable(self):
        """Gets the is_subtitle_enable of this VideoConfig.

        输出的视频是否带字幕。默认false。 > true: 打开字幕 > false: 关闭字幕

        :return: The is_subtitle_enable of this VideoConfig.
        :rtype: bool
        """
        return self._is_subtitle_enable

    @is_subtitle_enable.setter
    def is_subtitle_enable(self, is_subtitle_enable):
        """Sets the is_subtitle_enable of this VideoConfig.

        输出的视频是否带字幕。默认false。 > true: 打开字幕 > false: 关闭字幕

        :param is_subtitle_enable: The is_subtitle_enable of this VideoConfig.
        :type is_subtitle_enable: bool
        """
        self._is_subtitle_enable = is_subtitle_enable

    @property
    def subtitle_config(self):
        """Gets the subtitle_config of this VideoConfig.

        :return: The subtitle_config of this VideoConfig.
        :rtype: :class:`huaweicloudsdkmetastudio.v1.SubtitleConfig`
        """
        return self._subtitle_config

    @subtitle_config.setter
    def subtitle_config(self, subtitle_config):
        """Sets the subtitle_config of this VideoConfig.

        :param subtitle_config: The subtitle_config of this VideoConfig.
        :type subtitle_config: :class:`huaweicloudsdkmetastudio.v1.SubtitleConfig`
        """
        self._subtitle_config = subtitle_config

    @property
    def dx(self):
        """Gets the dx of this VideoConfig.

        裁剪视频左上角像素点坐标。  clip_mode= CROP时生效。 > * 以模特分辨率为画布大小，比如1920*1080分辨率的模特，dx最小值是0，最大值是1920。

        :return: The dx of this VideoConfig.
        :rtype: int
        """
        return self._dx

    @dx.setter
    def dx(self, dx):
        """Sets the dx of this VideoConfig.

        裁剪视频左上角像素点坐标。  clip_mode= CROP时生效。 > * 以模特分辨率为画布大小，比如1920*1080分辨率的模特，dx最小值是0，最大值是1920。

        :param dx: The dx of this VideoConfig.
        :type dx: int
        """
        self._dx = dx

    @property
    def dy(self):
        """Gets the dy of this VideoConfig.

        裁剪视频左上角像素点坐标。  clip_mode= CROP时生效。 > * 以模特分辨率为画布大小，比如1920*1080分辨率的模特，dy最小值是0，最大值是1080

        :return: The dy of this VideoConfig.
        :rtype: int
        """
        return self._dy

    @dy.setter
    def dy(self, dy):
        """Sets the dy of this VideoConfig.

        裁剪视频左上角像素点坐标。  clip_mode= CROP时生效。 > * 以模特分辨率为画布大小，比如1920*1080分辨率的模特，dy最小值是0，最大值是1080

        :param dy: The dy of this VideoConfig.
        :type dy: int
        """
        self._dy = dy

    @property
    def is_enable_super_resolution(self):
        """Gets the is_enable_super_resolution of this VideoConfig.

        视频是否开启超分。 > true: 开启 > false: 不开启

        :return: The is_enable_super_resolution of this VideoConfig.
        :rtype: bool
        """
        return self._is_enable_super_resolution

    @is_enable_super_resolution.setter
    def is_enable_super_resolution(self, is_enable_super_resolution):
        """Sets the is_enable_super_resolution of this VideoConfig.

        视频是否开启超分。 > true: 开启 > false: 不开启

        :param is_enable_super_resolution: The is_enable_super_resolution of this VideoConfig.
        :type is_enable_super_resolution: bool
        """
        self._is_enable_super_resolution = is_enable_super_resolution

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
        if not isinstance(other, VideoConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
