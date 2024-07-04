# BLTrade Version
import subprocess

# Git版本提交次数
def GetGitPushCount():
    
    gitpushcount=subprocess.getoutput('git rev-list --count HEAD')
    return gitpushcount

# 获取版本号
def GetVersion():
    try:
        BLTradeVersion=GetGitPushCount()
        #BLTradeVersion=subprocess.getoutput('gitx')
        #return f"BLTrade Engine Version: {int(BLTradeVersion)/1000}"
        return f"{int(BLTradeVersion)/1000}"
    except ValueError:
        print("Excepted: git命令执行失败!!!")
        BLTradeVersion=285
        #return f"BLTrade Engine Version: {int(BLTradeVersion)/1000}"
        return f"{int(BLTradeVersion)/1000}"


        
    

#print(GetVersion())