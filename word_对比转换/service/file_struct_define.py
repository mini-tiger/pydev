from abc import ABC, abstractmethod


class Base_Cls(ABC):
    @abstractmethod
    def page_define(self, index=None, value=None) -> int:
        return 0

    @abstractmethod
    def part_define(self, index=None, value=None) -> str:
        return ""


class Base_method(Base_Cls):
    reserved = False
    dyx = False

    def page_define(self, index=None, value=None) -> int:
        return 0

    def part_define(self, index=None, value=None) -> str:
        return ""


class dyx_unstd_unreserved(Base_Cls):
    reserved = False
    dyx = True

    def page_define(self, index=None, value=None) -> int:
        page = value.metadata.page_number

        if index >= 15 and index < 53:
            page = 2
        if index >= 53 and index < 67:
            page = 3
        if index >= 67 and index < 94:
            page = 4
        if index >= 94 and index < 115:
            page = 5
        if index >= 115 and index < 133:
            page = 6
        if index >= 133 and index < 165:
            page = 7
        if index >= 165 and index < 179:
            page = 8
        if index >= 179 and index < 204:
            page = 9
        if index >= 204 and index < 226:
            page = 10
        if index >= 226 and index < 246:
            page = 11
        if index >= 246 and index < 272:
            page = 12
        if index >= 272 and index < 291:
            page = 13
        return page

    def part_define(self, index=None, value=None) -> str:
        part = ""

        if index > 15 and index < 53:
            part = "互联网信息安全责任书"

        if index >= 53 and index < 67:
            part = "网站备案义务告知书"

        if index >= 67 and index < 81:
            part = "1 概述"

        if index >= 81 and index < 96:
            part = "2.1	服务定义"

        if index >= 96 and index < 132:
            part = "2.2	服务产品类型"

        if index >= 132 and index < 162:
            part = "2.3	服务标准"
        if index == 162:
            part = "2.4	服务中断罚则"
        if index == 163:
            part = "2.4	服务中断罚则 小节中的表格"
        if index >= 163 and index < 171:
            part = "3. 设备的交接、合理使用及保管"
        if index >= 171 and index < 177:
            part = "4. 技术服务与支持"
        if index >= 177 and index < 224:
            part = "5. 用户方权利与义务"
        if index >= 224 and index < 234:
            part = "6. 服务方权利和义务"
        if index >= 234 and index < 241:
            part = "7. 服务安全与紧急避险"
        if index >= 241 and index < 246:
            part = "8. 赔偿及提前解约违约金"
        if index >= 246 and index < 256:
            part = "9. 除外责任"
        if index >= 256 and index < 258:
            part = "10. 保密和知识产权"
        if index >= 258 and index < 260:
            part = "11. 不可抗力及免责"
        if index >= 260 and index < 262:
            part = "12. 法律适用和争议解决"
        if index >= 262 and index < 272:
            part = "13. 协议生效及其他"
        return part


class dyx_unstd_reserved(Base_Cls):
    reserved = True
    dyx = True

    def page_define(self, index=None, value=None) -> int:
        page = value.metadata.page_number

        if index >= 15 and index < 53:
            page = 2
        if index >= 53 and index < 68:
            page = 3
        if index >= 68 and index < 94:
            page = 4
        if index >= 94 and index < 115:
            page = 5
        if index >= 115 and index < 133:
            page = 6
        if index >= 133 and index < 165:
            page = 7
        if index >= 165 and index < 181:
            page = 8
        if index >= 181 and index < 206:
            page = 9
        if index >= 206 and index < 227:
            page = 10
        if index >= 227 and index < 248:
            page = 11
        if index >= 248 and index < 275:
            page = 12
        if index >= 275 and index < 292:
            page = 13
        return page

    def part_define(self, index=None, value=None) -> str:
        part = ""

        if index >= 15 and index < 53:
            part = "互联网信息安全责任书"

        if index >= 53 and index < 68:
            part = "网站备案义务告知书"

        if index >= 68 and index <= 85:
            part = "1 概述"

        if index >= 85 and index < 99:
            part = "2.1	服务定义"

        if index >= 99 and index < 136:
            part = "2.2	服务产品类型"

        if index >= 136 and index < 165:
            part = "2.3	服务标准"
        if index >= 165 and index < 168:
            part = "2.4	服务中断罚则"
        if index == 168:
            part = "2.4	服务中断罚则 小节中的表格"
        if index >= 169 and index < 175:
            part = "3. 设备的交接、合理使用及保管"
        if index >= 175 and index < 181:
            part = "4. 技术服务与支持"
        if index >= 181 and index < 229:
            part = "5. 用户方权利与义务"
        if index >= 229 and index < 238:
            part = "6. 服务方权利和义务"
        if index >= 238 and index < 245:
            part = "7. 服务安全与紧急避险"
        if index >= 245 and index < 251:
            part = "8. 赔偿及提前解约违约金"
        if index >= 251 and index < 260:
            part = "9. 除外责任"
        if index >= 260 and index < 262:
            part = "10. 保密和知识产权"
        if index >= 262 and index < 264:
            part = "11. 不可抗力及免责"
        if index >= 264 and index < 266:
            part = "12. 法律适用和争议解决"
        if index >= 266 and index < 280:
            part = "13. 协议生效及其他"
        return part


class undyx_unstd_unreserved(Base_Cls):
    reserved = False
    dyx = False

    def page_define(self, index=None, value=None) -> int:
        page = value.metadata.page_number

        if index >= 15 and index < 56:
            page = 2
        if index >= 56 and index < 71:
            page = 3
        if index >= 71 and index < 98:
            page = 4
        if index >= 98 and index < 118:
            page = 5
        if index >= 118 and index < 136:
            page = 6
        if index >= 136 and index < 166:
            page = 7
        if index >= 166 and index < 183:
            page = 8
        if index >= 183 and index < 206:
            page = 9
        if index >= 206 and index < 229:
            page = 10
        if index >= 229 and index < 248:
            page = 11
        if index >= 248 and index < 274:
            page = 12
        if index >= 274 and index < 291:
            page = 13
        return page

    def part_define(self, index=None, value=None) -> str:
        part = ""

        if index > 15 and index < 56:
            part = "互联网信息安全责任书"

        if index >= 56 and index < 71:
            part = "网站备案义务告知书"

        if index >= 71 and index <= 87:
            part = "1 概述"

        if index >= 88 and index < 102:
            part = "2.1	服务定义"

        if index >= 102 and index < 134:
            part = "2.2	服务产品类型"

        if index >= 134 and index < 164:
            part = "2.3	服务标准"
        if index >= 164 and index < 165:
            part = "2.4	服务中断罚则"
        if index == 166:
            part = "2.4	服务中断罚则 小节中的表格"
        if index >= 167 and index < 173:
            part = "3. 设备的交接、合理使用及保管"
        if index >= 173 and index < 179:
            part = "4. 技术服务与支持"
        if index >= 179 and index < 226:
            part = "5. 用户方权利与义务"
        if index >= 226 and index < 236:
            part = "6. 服务方权利和义务"
        if index >= 236 and index < 243:
            part = "7. 服务安全与紧急避险"
        if index >= 243 and index < 248:
            part = "8. 赔偿及提前解约违约金"
        if index >= 248 and index < 258:
            part = "9. 除外责任"
        if index >= 258 and index < 260:
            part = "10. 保密和知识产权"
        if index >= 260 and index < 262:
            part = "11. 不可抗力及免责"
        if index >= 262 and index < 264:
            part = "12. 法律适用和争议解决"
        if index >= 264 and index < 274:
            part = "13. 协议生效及其他"
        return part


class undyx_unstd_reserved(Base_Cls):
    reserved = True
    dyx = False

    def page_define(self, index=None, value=None) -> int:
        page = value.metadata.page_number

        if index >= 15 and index < 56:
            page = 2
        if index >= 56 and index < 71:
            page = 3
        if index >= 71 and index < 98:
            page = 4
        if index >= 98 and index < 118:
            page = 5
        if index >= 118 and index < 136:
            page = 6
        if index >= 136 and index < 166:
            page = 7
        if index >= 166 and index < 183:
            page = 8
        if index >= 183 and index < 206:
            page = 9
        if index >= 206 and index < 229:
            page = 10
        if index >= 229 and index < 248:
            page = 11
        if index >= 248 and index < 274:
            page = 12
        if index >= 274 and index < 286:
            page = 13
        return page

    def part_define(self, index=None, value=None) -> str:
        part = ""

        if index > 15 and index < 56:
            part = "互联网信息安全责任书"

        if index >= 56 and index < 71:
            part = "网站备案义务告知书"

        if index >= 71 and index <= 86:
            part = "1 概述"

        if index >= 86 and index < 102:
            part = "2.1	服务定义"

        if index >= 102 and index < 134:
            part = "2.2	服务产品类型"

        if index >= 134 and index < 165:
            part = "2.3	服务标准"
        if index == 165:
            part = "2.4	服务中断罚则"
        if index == 166:
            part = "2.4	服务中断罚则 小节中的表格"
        if index >= 167 and index < 173:
            part = "3. 设备的交接、合理使用及保管"
        if index >= 173 and index < 179:
            part = "4. 技术服务与支持"
        if index >= 179 and index < 226:
            part = "5. 用户方权利与义务"
        if index >= 226 and index < 236:
            part = "6. 服务方权利和义务"
        if index >= 236 and index < 243:
            part = "7. 服务安全与紧急避险"
        if index >= 243 and index < 248:
            part = "8. 赔偿及提前解约违约金"
        if index >= 248 and index < 258:
            part = "9. 除外责任"
        if index >= 258 and index < 260:
            part = "10. 保密和知识产权"
        if index >= 260 and index < 262:
            part = "11. 不可抗力及免责"
        if index >= 262 and index < 264:
            part = "12. 法律适用和争议解决"
        if index >= 264 and index < 274:
            part = "13. 协议生效及其他"
        return part
