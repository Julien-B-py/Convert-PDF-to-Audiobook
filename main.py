import pdfplumber
import pyttsx3


class PDF:
    def __init__(self, file, del_line_break=False):
        self.file = file
        self.del_line_break = del_line_break
        self.extract_text()
        self.narrator = pyttsx3.init()

    def extract_text(self):
        with pdfplumber.open(self.file) as pdf:
            # Total number of pages
            self.nb_pages = len(pdf.pages)

            self.pages = []
            # Loop through all pages
            # For each page grab every character line by line and append the page content to a list
            for page in pdf.pages:
                page_text = page.extract_text()

                # Improve text to speech process by removing unneeded breaks in the reading process
                # Good for a book but not for a documentation for example
                if self.del_line_break:
                    # Remove words wrapping on line breaks
                    page_text = page_text.replace('-\n', '')
                    # Remove line breaks
                    page_text = page_text.replace('\n', '')

                self.pages.append(page_text)

    def set_speech_language(self):
        voices = self.narrator.getProperty('voices')
        for voice in voices:
            if self.language.lower() in voice.name.lower():
                self.narrator.setProperty('voice', voice.id)

    def to_speech(self, language=None):
        if language:
            self.language = language
            self.set_speech_language()

        for page in self.pages:
            self.narrator.say(page)
            self.narrator.runAndWait()


my_pdf = PDF('file.pdf', del_line_break=True)
my_pdf.to_speech(language='english')
