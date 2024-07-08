import logging
from typing import Dict, List, Any, Union
from pydantic import BaseModel, Field
from zcbot_web_core.lib import time as time_lib

LOGGER = logging.getLogger(__name__)


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # mongodb主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


# 插入模型
class CacheSkuPoolModel(BaseData):
    # 主键
    linkSn: str = None
    # 商品名称
    skuName: str = None
    # 选项文本
    skuOptions: str = None
    # 品牌编号
    brandId: str = None
    # 品牌名称
    brandName: str = None
    # 店铺名称
    shopName: str = None
    # 店铺类型
    shopType: str = None
    # 是否自营
    isSelf: str = None
    # 实际销售价格
    salePrice: str = None
    # 小字段（字典）
    skuAttrs: Dict[str, Any] = {}
    # 评论数
    commentCountStr: str = None
    # 主图链接
    mainImages: List = []
    # 详图链接（可选）
    detailImages: List = None

    # 商品原价（商城原价、市场价格）
    originPrice: str = None
    # 电商平台编码
    platCode: str = None
    # 电商平台名称
    platName: str = None
    # 店铺编号
    shopId: str = None
    # 型号
    brandModel: str = None
    # 规格
    specs: str = None
    # 颜色
    color: str = None
    # 单位
    unit: str = None
    # 销量
    soldCount: str = None
    # 包装参数
    packAttrs: Union[str, Dict[str, str]] = None

    # 商品标签（如：包邮、新品、厂商配送等）
    tags: List[str] = None
    # 商品链接
    url: str = None
    # 首图链接
    coverImgUrl: str = None
    # 商品状态
    status: str = None
    # 商品状态
    statusText: str = None