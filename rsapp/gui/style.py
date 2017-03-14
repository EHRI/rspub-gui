#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Style(object):

    @staticmethod
    def error():
        return "color: rgb(255, 0, 0);"

    @staticmethod
    def default():
        return "color: rgb(0, 0, 0);"

    @staticmethod
    def parameter():
        return "background-color: rgb(255, 255, 255);"

    @staticmethod
    def derived():
        return "background-color: rgb(232, 245, 249);"

    @staticmethod
    def h2():
        return "color: rgb(90, 100, 120); background-color: rgb(210, 210, 210);"

    @staticmethod
    def alarm():
        return "color: rgb(255, 255, 255); background-color: rgb(225, 0, 0);"

    @staticmethod
    def blue_text():
        return "color: rgb(0, 0, 255);"

    @staticmethod
    def red_text():
        return "color: rgb(255, 0, 0);"

    @staticmethod
    def execute_title():
        return "color: rgb(255, 255, 255); background-color: rgb(102, 0, 0);"

    @staticmethod
    def transport_title():
        return "color: rgb(255, 255, 255); background-color: rgb(0, 0, 153);"

    @staticmethod
    def import_title():
        return "color: rgb(255, 255, 255); background-color: rgb(228, 131, 20);"
