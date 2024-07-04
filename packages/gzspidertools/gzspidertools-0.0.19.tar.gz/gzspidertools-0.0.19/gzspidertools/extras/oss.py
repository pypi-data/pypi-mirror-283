import warnings
from typing import Any, Optional

from retrying import retry

from gzspidertools.common.params import Param

try:
    import oss2
except ImportError:
    # pip install gzspidertools[all]
    pass

warnings.filterwarnings("ignore")

__all__ = [
    "AliOssBase",
]


class AliOssBase:
    """阿里云 Oss 对象存储 python sdk 示例
    其 GitHub 官方文档地址：
        https://github.com/aliyun/aliyun-oss-python-sdk
    阿里云官方 oss sdk 文档地址：
        https://www.alibabacloud.com/help/zh/oss/developer-reference
    """

    def __init__(
        self,
        access_key: str,
        access_secret: str,
        endpoint: str,
        bucket: str,
        doc: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """初始化 auth，bucket 等信息

        Args:
            access_key: 阿里云账号 AccessKey
            access_secret: 阿里云账号 AccessKey 对应的秘钥
            endpoint: 填写 Bucket 所在地域对应的 Endpoint；
                以华东1（杭州）为例，Endpoint 填写为 https://oss-cn-hangzhou.aliyuncs.com
            bucket: 填写 Bucket 名称，此 oss 项目所属 bucket
            doc: 需要操作的 oss 文件夹目录，比如 file/img，可选参数
        """
        self.endpoint = endpoint
        self.doc = doc
        self.auth = oss2.Auth(access_key, access_secret)
        self.bk = bucket
        self.bucket = oss2.Bucket(self.auth, f"{self.endpoint}/", bucket)
        self.headers = {"Connection": "close"}

    @retry(stop_max_attempt_number=Param.retry_num)
    def put_oss(
        self,
        put_bytes: bytes,
        file: str,
    ) -> None:
        """上传单个文件的 bytes 内容

        Args:
            put_bytes: 需要上传的文件 bytes 内容或链接
            file: 需要上传的文件的名称

        Returns:
            None
        """
        assert isinstance(put_bytes, bytes), "put_bytes 需要是 bytes 格式"

        oss_file_path = f"{self.doc}/{file}" if self.doc else file
        self.bucket.put_object(oss_file_path, put_bytes)
