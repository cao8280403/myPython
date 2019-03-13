#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Michael Liao'


class Student(object):
    name = 'student'
    # s.name = 'Michael' 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
    # print(Student.name)但是类属性并未消失，用Student.name仍然可以访问

    def __init__(self, name, score):
        # self.name = name
        # self.score = score
        self.__name = name
        self.__score = score    # 私有，使外部无法访问和修改

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
        # pass

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'


def test():
    bart = Student('Bart Simpson', 59)
    lisa = Student('Lisa Simpson', 87)
    bart.print_score()
    lisa.print_score()
    print(bart)#是对象
    print(lisa)
    print(lisa.get_name())
    print(lisa.get_grade())
    print(Student)#是类名


if __name__ == '__main__':
    test()

