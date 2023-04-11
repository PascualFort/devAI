
from classes.BashProcess import BashProcess


bash = BashProcess("D:/Documentos/webblocks/test", False, True)
print(bash.run('bash -c "touch"'))
