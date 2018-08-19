import json
import os
import shutil

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract
from string import Template
from html.parser import HTMLParser

from config import Config


# 合约管理
class ContractMgr:

    # 部署全部合约
    @staticmethod
    def deploy_all():
        # 遍历合约文件夹
        if os.path.isdir(Config.getContractPath()):
            for root, dirs, files in os.walk(Config.getContractPath()):
                for d in dirs:
                    pass
                for f in files:
                    ContractMgr.deploy_file(f);

    # 部署合约文件
    @staticmethod
    def deploy_file(filename):

        print('尝试部署',filename)

        # 编译合约
        filepath = Config.getContractPath(filename)
        if os.path.exists(filepath) == False:
            return

        with open(filepath,'r') as infile:
            sol = infile.read()

        compilename = '<stdin>:' + os.path.splitext(filename)[0].capitalize()
        compiled_sol = compile_source(sol)
        contract_interface = compiled_sol[compilename]

        print('  编译', filename, '完成..')

        savepath = Config.getBuildPath(filename)

        if os.path.isdir(Config.getBuildPath()) == False:
            os.mkdir(Config.getBuildPath())

        if os.path.isdir(savepath):
            shutil.rmtree(savepath)
        os.mkdir(savepath)

        # 生成abi,bytecode文件
        abipath = savepath + '/abi.json'
        with open(abipath,'w') as outfile:
            json.dump(contract_interface['abi'], outfile)

        print('  生成abi文件:', abipath, '..')

        bytecodepath = savepath + '/bytecode.s'
        with open(bytecodepath,'w') as outfile:
            json.dump(contract_interface['bin'], outfile)

        print('  生成bytecode文件:', bytecodepath, '..')

        # 尝试部署
        w3 = Web3(Web3.HTTPProvider(Config.getNodeIP()))

        # 设置默认账户
        w3.eth.defaultAccount = w3.eth.accounts[0]

        # 实例化合约
        contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        # 填充初始化参数
        from init import init_argv
        for k in init_argv:
            if k == filename:
                count = len(init_argv[k])
                for i in range(count):
                    if init_argv[k][i] == 'defaultAccount' \
                        or init_argv[k][i] == 'accounts[0]' \
                        or init_argv[k][i] == 'coinbase':
                        init_argv[k][i] = w3.eth.defaultAccount

        # 提交部署合约事务
        tx_hash = contract.constructor(*init_argv[filename]).transact()

        # 等待事务挖矿结束并获取交易收据
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # 生成地址文件
        addrpath = savepath + '/address.s'
        with open(addrpath,'w') as outfile:
            json.dump(tx_receipt['contractAddress'], outfile)
        print('  生成地址文件:', addrpath, '..')

        # 生成web模板页面
        webstr = Template('''
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="gbk">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>$template_title</title>
    <script src="js/web3.min.js"></script>
</head>
<body>
    <script>
        var web3 = new Web3(window.web3.currentProvider);
        var Contract;
        var abi = $template_abi;
        var address = '$template_addr';
        async function init(){
            Contract = await new web3.eth.Contract(abi,address);
        }
        init(); 
    </script>
</body>
</html>
        ''')

        yfstr = Template('''
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="gbk">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>$template_title</title>
    <script src="js/web3.min.js"></script>
</head>
<body>
    <h2>功德箱</h2>
    <h3>积德人数：<em id="goodman_count"></em></h3>
    <h4>最低打赏 0.1 eth</h4>
    <input type="button" id="send" value="积德行善">
    <script>
        var web3 = new Web3(window.web3.currentProvider);
        var Contract;
        var abi = $template_abi;
        var address = '$template_addr';
        async function init(){
            Contract = await new web3.eth.Contract(abi,address);
            Contract.methods.goodman_count().call().then(function(num){
                document.getElementById('goodman_count').textContent = num;
            });

        }
        init(); 
        async function send(){
            var accounts = await web3.eth.getAccounts();
            Contract.methods.givemoney(accounts[0])
            .send({from:accounts[0],value:web3.utils.toWei(0.1, "ether")})
            .then(function(data){
                console.log(data);
            })
        
        }
        document.getElementById('send').addEventListener('click',send);
    </script>
</body>
</html>
        ''')

        if filename == 'yaofan.sol':
            webstr = yfstr.substitute(template_title=filename,
                                       template_abi=json.dumps(contract_interface['abi']),
                                       template_addr=tx_receipt['contractAddress']),
        else:
            webstr = webstr.substitute(template_title=filename,
                                        template_abi=json.dumps(contract_interface['abi']),
                                        template_addr=tx_receipt['contractAddress']),
        webpath = Config.getWebTemplatePath('app/'+os.path.splitext(filename)[0]+'.html')

        with open(webpath,'w') as outfile:
            outfile.write(webstr[0])
        print('  生成web模板文件:', webpath, '..')

        print('部署', filename, '完成,', '地址:', tx_receipt['contractAddress'],'\n')

        # web3py直接RPC示例
        """
        # Create the contract instance with the newly-deployed address
        greeter = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi'],
        )
    
        # Display the default greeting from the contract
        print('Default contract greeting: {}'.format(
            greeter.functions.greet().call()
        ))
    
        print('Setting the greeting to nihao...')
        tx_hash = greeter.functions.setGreeting('nihao').transact()
    
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
    
        # Display the new greeting value
        print('Updated contract greeting: {}'.format(
            greeter.functions.greet().call()
        ))
    
        # When issuing a lot of reads, try this more concise reader:
        reader = ConciseContract(greeter)
        assert reader.greet() == "nihao"
        """
