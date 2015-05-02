import ReverseDoc, re, copy, Fields


class Constructor():
    def __init__(self):
        """
        Stores Constructor for later printing

        attributes:
        sig: signature of the constructor method
        comments: any comments that accompany the constructor
        parameters: what is getting passed to the constructor
        body: constructor body. Will guess at what to put based on parameters and fields. ie. this.speed = speed if
             speed is a parameter
        """

        self.sig = ""
        self.comments = ""
        self.parameters = list()
        self.body = ""

    def __repr__(self, interface):
        """
        Used to print out the constructor.
        :param interface: Boolean telling whether the constructor is in an interface or not
        :return: string that can be printed to a file
        """

        # TODO consider making this add a private field if it isn't there
        # TODO consider checking what is in the parent class's constructor and call super on those parameters,
        # then do this. on the rest, adding the field as necessary
        if self.parameters:
            for parameter in self.parameters:
                self.body += "\t\tthis." + parameter[0] + " = " + parameter[0] + ";\n"
        else:
            self.body = ""
        if self.comments and self.parameters:
            header = str(self.comments) + ReverseDoc.parameter_print(self.parameters) + "\n\t */\n"
        elif self.comments:
            header = str(self.comments) + "\n\t */\n"
        else:
            header = ""
        if interface:
            return header + "\t" + self.sig + ";"

        return header + "\t" + self.sig + " {" \
            + "\n" + "\t\t//TODO Check for accuracy\n" + self.body + "\n\t} \n\n"


def find_constructor(soup, fields):
    """
    Finds the constructor and other necessary items for the constructor method
    :param soup: HTML of the class
    :return: constructor instance
    """
    constructor = soup.find(text=re.compile("CONSTRUCTOR\sDETAIL"))
    if constructor:
        constructor = constructor.findNext("ul")
        new_constructor = Constructor()
        new_constructor.sig = " ".join(str(constructor.find("pre").text).replace("\n", "").split())
        if str(new_constructor.sig).find("(") - str(new_constructor.sig).find(")") != -1 and \
                constructor.find("div", {"class": "block"}):
            new_constructor.comments = ReverseDoc.create_comment(
                str(constructor.find("div", {"class": "block"}).text), True)
            constructor_parameters = constructor.find("span", {"class": "paramLabel"}, recursive=True)
            if constructor_parameters:
                parameters_list = list()
                constructor_parameters = constructor_parameters.parent.parent # Move up two levels so dd flag can be seen
                for parameter in constructor_parameters.find_all("dd"):
                    if parameter.find("code") is not None:
                        parameters_list.append([parameter.text.split("-", 1)[0].strip(),
                                                parameter.text.split("-", 1)[1].strip()])
                new_constructor.parameters = parameters_list
        else:
            return None
        check_fields(new_constructor, fields)
        return new_constructor


def check_fields(new_constructor, fields):
    param_to_make = copy.deepcopy(new_constructor.parameters)
    for param in new_constructor.parameters:
        for field in fields:
            if param[0] == field.name:
                param_to_make.remove(param)
    # print(param_to_make)
    for param in param_to_make:
        new_field = Fields.StaticField()
        new_field.comments = str(ReverseDoc.create_comment(param[1], True))
        signature = str(new_constructor.sig)
        start = signature.index("(")
        end = signature.find(")")
        params = signature[start + 1: end]
        param_list = re.findall(r"[\w]+", params)
        param_loc = param_list.index(str(param[0]))
        new_field.name = "private " + param_list[param_loc - 1] + " " + param[0]
        fields.append(new_field)
