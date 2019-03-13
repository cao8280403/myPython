#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Michael Liao'


class Student(object):

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

