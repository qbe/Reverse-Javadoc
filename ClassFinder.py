#!/usr/bin/python3
import ReverseDoc
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
import argparse

class Java():
    """
    Holds a java class with its location.
    """
    def __init__(self):
        self.name = ""
        self.location = ""

    def __str__(self):
        return self.location


def findClasses(soup):
    """
    Used to locate all classes in the javadoc. Also keeps track of each classes location to determine packages.
    :param soup: HTML of the overview-tree page.
    :return: list containing Java class objects
    """
    classes = soup.find("h2", {"title": "Class Hierarchy"}) #gets the tag for the class list
    java_class_list = list()
    if classes:
        classes = classes.findNext("ul") #move down to the class list
        class_list = classes.find_all("a") #list of classes
        for java_class in class_list:
            new_class = Java()
#            new_class.name = str(java_class.find("span", {"class": "typeNameLink"}).text)
            new_class.name = str(java_class.find("span", class_="typeNameLink"))
            new_class.location = str(java_class.get("href"))
            java_class_list.append(new_class)
    return java_class_list


def findInterfaces(soup):
    """
    Just like findClasses, but for interfaces
    :param soup: HTML of the overview-tree page.
    :return: list containing java class objects.
    """
    #TODO combine with findClasses
    interfaces = soup.find("h2", {"title": "Interface Hierarchy"})
    interface_list = list()
    if interfaces:
        interfaces = interfaces.findNext("ul")
        temp_list = interfaces.find_all("li")
        for temp_class in temp_list:
            new_class = Java()
#            new_class.name = str(temp_class.find("span", {"class": "typeNameLink"}).string)
            new_class.name = str(temp_class.find("span", class_="typeNameLink"))
            new_class.location = str(temp_class.find("a").get("href"))
            interface_list.append(new_class)
    return interface_list


def main():
    parser=argparse.ArgumentParser(description='a program that generates stubs form JavaDoc')
    parser.add_argument('--doc', type=string, default='', help='url to main doc page(index)')
    parser.add_argument('--src', type=string, default='', help='complete location to output src files: ')
    args = parser.parse_args()

    htmlfile=args.doc
    output=args.src
    if(args.doc == ''):
        htmlfile = input("Enter url to main doc page: ")
    if(args.src == ''):
        output = input("Enter complete location to output src files: ")
    # htmlfile = "http://www.cs.rit.edu/~csci142/Projects/01/doc/"
    # htmlfile = "http://www.cs.rit.edu/~csci142/Labs/09/Doc/"
    # output = "/home/andrew/Documents/AJ-College/Spring2015/CS142/9Mogwai/Lab9"
    # htmlfile = "http://www.cs.rit.edu/~csci142/Labs/06/Doc/"
    # output = "/home/andrew/java"
    # output = "/home/andrew/Documents/AJ-College/Spring2015/CS142/6Graduation/Lab6"
    # output = "/home/andrew/school/CS142/4BankAccount/Lab4"
    # output = "/home/andrew/school/CS142/1Perp/Project1"
    if htmlfile[-1] != "/": #add slashes as appropriate
        htmlfile += "/"
    if output[-1] != "/":
        output += "/"
    output += "src/" # put the output in a directory called src
    htmltext = urllib.request.urlopen(htmlfile + "overview-tree.html").read()
    soup = BeautifulSoup(htmltext)
    class_list = findClasses(soup)
    interface_list = findInterfaces(soup)
    #TODO make this a function and pass it interface or class as appropriate
    for java_class in class_list:
        if(java_class.location.startswith("https://docs.oracle.com/javase")):
            continue
        new_class = (
                ReverseDoc.ReverseDoc(urllib.request.urlopen(htmlfile + java_class.location).read(), htmlfile), "except")
        path = os.path.join(output, java_class.location.replace(".html", "") + ".java")
        dirpath = path.rsplit("/", 1)[0] + "/"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(path, "w") as f:
            #TODO see if the decoding or printing can be done at creation to remove if else
            if new_class[1] == "try":
                f.write(new_class[0].decode("utf-8"))
            else:
                f.write(new_class[0].__repr__(False)) #telling it to print as a class
    for interface in interface_list:
        if(interface.location.startswith("https://docs.oracle.com/javase")):
            continue
        new_interface = (
                ReverseDoc.ReverseDoc(urllib.request.urlopen(htmlfile + interface.location).read(), htmlfile), "except")
        path = os.path.join(output, interface.location.replace(".html", "") + ".java")
        dirpath = path.rsplit("/", 1)[0] + "/"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(path, "w") as f:
            if new_interface[1] == "try":
                f.write(new_interface[0].decode("utf-8"))
            else:
                f.write(new_interface[0].__repr__(True)) #telling it to print as an interface


if __name__ == '__main__':
    main()
