# 合约初始化参数,参数依次排列
# 比如constructor(address god) public
# 这个初始化函数这样设置'yaofan.sol':['coinbase']
# defaultAccount,accounts[0],coinbase都代表当前的账号
# 部署合约时自动填充
init_argv = {'hello.sol': [],
             'yaofan.sol': ['coinbase']}