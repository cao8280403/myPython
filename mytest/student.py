#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Michael Liao'


class Student(object):
    name = 'student'

    # __slots__ = ('sex', 'age')  # 用tuple定义允许绑定的属性名称__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
    # s.name = 'Michael' 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
    # print(Student.name)但是类属性并未消失，用Student.name仍然可以访问

    def __init__(self, name, score):
        # self.name = name
        # self.score = score
        self.__name = name
        self.__score = score  # 私有，使外部无法访问和修改

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
        # pass

    def get_name(self):
        return self.__name

    @property
    def score(self):
        return self.__score

    # 加上注释之后就变成一个只读属性
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self.__score = value

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'

    def __str__(self):  # 类似tostring
        return 'Student object (name: %s)' % self.name

    __repr__ = __str__
    # __str__() 返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串

    def __call__(self):
        print('My name is %s.' % self.name)
        # s()  # self参数不要传入
        # callable(Student()) 返回True能被调用的对象就是一个Callable对象


def test():
    bart = Student('Bart Simpson', 59)
    lisa = Student('Lisa Simpson', 87)
    bart.print_score()
    lisa.print_score()
    print(bart)  # 是对象
    print(lisa)
    print(lisa.get_name())
    print(lisa.get_grade())
    print(Student)  # 是类名
    s = Student('Lisa Simpson2', 27)
    s.score = 60  # OK，实际转化为s.set_score(60)
    print(s.score)  # OK，实际转化为s.get_score()
    s = Student('Michael', '46')
    s.name = 'apple'
    print(s)


if __name__ == '__main__':
    test()
