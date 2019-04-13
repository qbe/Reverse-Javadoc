import ReverseDoc
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class StaticField():
    """
    class static_field

    Stores a single static field of a class for later printing

    slots:
        comment - the comments from the javadoc about the method
        instance_type - the type of the static variable
        name - the name of the variable
"""

    def __init__(self):
        self.comments = ""
        # self.comments.header = False
        self.instance_type = ""
        self.name = ""
        self.value = ""


    def __repr__(self):
        """
        method __repr__(self)

        Returns the field as a string in this format:
        //comment
        self.instance_type self.name
    """
        return str(self.comments) + "\n\t */\n " + "\t" + " " + self.name + self.value + ";\n\n"


def find_fields_details(fields_list, soup):
    """

    :param fields_list:
    :param soup:
    """
    for field in fields_list:
        field_details = soup.find("a", {"name": field.name})
        field.name = str(field_details.findNext("pre").text).replace(u'\u00a0', " ")
        if field_details.findNext("div", {"class": "block"}):
            field.comments = ReverseDoc.create_comment(str(field_details.findNext("div", {"class": "block"}).text),
                                                       True)


def check_constant(field):
    """
    Checks to see if the field has a constant value and sets it to such if possible
    :param field: field to check
    """


def find_fields(soup, location):
    """
    method find_fields

    Finds all of the fields and returns them as a python list of type static_field
    :param soup: Beautiful soup of class page
    :param location: where is the class file (as a URL)
    """
    fields_list = list()
    field_summary = soup.find(text=re.compile("FIELD\sSUMMARY"))
    if field_summary:
        field_summary = field_summary.findNext("ul")
        for table_row in field_summary.find_all("tr", recursive="true"):
            # print(table_row.text.strip())
            if table_row.text.strip() != "Modifier and Type\nField and Description":
                new_field = StaticField()
                for table_code in table_row.find_all("code", recursive="true"):
                    if new_field.instance_type == "":
                        new_field.instance_type = str(table_code.text)
                    else:
                        new_field.name = str(table_code.text)
                fields_list.append(new_field)
        find_fields_details(fields_list, soup)
    try:
        constants = urlopen(location + "constant-values.html").read()
        constant_soup = BeautifulSoup(constants)
        for field in fields_list:
            value_check = constant_soup.find("a", {"name": re.compile(field.name.split(" ")[-1])})
            if value_check:
                field.value = str(value_check.findNext("td", {"class": "colLast"}).text)
                field.value = " = " + field.value
    except:
        pass

    return fields_list