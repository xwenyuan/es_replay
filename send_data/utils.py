#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ISP 中文转换为英文
找不到的转为 Other
"""
import os
import json
import random
import socket
import struct
from functools import reduce
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

ISP_MAPPING = [
    {"isp": "电信", "isp_en": "China Telecom"},
    {"isp": "联通", "isp_en": "China Unicom"},
    {"isp": "移动", "isp_en": "China Mobile"},
    {"isp": "铁通", "isp_en": "China Tietong Telecom"},
    {"isp": "教育网", "isp_en": "CERNET"},
    {"isp": "鹏博士", "isp_en": "Dr. Peng"},
    {"isp": "阿里云", "isp_en": "Alibaba Cloud"},
    {"isp": "腾讯云", "isp_en": "QCloud"},
    {"isp": "广电网", "isp_en": "China Broadcasting Network"},
    {"isp": "电子政务网", "isp_en": "China E-Gov"},
    {"isp": "新国信", "isp_en": "Xin Guo Xin"},
    {"isp": "世纪互联", "isp_en": "21 Vianet"},
    {"isp": "东方有线", "isp_en": "OCN"},
    {"isp": "科技网", "isp_en": "CSTNET"},
    {"isp": "歌华有线", "isp_en": "BGCTV"},
    {"isp": "天威视讯", "isp_en": "TOPWAY"},
    {"isp": "有线通", "isp_en": "Cable The"},
    {"isp": "北龙中网", "isp_en": "KNET"},
    {"isp": "京宽网络", "isp_en": "KUANCOM"},
    {"isp": "方正宽带", "isp_en": "FounderBN"},
    {"isp": "华数", "isp_en": "WASU"},
    {"isp": "中电华通", "isp_en": "China COMM"},
    {"isp": "油田宽带", "isp_en": "China Oilfield Broadband"},
    {"isp": "屹立由", "isp_en": "YILIYOU"},
    {"isp": "中电飞华", "isp_en": "FIBRLINK"},
    {"isp": "中信网络", "isp_en": "CITIC"},
    {"isp": "三信时代", "isp_en": "CIII"},
    {"isp": "电信/骨干网/基站WiFi", "isp_en": "Chinanet"},
    {"isp": "BGP多线", "isp_en": "BGP"},
    {"isp": "阿里巴巴", "isp_en": "Alibaba"},
    {"isp": "互联网服务商联盟", "isp_en": "CNISP"},
    {"isp": "百度", "isp_en": "Baidu"},
    {"isp": "诚亿时代网络", "isp_en": "Sincerity-times"},
    {"isp": "江苏有线", "isp_en": "JSCN"},
    {"isp": "视讯宽带", "isp_en": "GDVNET"},
    {"isp": "二六三网络通信", "isp_en": "NET263"},
    {"isp": "天地祥云", "isp_en": "CloudVSP"},
    {"isp": "新网", "isp_en": "XINNET"},
    {"isp": "美团", "isp_en": "MEITUAN"},
    {"isp": "新一代/电信", "isp_en": "CT OTN"},
    {"isp": "微软", "isp_en": "Mircosoft"},
    {"isp": "网易/BGP多线", "isp_en": "NETEASE"},
    {"isp": "恒慧通信", "isp_en": "HH"},
    {"isp": "Amazon", "isp_en": "Amazon"},
    {"isp": "中企动力", "isp_en": "GROW FORCE"},
    {"isp": "鹏博士/电信", "isp_en": "Peng/CT"},
    {"isp": "方正网络", "isp_en": "FounderBN"},
    {"isp": "中兴能源", "isp_en": "ZONERGY"},
    {"isp": "有孚网络", "isp_en": "YOVOLE"},
    {"isp": "苏宁", "isp_en": "SUNING"},
    {"isp": "畅捷通信", "isp_en": "CHANJET"},
    {"isp": "新视讯", "isp_en": "CT OTN"},
    {"isp": "电信/基站WiFi", "isp_en": "CT WiFi"},
    {"isp": "睿江科技", "isp_en": "EFLY Cloud"},
    {"isp": "太平洋电信", "isp_en": "TELSTRA"},
    {"isp": "方正宽带/电信", "isp_en": "FounderBN/CT"},
    {"isp": "中国互联网络信息中心", "isp_en": "CNNIC"},
    {"isp": "国研网", "isp_en": "DRCNET"},
    {"isp": "天地网联", "isp_en": "UPNET"},
    {"isp": "中企通信", "isp_en": "CHINA ENTERCOM"},
    {"isp": "联合在线", "isp_en": "EUNCN"},
    {"isp": "蓝汛通信", "isp_en": "China Cache"},
    {"isp": "宽捷网络", "isp_en": "KUANJIE NET"},
    {"isp": "移动/基站WiFi", "isp_en": "CM/WiFi"},
    {"isp": "新飞金信", "isp_en": "XinFei JinXin"},
    {"isp": "国研科技/歌华有线", "isp_en": "SRIT/BGCTV"},
    {"isp": "地面通信息网络", "isp_en": "SHDMT NET"},
    {"isp": "光环新网/电信", "isp_en": "SINNET/CT"},
    {"isp": "华瑞信通", "isp_en": "HUARUI"},
    {"isp": "奇虎360", "isp_en": "360"},
    {"isp": "沃通电子商务", "isp_en": "WoSign"},
    {"isp": "天地通电信", "isp_en": "TianDiTong"},
    {"isp": "龙腾佳讯", "isp_en": "LongTel China"},
    {"isp": "润迅通信", "isp_en": "RUNXUN"},
    {"isp": "视虎科技", "isp_en": "Seehu"},
    {"isp": "金桥网", "isp_en": "China GBN"},
    {"isp": "网联光通", "isp_en": "NETEON"},
    {"isp": "光环迅通", "isp_en": "SINNET"},
    {"isp": "Amazon/西部云基地", "isp_en": "Amazon"},
    {"isp": "景安网络", "isp_en": "GAINET"},
    {"isp": "新浪/联通", "isp_en": "Xina/CU"},
    {"isp": "翰威科技", "isp_en": "Highway"},
    {"isp": "互联互通", "isp_en": "Linktom"},
    {"isp": "中立数据", "isp_en": "ZhongLi Data"},
    {"isp": "电联", "isp_en": "HTU"},
    {"isp": "上海大众汽车", "isp_en": "CSVW"},
    {"isp": "可口可乐网络", "isp_en": "Coca-cola"},
    {"isp": "高新翼云", "isp_en": "Wing Cloud"},
    {"isp": "华夏光网", "isp_en": "HXGW"},
    {"isp": "华北石油通信", "isp_en": "OilHB"},
    {"isp": "平煤神马集团", "isp_en": "PMJT"},
    {"isp": "信天游", "isp_en": "TRAVELSKY"},
    {"isp": "天盈信息技术", "isp_en": "51SOLE"},
    {"isp": "艾维通信", "isp_en": "CEC-CEDA"},
    {"isp": "央视", "isp_en": "CCTV"},
    {"isp": "同煤集团", "isp_en": "DTCOALMINE"},
    {"isp": "安徽省教育厅", "isp_en": "AH JYT"},
    {"isp": "中国国际电子商务中心", "isp_en": "CIECC"},
    {"isp": "盛大网络", "isp_en": "SNDA"},
    {"isp": "南凌科技", "isp_en": "NOVA"},
    {"isp": "南京信风", "isp_en": "Greatbit"},
    {"isp": "电信CN2骨干网", "isp_en": "China Telecom CN2"},
    {"isp": "联通/骨干网", "isp_en": "China Unicom"},
    {"isp": "百吉数据", "isp_en": "IDCBEST"},
    {"isp": "华数/联通", "isp_en": "WASU/CU"},
    {"isp": "UCloud云计算", "isp_en": "Ucloud"},
    {"isp": "优酷土豆", "isp_en": "Youku"},
    {"isp": "视通宽带", },
    {"isp": "卫视创捷", },
    {"isp": "新一代/联通/电信", },
    {"isp": "小鸟云", },
    {"isp": "华为", },
    {"isp": "森华易腾", },
    {"isp": "吉林油田通信", },
    {"isp": "数讯信息", },
    {"isp": "263网络通信", },
    {"isp": "互联港湾", },
    {"isp": "夏龙通信", },
    {"isp": "联想", },
    {"isp": "佰隆网络", },
    {"isp": "中国一汽", },
    {"isp": "城市网络", },
    {"isp": "联通/移动", },
    {"isp": "景安计算机网络", },
    {"isp": "壹通通信", },
    {"isp": "众屹赢时通信", },
    {"isp": "蓝讯通信技术", },
    {"isp": "爱名网络", },
    {"isp": "易速网络", },
    {"isp": "联通/网宿科技", },
    {"isp": "首信网", },
    {"isp": "舒华士", },
    {"isp": "京宽", },
    {"isp": "奥斯达通信", },
    {"isp": "网宽天地", },
    {"isp": "蓝汛通信/联通/电信", },
    {"isp": "珠江宽频/联通", "isp_en": "GZDM"},
    {"isp": "盈通网络", },
    {"isp": "燕大正洋", },
    {"isp": "斐讯", },
    {"isp": "蓝汛通信/联通/电信/移动", },
    {"isp": "青云QingCloud/电信", },
    {"isp": "网宿科技", },
    {"isp": "首都在线科技", },
    {"isp": "光环新网/联通", "isp_en": "SINNET/CU"},
    {"isp": "网易", },
    {"isp": "航数宽网", },
    {"isp": "维赛网络", },
    {"isp": "新一代/联通", },
    {"isp": "青云QingCloud/联通", },
    {"isp": "银盾泰安", },
    {"isp": "华宇宽带", },
    {"isp": "电信/联通", },
    {"isp": "上海信息网络", },
    {"isp": "爱名网", },
    {"isp": "电信/骨干网", },
    {"isp": "日升天信", },
    {"isp": "零色沸点网络", },
    {"isp": "安莱信息通信", },
    {"isp": "通慧网联", },
    {"isp": "光环新网", "isp_en": "SINNET"},
    {"isp": "云方舟", },
    {"isp": "众生网络", },
    {"isp": "新一代/电信/联通", },
    {"isp": "中电飞华/联通", },
    {"isp": "润泽科技", },
    {"isp": "京东", "isp_en": "JD"},
    {"isp": "金山在线", "isp_en": "SPC365"},
    {"isp": "安畅网络", },
    {"isp": "小鸟云/电信/联通", },
    {"isp": "奇虎360/电信", },
    {"isp": "广西视虎", },
    {"isp": "铜牛", "isp_en": "Topnew"},
    {"isp": "临网通讯", },
    {"isp": "联通/电信", },
    {"isp": "鹏博士/联通", },
    {"isp": "奇虎360/电信/联通", },
    {"isp": "金科信息网", },
    {"isp": "公云PubYun/电信", },
    {"isp": "中原油田", },
    {"isp": "湖南有线/联通", },
    {"isp": "电信/网宿科技", },
    {"isp": "博路电信", },
    {"isp": "星缘新动力", },
    {"isp": "网宿科技/BGP多线", },
    {"isp": "通科信息技术", },
    {"isp": "滴滴", "isp_en": "DD"},
    {"isp": "世纪互联/电信/移动", },
    {"isp": "腾讯", "isp_en": "Tencent"},
    {"isp": "企商在线", },
    {"isp": "安畅", },
    {"isp": "浙江日报", },
    {"isp": "犀思云", },
    {"isp": "网银互联", "isp_en": "Netbank"},
    {"isp": "奇虎360/联通", },
    {"isp": "网宿科技/联通", },
    {"isp": "银澎百盛云计算", },
    {"isp": "祥达信", "isp_en": "STI"},
    {"isp": "华云数据", },
    {"isp": "中科鸿基", },
    {"isp": "龙江网络", },
    {"isp": "云端时代", },
    {"isp": "首都在线/电信", },
    {"isp": "全时", },
    {"isp": "爱奇艺", "isp_en": "iQiYi"},
    {"isp": "中联讯通", },
    {"isp": "联通/基站WiFi", },
    {"isp": "新觉互联", },
    {"isp": "凤凰新媒体", },
    {"isp": "中基电信石油通信", },
    {"isp": "华通宽带", },
    {"isp": "蓝芒科技", },
    {"isp": "飞华领航", },
    {"isp": "中国石油", },
    {"isp": "润迅数据", },
    {"isp": "美团/联通/电信", },
    {"isp": "康盛新创", },
    {"isp": "中关村软件园", },
    {"isp": "谷歌/电信", },
    {"isp": "景安/IDC", },
    {"isp": "新一代", },
    {"isp": "中国邮政", },
    {"isp": "新一代/鹏博士/联通/电信", },
    {"isp": "天维信通", },
    {"isp": "欧网网络", },
    {"isp": "光明网", },
    {"isp": "中经网", },
    {"isp": "经天科技", },
    {"isp": "云方舟/电信/联通", },
    {"isp": "奥飞数据", },
    {"isp": "纵横信息", },
    {"isp": "信盈恒泰", },
    {"isp": "戴鑫云", },
    {"isp": "三星", },
    {"isp": "万通电讯", },
    {"isp": "优酷土豆/BGP多线", },
    {"isp": "平安科技", },
    {"isp": "松江科技", },
    {"isp": "互联通", },
    {"isp": "新世纪资通", },
    {"isp": "日升科技", },
    {"isp": "亚马逊", "isp_en": "Amazon"},
    {"isp": "龙腾网络", },
    {"isp": "慧聪网", },
    {"isp": "润迅通信/BGP多线/电信", "isp_en": "QingCloud/BGP/CT"},
    {"isp": "紫田网络", },
    {"isp": "文物信息咨询中心", },
    {"isp": "北京IDC", },
    {"isp": "土豆", },
    {"isp": "天广信息通信", },
    {"isp": "东南广播电视网络", },
    {"isp": "中国科技馆", },
    {"isp": "天网在线", },
    {"isp": "青云QingCloud/BGP多线", "isp_en": "QingCloud/BGP"},
    {"isp": "宝马", },
    {"isp": "新一代/鹏博士/联通", },
    {"isp": "云方舟/联通", },
    {"isp": "新浪/电信", },
    {"isp": "迅达云", },
    {"isp": "优酷土豆/教育网", },
    {"isp": "嘉华网络", },
    {"isp": "中国免税品（集团）", },
    {"isp": "唯一网络", },
    {"isp": "神威迅腾", },
    {"isp": "高升科技", },
    {"isp": "百优科技", },
    {"isp": "艾亚网络", },
    {"isp": "亿人互联", },
    {"isp": "百度云加速/电信", "isp_en": "Baidu Cloud/CT"},
    {"isp": "优酷土豆/电信", "isp_en": "Youku/CT"},
    {"isp": "祥达信/联通", "isp_en": "STI/CU"},
    {"isp": "益博睿", },
    {"isp": "百度云加速/联通", },
    {"isp": "优酷土豆/联通", },
    {"isp": "英特尔", "isp_en": "Intel"},
    {"isp": "易信科技", },
    {"isp": "云港讯通", "isp_en": "CNNIX"},
    {"isp": "中经云", },
    {"isp": "中海宽带", },
    {"isp": "丽水杰世", },
    {"isp": "平煤集团", },
    {"isp": "世纪互联/移动", "isp_en": "21 Vianet/CM"},
    {"isp": "西部数码", },
    {"isp": "宝联科技", },
    {"isp": "阿比酷", },
    {"isp": "高新翼云科技", },
    {"isp": "PubYun公云", },
    {"isp": "昆时网络", },
    {"isp": "睿廷网络", },
    {"isp": "蒲公英网络/BGP阻断国外/IDC", },
    {"isp": "蒲公英网络/联通/IDC", },
    {"isp": "世通在线", },
    {"isp": "网鼎科技", },
    {"isp": "天成网络", },
    {"isp": "沃尔玛", },
    {"isp": "聚友集团", },
    {"isp": "有家网络", },
    {"isp": "数据家/联通", },
    {"isp": "宁波高防", },
    {"isp": "快云电信", },
    {"isp": "华夏雅库网络", },
    {"isp": "蚂蚁金服", },
    {"isp": "帝联科技", },
    {"isp": "方正宽带/联通", },
    {"isp": "华通云数据", },
    {"isp": "蓝队网络", },
    {"isp": "神州云/电信", },
    {"isp": "奇虎360/移动", "isp_en": "360/CM"},
    {"isp": "祥达信/铁通", "isp_en": "STI/CTT"},
    {"isp": "中企通信/联通/电信", "isp_en": "CHINA ENTERCOM/CU/CT"},
    {"isp": "火亿互联", },
    {"isp": "华夏联动", },
    {"isp": "环球网", },
    {"isp": "华晨宝马", },
    {"isp": "海联信息", },
    {"isp": "rixCloud", },
    {"isp": "DNSPod", },
    {"isp": "Gap品牌", },
    {"isp": "IDC", },
    {"isp": "阿帕云", },
    {"isp": "比通联合网络", },
    {"isp": "承启通", },
    {"isp": "天地祥云/联通", "isp_en": "CloudVSP/CU"},
    {"isp": "腾讯云/DNSPod", },
    {"isp": "蘑菇主机", },
    {"isp": "蒲公英网络/BGP/IDC", },
    {"isp": "朗为数据", },
    {"isp": "联动天翼", },
    {"isp": "联华世纪", },
    {"isp": "上海双于", },
    {"isp": "华普在线", },
    {"isp": "汇通信安", },
    {"isp": "光通朗迅", },
    {"isp": "海视泰数据", },
    {"isp": "红豆集团", },
    {"isp": "第一线", },
    {"isp": "烽火通信", },
    {"isp": "维速", },
    {"isp": "中信", },
    {"isp": "友普信息", },
    {"isp": "蒲公英网络/电信/IDC", },
    {"isp": "乐视", },
    {"isp": "上海文德", },
    {"isp": "赛格网络", },
    {"isp": "数凹科技", },
    {"isp": "太极", },
    {"isp": "聚友网络", },
    {"isp": "华胜天成", },
    {"isp": "杭州赞云", },
    {"isp": "光联集团", },
    {"isp": "二六三网络/联通", },
    {"isp": "力通网络", },
    {"isp": "云瑞智通", },
    {"isp": "迅雷", },
    {"isp": "逸云科技", },
    {"isp": "中金数据系统", },
    {"isp": "中光电信", },
    {"isp": "云方舟/电信", },
    {"isp": "信思贤/IDC", },
    {"isp": "网宿科技/联通/电信", },
    {"isp": "东方网信", "isp_en": "NETEAST"},
    {"isp": "光明都市传媒", },
    {"isp": "华数/电信", "isp_en": "WASU/CT"},
    {"isp": "OPPO", "isp_en": "OPPO"},
    {"isp": "八度网络", "isp_en": "EBADU"},
    {"isp": "船舶通信导航", "isp_en": "SCN"},
    {"isp": "沃通", "isp_en": "WoTrus"},
    {"isp": "曦光科技", "isp_en": "SHUGUANG"},
    {"isp": "云林网络", "isp_en": "YUNLIN"},
    {"isp": "上海纵智", "isp_en": "NISNET"},
    {"isp": "世纪东方", "isp_en": "51WEB"},
    {"isp": "瑞兆", "isp_en": "RUIZHAO"},
    {"isp": "企商在线/联通", "isp_en": "NETNIC/CU"},
    {"isp": "汽车之家", "isp_en": "AutoHome"},
    {"isp": "青云QingCloud", "isp_en": "QingCloud"},
    {"isp": "联华世纪/IDC", "isp_en": "LINKCHINA/IDC"},
    {"isp": "麦格纳", "isp_en": "Magna"},
    {"isp": "环球航通", "isp_en": "VSAT"},
    {"isp": "葵芳IDC", "isp_en": "ChinahkIDC"},
    {"isp": "优酷土豆/移动", "isp_en": "YILIYOU/CM"},
    {"isp": "电信通", "isp_en": "Beijing Teletron"},
    {"isp": "中国在线", "isp_en": "China Daily"},
    {"isp": "天地祥云/铁通", "isp_en": "CloudVSP/CTT"},
    {"isp": "奇虎360蜘蛛/联通", "isp_en": "360/CU"},
    {"isp": "奇虎360/教育网", "isp_en": "360/CERNET"},
    {"isp": "百度云加速/移动", "isp_en": "Baidu Cloud/CM"},
    {"isp": "科技网/联通", "isp_en": "CSTNET/CU"},
    {"isp": "联想调频科技", "isp_en": "Lenovo"},
    {"isp": "峰鸟云", "isp_en": "FengNiaoYun"},
    {"isp": "安畅/电信", "isp_en": "ANCHNET/CT"},
    {"isp": "世博科技", "isp_en": "SHIBO"},
    {"isp": "阿里云/DNS", "isp_en": "Alibaba Cloud/DNS"},
    {"isp": "网宿科技/电信", "isp_en": "WANGSU/CT"},
    {"isp": "阿里云DNS", "isp_en": "Alibaba Cloud/DNS"},
    {"isp": "百度云加速/BGP多线", "isp_en": "Baidu Cloud/BGP"},
    {"isp": "世纪互联/联通", "isp_en": "21 Vianet/CU"},
    {"isp": "国信比林", "isp_en": "Beijing Teletron"},
    {"isp": "政务和公益机构域名注册管理中心", "isp_en": "CONAC"},
    {"isp": "祥达信/电信", "isp_en": "STI/CT"},
    {"isp": "新浪/移动", "isp_en": "Xinna/CM"},
    {"isp": "天互数据/电信/IDC", "isp_en": "IDCS/CT/IDC"},
    {"isp": "百度云加速/天互数据/电信/IDC", "isp_en": "Baidu Cloud/IDCS/CT/IDC"},
    {"isp": "众达科技", "isp_en": "PCL Technologies"},
    {"isp": "优酷土豆/铁通", "isp_en": "TOUKU/CTT"},
    {"isp": "奇虎360蜘蛛/电信", "isp_en": "360/CT"},
    {"isp": "科安德网络", "isp_en": "CANDIS"},
    {"isp": "BBTEC", "isp_en": "BBTEC"},
    {"isp": "电信/DNS", "isp_en": "CT/DNS"},
    {"isp": "NTT/骨干网", "isp_en": "NTT"},
    {"isp": "AliDNS", "isp_en": "AliDNS"},
    {"isp": "114DNS", "isp_en": "114DNS"},
    {"isp": "SDNS", "isp_en": "SDNS"},
    {"isp": "CTDNS", "isp_en": "CTDNS"},
    {"isp": "奇虎360/蓝汛通信/联通/电信", "isp_en": "360/CC/CU/CT"},
    {"isp": "奇虎360/鹏博士/电信/联通", "isp_en": "360/Peng/CT/CU/"},
    {"isp": "苹果", "isp_en": "Apple"},
    {"isp": "Akamai", "isp_en": "Akamai"},
    {"isp": "谷歌", "isp_en": "Google"},
    {"isp": "Cloudflare", "isp_en": "Cloudflare"},
    {"isp": "ORACLE", "isp_en": "ORACLE"},
    {"isp": "Amazon/GlobalCloudFront", "isp_en": "Amazon/GlobalCloudFront"},
    {"isp": "電訊盈科", "isp_en": "PCCW"},
    {"isp": "NTT", "isp_en": "NTT"},
    {"isp": "Verizon", "isp_en": "Verizon"},
    {"isp": "SoftLayer", "isp_en": "SoftLayer"},
    {"isp": "Facebook", "isp_en": "Facebook"},
    {"isp": "Telia", "isp_en": "Telia"},
    {"isp": "IBM SoftLayer", "isp_en": "IBM SoftLayer"},
    {"isp": "AT&T", "isp_en": "AT&T"},
    {"isp": "Zenlayer", "isp_en": "Zenlayer"},
    {"isp": "Telstra", "isp_en": "Telstra"},
    {"isp": "亚太环通/Pacnet", "isp_en": "Pacnet"},
    {"isp": "PetaExpress", "isp_en": "PetaExpress"},
    {"isp": "GTT", "isp_en": "GTT"},
    {"isp": "Twitter", "isp_en": "Twitter"},
    {"isp": "雅虎", "isp_en": "Yahoo"},
    {"isp": "OpenDNS", "isp_en": "OpenDNS"},
    {"isp": "亚太环通/Pacnet/骨干网", "isp_en": "Pacnet"},
    {"isp": "Cloudflare/CDN", "isp_en": "Cloudflare/CDN"},
    {"isp": "EdgeCast", "isp_en": "EdgeCast"},
    {"isp": "Amazon/CloudFront", "isp_en": "Amazon/CloudFront"},
    {"isp": "CloudDNS", "isp_en": "CloudDNS"},
    {"isp": "GTT/骨干网", "isp_en": "GTT"},
    {"isp": "PDR", "isp_en": "PDR"},
    {"isp": "APNIC-LABS", "isp_en": "APNIC-LABS"},
    {"isp": "BICS", "isp_en": "BICS"},
    {"isp": "Vodafone", "isp_en": "Vodafone"},
    {"isp": "V2exDNS", "isp_en": "V2exDNS"},
    {"isp": "GoogleDNS", "isp_en": "GoogleDNS"},

]


def isp2en(isp_name):
    matched_items = filter(lambda x: isp_name in x['isp'], ISP_MAPPING)
    if len(matched_items) > 0:
        return matched_items[0].get('isp_en', 'Other')
    else:
        return 'Other'


if __name__ == "__main__":
    print(isp2en('阿里'))
