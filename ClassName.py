import ReverseDoc

class ClassName():

    def __init__(self):
        self.comments = ""
        self.title = ""

    def __repr__(self):
        if self.comments:
            self.comments = str(self.comments) + "\n */\n"
        return self.comments + str(self.title)



def find_class_name(soup):
    """
    method find_class_name

    finds a returns the name of the class on the page
    :param soup:
"""
    my_class = ClassName()
    my_class.title = str(soup.find("pre").text).replace("\n", " ")
    class_comments = soup.find("div", {"class": "description"}).find("div", {"class": "block"})
    if class_comments:
        my_class.comments = ReverseDoc.create_comment(str(class_comments.text), False)
    return my_class