
class Printer:
	should_print = False

	@classmethod
	def set_print(cls, settings):
		cls.should_print = settings

	@classmethod
	def write(cls, text):
		if cls.should_print:
			print text
