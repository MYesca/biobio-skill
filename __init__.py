from mycroft import MycroftSkill, intent_file_handler


class Biobio(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('biobio.intent')
    def handle_biobio(self, message):
        self.speak_dialog('biobio')


def create_skill():
    return Biobio()

