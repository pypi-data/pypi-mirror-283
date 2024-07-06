from accions import *
from asyncio import run


value = run(MultiWalk('181.232.180.7',"ConextVM",["1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.4194403072"],False,True))
print(value)


# async def exec():
#     value = await Get_async('181.232.180.7',"ConextVM","1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.4194403072.5")

#     return value



# print(run(exec()))


# async def exec():
#     value = await Set_async('181',"ConextVM","1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1.4194403072.4",2,"int")

#     return value


# print(run(exec()))
