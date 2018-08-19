## 配置 ##
class Config:

    ################################################################

    # 以太坊节点地址,端口
    _node_ip = 'localhost'
    _node_port = '9545'

    # web服务器地址,端口
    _web_ip = 'localhost'
    _web_port = '9000'

    # 生成构建目录
    _build_path = '../build/'

    # 生成合约目录
    _contracts_path = '../contracts/'

    # 生成web目录
    _web_path = '../web/'

    # web模板目录
    _web_template_path = '../core/template/'

    #################################################################

    @staticmethod
    def getNodeIP():
        return ''.join(['http://',Config._node_ip,':',Config._node_port])

    @staticmethod
    def getWebIP():
        return Config._web_ip

    @staticmethod
    def getWebPort():
        return Config._web_port

    @staticmethod
    def getBuildPath(filename=''):
        return Config._build_path + filename

    @staticmethod
    def getContractPath(filename=''):
        return Config._contracts_path + filename

    @staticmethod
    def getWebPath(filename=''):
        return Config._web_path + filename

    @staticmethod
    def getWebTemplatePath(filename=''):
        return Config._web_template_path + filename

