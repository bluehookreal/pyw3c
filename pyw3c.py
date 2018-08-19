import os
import sys

from core.deploy import ContractMgr
from core.webserver import WebServerMgr


##
if __name__ == '__main__':

    if 'compile' in sys.argv:
        pass
    elif 'migrate' in sys.argv:
        # 部署合约
        os.chdir("./core/")
        ContractMgr.deploy_all()
        # 生成web页面
        WebServerMgr.build_web()
    elif 'run' in sys.argv:
        # 启动web服务器
        print('\n启动web服务器..')
        os.chdir("./web/")
        os.system("run.py")
    else:
        help = '''
usage: python pyw3c.py [option] [arg] 
Options and arguments (and corresponding environment variables):
help h -h   : help text
compile     : only compile
migrate     : compile and deploy contracts
run         : run webserver
        '''
        print(help)
