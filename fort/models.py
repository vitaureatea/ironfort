from django.db import models
from django.contrib.auth.models import User

class Host(models.Model):
    hostname = models.CharField(max_length=128,unique=True,verbose_name='远程主机名')
    ip = models.GenericIPAddressField(verbose_name='主机IP') #做了ip映射，ip可能重复，ip:port 不会重复
    port = models.SmallIntegerField(default=22,verbose_name='端口')
    release = models.CharField(max_length=255, default='CentOS', verbose_name='发行版本')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '[%s]  < %s : %s >' % (self.hostname, self.ip, self.port)

    class Meta:
        verbose_name = '远程主机'
        verbose_name_plural = '远程主机'
        unique_together = ('ip', 'port')


class RemoteUser(models.Model):
    # 用户名可以重复的！
    remote_user_name = models.CharField(max_length=128,default='root',verbose_name='远程主机用户名')
    # 密码将被用于ssh登录
    password = models.CharField(max_length=512)

    def __str__(self):
        return '[%s]   < %s >' % (self.remote_user_name, self.password)

    class Meta:
        verbose_name = '远程主机用户'
        verbose_name_plural = '远程主机用户'
        unique_together = ('remote_user_name', 'password')  # root 123



class RemoteUserBindHost(models.Model):
    # host1: (root, 123)
    # host2: (test, 666)
    remote_user = models.ForeignKey('RemoteUser', on_delete=models.CASCADE)
    #on_delete当RemoteUser记录被删时，本表的对应记录也会被删除 2.0专属
    host = models.ForeignKey('Host', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def __str__(self):
        return '[ %s ]   <  %s : %s >' % (self.host.hostname,
                                          self.remote_user.remote_user_name,
                                          self.remote_user.password)

    class Meta:
        verbose_name = '用户绑定主机'
        verbose_name_plural = '用户绑定主机'
        unique_together = ('host', 'remote_user')
        #一个用户下，只能绑定同一个主机一次，不能一个用户下绑定两个相同主机



class Group(models.Model):
    group_name = models.CharField(max_length=128, unique=True, verbose_name='主机组名')
    remote_user_bind_hosts = models.ManyToManyField('RemoteUserBindHost', blank=True,verbose_name='组内关联的远程用户')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '主机组： %s' % self.group_name

    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = '主机组'


#堡垒机用户表
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type_chiose = (
        ('0','超级用户'),
        ('1','普通用户'),
        ('2','测试用户'),
        ('3','开发用户'),
        ('4','运维用户')
    )
    user_type = models.CharField(max_length=4, choices=user_type_chiose,default='普通用户', verbose_name='用户类型')
    remote_user_bind_hosts = models.ManyToManyField('RemoteUserBindHost', blank=True, verbose_name='堡垒机用户关联的远程用户')
    groups = models.ManyToManyField('Group', blank=True, verbose_name='所属堡垒机组')
    enabled = models.BooleanField(default=True, verbose_name='是否可以登录堡垒机')

    def __str__(self):
        return '%s  ： %s' % (self.user_type, self.user.username)

    class Meta:
        verbose_name = '堡垒机用户'
        verbose_name_plural = '堡垒机用户'


#用户中心表
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True,null=True)
    job = models.CharField(max_length=128,verbose_name='职位')
    image = models.ImageField(upload_to='dist/img/userhead/', verbose_name=u'头像',
                              default=u'dist/img/user2-160x160.jpg', max_length=100)

    def __str__(self):
        return '%s : %s' %(self.user,self.job)

    class Meta:
        verbose_name = '堡垒机用户的个人信息'
        verbose_name_plural = '堡垒机用户的个人信息'



#日志
class AccessLog(models.Model):
    log_type_choices = (
        ('0', 'DEBUG'),
        ('1', 'INFO'),
        ('2', 'WARNING'),
        ('3', 'ERROR'),
        ('4', 'CRITICAL'),
    )
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='产生日志的用户', on_delete=models.SET_NULL)
    #on_delete=models.SET_NULL 当外键的用户被删时，对应的日志不会被删，设为null
    log_type = models.CharField(max_length=32, choices=log_type_choices, default='1', verbose_name='日志类型')
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    def __str__(self):
        return '%s < %s >  记录时间： <%s>' % (self.user.userprofile.user_type, self.user.username, self.c_time)

    class Meta:
        verbose_name = '堡垒机用户行为日志'
        verbose_name_plural = '堡垒机用户行为日志'
        ordering = ['-c_time']
