from django.db import models
from system.models import Evaluate


class Customer(models.Model):
    '''客户单位信息'''
    chocontext = (("1", "党政机关"), ("2", "国家重要行业、重要领域或重要企事业单位"), ("3", "一般企事业单位"), ("4", "其他类型"))
    unit_name = models.CharField(max_length=30, verbose_name='单位名称')
    company_profile = models.TextField(max_length=300, verbose_name='单位简介')
    address = models.CharField(max_length=255, verbose_name='单位地址')
    nature = models.CharField(max_length=30, verbose_name='单位性质', choices=chocontext)
    code = models.CharField(max_length=30, verbose_name='邮编')
    department = models.CharField(max_length=30, verbose_name='部门')
    superdepar = models.CharField(max_length=30, verbose_name='上级主管部门')
    user = models.ForeignKey('system.UserInfo', on_delete=models.CASCADE, verbose_name='单位与添加人员关联表')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name_plural = '客户单位信息表'
        # managed = False

    def get_user(self):
        return self.user.username

    @staticmethod
    def get_title_list():
        return ["{单位全称}", "{单位情况简介}", "{单位地址}", "{单位所属类型}", "{邮政编码}", "{所属部门}", "{上级主管部门}"]


class CUserInfo(models.Model):
    '''客户方联系人信息'''
    name = models.CharField(max_length=30, verbose_name='联系人名字')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    post = models.CharField(max_length=30, verbose_name='岗位')
    phone = models.CharField(max_length=11, verbose_name='电话号码')
    telephone = models.CharField(max_length=11, verbose_name='手机')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    nameinfo = models.ForeignKey(Customer, verbose_name='单位联系人和单位关联表', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_user(self):
        return self.nameinfo.user.username

    class Meta:
        verbose_name_plural = '客户方联系人信息'
        # managed = False

    @staticmethod
    def get_title_list():
        return ["{联系人姓名}", "{电子邮箱}", "{职务}", "{联系方式手机}", "{联系方式电话}"]


class GmanagerInfo(models.Model):
    '''客户方负责人的信息'''
    gmanager = models.CharField(max_length=30, verbose_name='负责人名字')
    gphone = models.CharField(max_length=11, verbose_name='负责人办公电话')
    gtelephone = models.CharField(max_length=11, verbose_name='负责人手机')
    gpost = models.CharField(max_length=30, verbose_name='负责人岗位')
    gemail = models.EmailField(max_length=100, verbose_name='负责人邮箱')

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    gnameinfo = models.ForeignKey(Customer, verbose_name='单位负责人和单位关联表', on_delete=models.CASCADE)

    def __str__(self):
        return self.gmanager

    def get_user(self):
        return self.gnameinfo.user.username

    class Meta:
        verbose_name_plural = '客户方负责人信息'
        # managed = False

    @staticmethod
    def get_title_list():
        return ["{负责人}", "{负责人办公电话}", "{负责人移动电话}", "{负责人职务}", "{负责人电子邮件}"]


class ProInfo(models.Model):
    '''系统信息表'''
    proname = models.CharField(max_length=30, verbose_name='项目名称')
    agentname = models.CharField(max_length=30, verbose_name='中间商单位名称', blank=True, null=True)
    sys_name = models.CharField(max_length=30, verbose_name='系统名称')
    level = models.CharField(max_length=20, verbose_name='系统级别', choices=(
        ('1', 'S2A2G2'), ('2', 'S2A1G2'), ('3', 'S1A2G2'), ('4', 'S3A3G3'), ('5', 'S3A2G3'), ('6', 'S2A3G3')))
    sys_service = models.CharField(max_length=30, verbose_name='系统服务性质',
                                   choices=(('1', '业务专网'), ('2', '互联网'), ('3', '其他')))
    sys_obj = models.CharField(max_length=20, verbose_name='系统服务对象',
                               choices=(('1', '单位内部人员'), ('2', '社会公众人员'), ('3', '二者均包括'), ('4', '其他')))
    pro_num = models.CharField(max_length=30, verbose_name='项目编号', blank=True, null=True)
    Record_num = models.CharField(max_length=100, verbose_name='备案编号', blank=True, null=True)
    pm = models.CharField(max_length=100, verbose_name='项目经理')
    supervisor = models.CharField(max_length=100, verbose_name='监督人')
    reporter_pro = models.CharField(max_length=100, verbose_name='汇报人')
    supervisored = models.CharField(max_length=100, verbose_name='被监督人')
    desc = models.CharField(max_length=255, verbose_name='业务描述')

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    proinfo = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='项目和客户单位管理表')

    def __str__(self):
        return self.pro_num

    def get_user(self):
        return self.proinfo.user.username

    @staticmethod
    def get_title_list():
        return ["{项目名称}", "{中间商}", "{系统名称}",
                "{对应级别}", "{系统网络性质}", "{系统服务对象}",
                "{项目编号}", "{备案证明编号}", "{项目经理}", "{监督人}",
                "{汇报人}", "{被监督人}", "{业务描述}"]

    class Meta:
        verbose_name_plural = '项目信息表'
        # managed = False


class BonusUnit(models.Model):
    '''奖金单位表'''
    a = (("1", '李海燕'), ("2", '段圣雄'), ("3", '朱贇'), ("4", '苏钰淇'), ("5", '银鹰'),
         ("6", '张鑫'), ("7", '金俊'), ("8", '颜星晨'), ("9", '王栋'), ("10", '杨华'), ("11", '侍国亮'),
         ("12", '张保稳'), ("13", '张全海'), ("14", '陈秀真'), ("15", '周志洪'), ("16", '夏正敏'), ("17", '沈瑜'))
    nature = models.CharField(max_length=30, verbose_name='系统性质', choices=(('安全测评', '安全测评'), ('等保测评', '等保测评')))
    unit = models.CharField(max_length=100, verbose_name='单位名称')
    # bonus = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='税前奖金')
    bonus = models.CharField(max_length=255, verbose_name='税前奖金')
    pm = models.CharField(max_length=30, verbose_name='项目经理', choices=a)
    sale = models.CharField(max_length=30, verbose_name='商务', choices=a)
    contract_pdf = models.FileField(upload_to='contract_pdf', null=True, blank=True, verbose_name='合同文件')
    remarks = models.CharField(max_length=255, verbose_name='备注')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    bonus_pro = models.OneToOneField(to='ProInfo', verbose_name='关联项目', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey('system.UserInfo', on_delete=models.CASCADE, verbose_name='用户')

    def __str__(self):
        return self.unit

    @staticmethod
    def get_title_list():
        return ["单位性质", "单位名称", "奖金金额", "项目经理", "商务经理", '备注']

    class Meta:
        verbose_name_plural = '奖金单位表'
        # managed = False


class BonusSystem(models.Model):
    choices = (('1', 'S2A2G2'), ('2', 'S2A1G2'), ('3', 'S1A2G2'), ('4', 'S3A3G3'), ('5', 'S3A2G3'), ('6', 'S2A3G3'))
    system = models.CharField(max_length=100, verbose_name='系统名称')
    level = models.CharField(max_length=30, verbose_name='系统级别', choices=choices)
    completion_time = models.DateField(blank=True, null=True, verbose_name='项目完成时间')
    bonusunit = models.ForeignKey('BonusUnit', on_delete=models.CASCADE, verbose_name='奖金单位表')

    def __str__(self):
        return self.system

    @staticmethod
    def get_title_list():
        return ["系统名称", "系统级别", "完成时间"]

    class Meta:
        verbose_name_plural = '奖金系统表'


class ProDate(models.Model):
    '''被测系统测评时间'''
    apply = models.CharField(max_length=32, verbose_name='测评申请书')
    accept = models.CharField(max_length=32, verbose_name='文档接受清单')
    formalization = models.CharField(max_length=32, verbose_name='形式化审查意见')
    contract = models.CharField(max_length=32, verbose_name='测评服务合同')
    secret = models.CharField(max_length=32, verbose_name='保密协议')
    authorization = models.CharField(max_length=32, verbose_name='授权委托书')

    task = models.CharField(max_length=32, verbose_name='项目任务书')
    question = models.CharField(max_length=32, verbose_name='基本信息调查表')
    scheme = models.CharField(max_length=32, verbose_name='方案编制')
    schemereview = models.CharField(max_length=32, verbose_name='方案评审')

    firstmeeting = models.CharField(max_length=32, verbose_name='首次会议')
    onsiteevalaation = models.CharField(max_length=32, verbose_name='现场测评授权书')
    record = models.CharField(max_length=32, verbose_name='安全等级测评记录表 ')
    test = models.CharField(max_length=32, verbose_name='检验监督记录')
    lasttmeeting = models.CharField(max_length=32, verbose_name='末次会议')

    reporter_date = models.CharField(max_length=32, verbose_name='测评报告')
    reporterview = models.CharField(max_length=32, verbose_name='测评报告评审')
    acceptreporter = models.CharField(max_length=32, verbose_name='测评报告接收单')
    agreen = models.CharField(max_length=32, verbose_name='客户满意度问卷调查')

    unit = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='时间和客户单位关系表')

    def get_user(self):
        return self.unit.user.username

    def __str__(self):
        return self.unit

    @staticmethod
    def get_title_list():
        return ["{测评申请书日期}", "{文档接受清单日期}", "{形式化审查意见时间}", "{测评服务合同}", "{保密协议}", "{授权委托书}",
                "{项目任务书实验室主任签字时间}", "{基本信息调查表}", "{方案编制时间}", "{方案评审时间}",
                "{首次会议签到、纪要表时间}", "{现场测评授权书签字时间}", "{安全等级测评记录表签字时间}", "{监督日期}", "{末次会议签到、纪要表时间}",
                "{测评报告时间}", '{报告评审时间}', "{测评报告接受单}", "{客户满意度问卷调查表时间}"]

    class Meta:
        verbose_name_plural = '项目时间表'


class Djcp(models.Model):
    customer = models.ForeignKey(to='Customer', verbose_name='单位', on_delete=models.CASCADE)
    proInfo = models.ForeignKey(to='ProInfo', verbose_name='系统', on_delete=models.CASCADE)
    prodate = models.ForeignKey(to='ProDate', verbose_name='测评服务合同', on_delete=models.CASCADE)
    cuserInfo = models.ForeignKey(to='CUserInfo', verbose_name='联系人', on_delete=models.CASCADE)
    gmanagerInfo = models.ForeignKey(to='GmanagerInfo', verbose_name='负责人', on_delete=models.CASCADE)
    remark = models.TextField(verbose_name='备注')

    def get_user(self):
        return self.customer.user.username

    def get_customerr(self):
        return self.customer.unit_name

    def __str__(self):
        return self.customer.unit_name


class Info(models.Model):
    '''信息调查表'''
    zc_excel = models.FileField(upload_to='infocheck', null=True, blank=True, verbose_name='资产表excel')
    tpt = models.FileField(upload_to='tpt', null=True, blank=True, verbose_name='拓扑图')
    tpt_desc = models.TextField(verbose_name='拓扑图描述')
    downloadinfo = models.FileField(upload_to='downloadinfo', null=True, blank=True, verbose_name='下载信调表')
    djcp = models.ForeignKey(to='Djcp', verbose_name='项目', on_delete=models.CASCADE)

    def __str__(self):
        return self.djcp.customer.unit_name + self.djcp.proInfo.sys_name


class Case(models.Model):
    '''测评方案'''
    caseUpload = models.FileField(upload_to='caseUpload', null=True, blank=True, verbose_name='上传方案')
    caseDown = models.FileField(upload_to='caseDown', null=True, blank=True, verbose_name='下载方案')
    case = models.ForeignKey(to='Djcp', verbose_name='项目', on_delete=models.CASCADE)

    def __str__(self):
        return self.case.customer.unit_name + self.case.proInfo.sys_name
