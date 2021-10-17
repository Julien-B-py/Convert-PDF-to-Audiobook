import pdfplumber
import pyttsx3


class PDF:
    def __init__(self, file: str, del_line_break: bool = False):
        """
        Constructs a new PDF object.
        @param file: Path of the PDF file to open.
        @type file: str
        @param del_line_break: Remove all line breaks characters ("\n") from the extracted text to allow a smoother
        text audio playback.
        @type del_line_break: bool
        """
        self.file = file
        self.del_line_break = del_line_break
        self.pages = []
        self.extract_text()
        # Create text-to-speech conversion object
        self.narrator = pyttsx3.init()

    def extract_text(self):
        """
        Extract the text from every single page of the PDF file and store it as a list of strings.
        """
        with pdfplumber.open(self.file) as pdf:
            # Loop through all pages
            # For each page grab every character line by line and append the page content to a list
            for page in pdf.pages:
                page_text = page.extract_text()
                # Improve text to speech process by removing unneeded breaks in the reading process
                # Good for a book but not for a documentation for example
                if self.del_line_break:
                    # Remove words wrapping on line breaks
                    page_text = page_text.replace("-\n", "")
                    # Remove line breaks
                    page_text = page_text.replace("\n", "")

                self.pages.append(page_text)

    def set_speech_language(self):
        """
        Changes the voice language used during text audio playback.
        If the specified voice language does not exists, default voice will be used.
        For example in my case the default language is French.
        """
        # Get the list of all the voices objects
        voices = self.narrator.getProperty("voices")
        # Loop through all voices
        for voice in voices:
            # If user requested language is part of the current voice name we set this voice as the active voice.
            if self.language.lower() in voice.name.lower():
                self.narrator.setProperty("voice", voice.id)

    def to_speech(self, language: str = None):
        """
        Perform the text audio playback for every single page of the PDF file in the selected language.
        @param language: The language used for text audio playback
        @type language: str
        """
        # If user requested a specific language
        if language:
            self.language = language
            # Change the text-to-speech language
            self.set_speech_language()

        # For each page of the PDF file the text-to-speech will be performed
        for page in self.pages:
            self.narrator.say(page)
            self.narrator.runAndWait()


if __name__ == "__main__":
    my_pdf = PDF("file.pdf")
    my_pdf.to_speech(language="english")
