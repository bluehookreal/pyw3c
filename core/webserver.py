import json
import os
import shutil

from config import Config


# 创建aiohttp服务器
class WebServerMgr:

    @staticmethod
    def build_web():
        webpath = Config.getWebPath()
        if os.path.isdir(webpath):
            shutil.rmtree(webpath)

        #复制模板
        shutil.copytree(Config.getWebTemplatePath(), webpath)

        #生成合约测试页面列表
        pagelist = []
        list_dirs = os.walk(Config.getWebPath('app'))
        for root, dirs, files in list_dirs:
            for f in files:
                if os.path.splitext(f)[-1] == '.html':
                    pagelist.append(os.path.splitext(f)[0]+'.html')

        webpath = Config.getWebPath('app/' + 'index.html')
        with open(webpath,'w') as outfile:
            for page in pagelist:
                outfile.write('<a href="/app/' + page + '">' + page + '合约测试页</a><br/>')

