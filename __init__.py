import io
from datetime import date, datetime
from math import sin, pi

from mycroft import MycroftSkill, intent_file_handler
from mycroft.util import extract_datetime
from mycroft.client.enclosure.emilia import PrinterCommand

class Biobio(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def plot(self, birth):
        if type(birth) is str:
            dt_birth = datetime.strptime(birth, '%d/%m/%Y').date()
        else:
            dt_birth = birth

        t0 = dt_birth.toordinal()
        t1 = date.today().toordinal()
        dates = list(range((t1-10),(t1+10))) # range of 20 days

        div = ''.join(['-'] * 92)

        output = io.StringIO()

        print("\n\n", file=output)
        print(div, file=output)
        print("                                         BIORRÍTMO", file=output)
        print(f"Data de Nascimento: {dt_birth.strftime('%d/%m/%Y')}                              Período: {date.fromordinal(dates[0]).strftime('%d/%m/%Y')} a {date.fromordinal(dates[-1]).strftime('%d/%m/%Y')}", file=output)
        print(div, file=output)

        p = []
        e = []
        i = []
        for d in dates:
            p.append(sin(2*pi*(d-t0)/23))
            e.append(sin(2*pi*(d-t0)/28))
            i.append(sin(2*pi*(d-t0)/33))

        for ind, d in enumerate(dates):
            line = ['.'] * 80 if d == t1 else [' '] * 80
            line[int(40 + (p[ind] * 39))] = 'f'
            line[int(40 + (e[ind] * 39))] = 'e'
            line[int(40 + (i[ind] * 39))] = 'i'
            print(date.fromordinal(d).strftime('%d/%m/%Y') + '-' + ''.join(line), file=output)

        print(div, file=output)
        print("f = Físico / e = Emocional / i = Intelectual", file=output)
        print(div, file=output)

        chart = output.getvalue()
        output.close()

        return chart

    def extract_birth_date(self, utt):
        dt_info = extract_datetime(utt)
        if dt_info:
            birth = dt_info[0].date() # .replace(tzinfo=None)
            today = datetime.today().date()
            self.log.info(f"BIRTH NO TZ ----->  {birth} / TODAY ------> {today}")
            if birth < today:
                return birth
        return None

    @intent_file_handler('biobio.intent')
    def handle_biobio(self, message):
        birth = self.extract_birth_date(message.data["utterance"])
        self.log.info(f"BIRTH 1 ----->  {birth}")
        if birth is None:
            utt = self.get_response("ask.birth.date")
            birth = self.extract_birth_date(utt)
            self.log.info(f"BIRTH 2 ----->  {birth}")
            if birth is None:
                self.speak("Sorry, could not understand your birth date, please start again.")
                return

        if self.ask_yesno("confirm.plotting") == "yes":
            self.speak_dialog("biobio")
            chart = self.plot(birth)
            self.log.info(chart)
            self.enclosure.print_text(chart)


def create_skill():
    return Biobio()

