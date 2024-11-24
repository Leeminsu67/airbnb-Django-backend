# class Human:
#     def __init__(self, name):
#         self.name = name
        
#     def hello(self):
#         print(f"hello {self.name}")

# class Player(Human):
#     # 클래스를 호출할 때 제일 먼저 실행되는 함수 javascript로 치면 constructor
#     def __init__(self, name, xp):
#         super().__init__(name)
#         self.xp = xp
        
        
# class Fan(Human):
#     def __init__(self, name, fav_team):
#         super().__init__(name)
#         self.fav_team = fav_team
        
#     def test(self):
#         print(self.name)
        
        
# mingdev = Player('mingdev', 1000)
# print(mingdev.name, mingdev.xp)
# mingdev.hello()

# ming_player = Fan('mingdev', 'testest')
# ming_player.hello()
# ming_player.test()

"""
"""
# class Dog:
#     def woof(self):
#         print("woof woof")
        
        
# class Beagle(Dog):
#     def jump(self):
#         super().woof()
#         print("super woof")
        
        
# beagle = Beagle()
# beagle.jump()


"""
==============================================
"""


# class Dog:
#     def __init__(self, name):
#         self.name = name
    
#     def __str__(self):
#         return f"Dog: {self.name}"
        
# jia = Dog('jia')
# print(dir(jia))
# print(jia)
# paul = Dog('paul')
# print(paul)