import os
import re
import fitz
import tkinter
import pdfplumber
from io import BytesIO
from PyPDF2.generic import NameObject, TextStringObject
from natsort import natsorted
from pdfminer.layout import LAParams, LTTextLine, LTTextContainer
from pdfminer.high_level import extract_pages
from PyPDF2 import PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

class ReportGenerator:
    def __init__(self, report_pdf, published_evidence_folder, witness_evidence_folder, console_text):
        self.debug = False # Set to True to debug to the console

        self.report_pdf = report_pdf
        self.published_evidence_folder = published_evidence_folder
        self.witness_evidence_folder = witness_evidence_folder
        self.console_text = console_text

        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.font_path_roman = os.path.join(self.current_dir, "fonts", "FrutigerLTStd-Roman.ttf")
        self.font_path_bold = os.path.join(self.current_dir, "fonts", "FrutigerLTStd-Bold.ttf")
        self.font_path_italic = os.path.join(self.current_dir, "fonts", "FrutigerLTStd-Italic.ttf")

        self.register_custom_fonts()

    def register_custom_fonts(self):
        try:
            pdfmetrics.registerFont(TTFont('FrutigerLTStd-Roman', self.font_path_roman))
            pdfmetrics.registerFont(TTFont('FrutigerLTStd-Bold', self.font_path_bold))
            pdfmetrics.registerFont(TTFont('FrutigerLTStd-Italic', self.font_path_italic))
            return True
        except Exception as e:
            self.debug_message(f"Failed to register custom fonts: {e}")
            return False

    def debug_message(self, message):
        if self.debug:
            print(message)

    def console_message(self, message):
        """
        Log updates to the console instance defined in ui.py for the client to see
        the crawler and pdf generator progress.

        Args:
            message (str): Text to be displayed to the client.
        """

        self.console_text.configure(state='normal')
        self.console_text.insert(tkinter.END, message + '\n')
        self.console_text.configure(state='disabled')
        self.console_text.yview(tkinter.END)

    def sanitize_text(self, text):
        return ''.join(char if char.isprintable() else ' ' for char in text)

    def get_text_style(self, page):
        """
        Extracts text styles from a given PDF page.

        Args:
            page (PageObject): A PDF page object from which text styles are extracted.

        Returns:
            styles (list[dict]): A list of dictionaries, each containing text style information.
        """

        text_information = []
        page_info = page.get_text("dict")["blocks"]

        for section in page_info:
            if "lines" in section:
                for line in section["lines"]:
                    for span in line["spans"]:
                        text = {
                            "text": self.sanitize_text(span["text"]),
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"],
                            "origin": span["origin"],
                            "page": page.number,
                        }
                        text_information.append(text)
        return text_information

    def identify_headers(self, pdf_path):
        """
        Identifies headers in a PDF document based on text size.

        Args:
            pdf_path (str): The file path to the PDF document.

        Returns:
            headers (list[dict]): A list of dictionaries, each containing header information.
        """
        headers = []
        document = fitz.open(pdf_path)

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text_styles = self.get_text_style(page)
            for style in text_styles:
                if style["size"] > 12:  # The text separation between lines, seems like exactly 12 on inspection
                    header = {
                        "text": style["text"].strip(),
                        "page": style["page"],
                        "font": style["font"],
                        "size": style["size"],
                        "color": style["color"],
                        "origin": style["origin"]
                    }
                    headers.append(header)

        return headers

    def find_next_header(self, headers, current_header):
        """
        Finds the next header in the list of headers after the current header.

        Args:
            headers (List[dict]): A list of header dictionaries.
            current_header (dict): The current header dictionary.

        Returns:
            header (dict): The next header dictionary if found, otherwise None.
        """

        current_index = None
        for i, header in enumerate(headers):
            if header["text"] == current_header["text"] and header["page"] == current_header["page"]:
                current_index = i
                break

        if current_index is not None:
            current_style = (current_header["font"], current_header["size"], current_header["color"])
            for header in headers[current_index + 1:]:
                header_style = (header["font"], header["size"], header["color"])
                if header_style == current_style:
                    return header
        return None

    def trim_pdf(self, input_pdf, output_pdf):
        """
        Trims the input PDF by removing the front page and keeping specific page ranges
        such as committee pages, witness evidence pages, and published written evidence.

        Args:
            input_pdf (str): The path to the input PDF file.
            output_pdf (str): The path to the output PDF file.

        Returns:
            witness_pages (list): A list containing the first and last page where witness
                                evidence is found within the trimmed pdf.
            published_pages (list): A list containing the first and last page where published
                                    written evidence is found within the trimmed pdf.
        """

        headers_info = self.identify_headers(input_pdf)
        contents_page = None

        self.witnesses_start_page = None
        self.witnesses_end_page = None
        self.evidence_start_page = None
        self.evidence_end_page = None

        with open(input_pdf, "rb") as input_pdf_file:
            reader = PdfReader(input_pdf_file)
            total_pages = len(reader.pages)

            for i, header in enumerate(headers_info):
                if "Contents" in header["text"]:
                    contents_page = header["page"]
                    self.start_page = contents_page - 1
                elif "Witnesses" in header["text"]:
                    self.witnesses_start_page = header["page"]
                    if i + 1 < len(headers_info):
                        next_header_page = headers_info[i + 1]["page"]
                        if next_header_page == self.witnesses_start_page:
                            self.witnesses_end_page = next_header_page
                        else:
                            self.witnesses_end_page = next_header_page - 1
                    else:
                        self.witnesses_end_page = total_pages - 1
                elif "Published written evidence" in header["text"]:
                    self.evidence_start_page = header["page"]
                    next_header = self.find_next_header(headers_info, header)
                    if next_header:
                        self.evidence_end_page = next_header["page"] - 1
                    else:
                        self.evidence_end_page = total_pages - 1

            writer = PdfWriter()

            end_page = contents_page if contents_page is not None else total_pages
            original_to_new_pages = []

            published_evidence_markers = {}
            witness_evidence_markers = {}

            new_page_num = 1
            for page_num in range(1, end_page):
                writer.add_page(reader.pages[page_num])
                original_to_new_pages.append((page_num + 1, new_page_num))
                new_page_num += 1

            def add_page_range(writer, reader, start_page, end_page, new_page_num, markers_dict):
                if start_page is not None and end_page is not None:
                    for page_num in range(start_page, end_page + 1):
                        if page_num <= len(reader.pages):
                            writer.add_page(reader.pages[page_num])
                            original_to_new_pages.append((page_num, new_page_num))
                            markers_dict[new_page_num] = []
                            new_page_num += 1
                return new_page_num

            self.debug_message(f"{self.witnesses_start_page, self.witnesses_end_page, self.evidence_start_page, self.evidence_end_page}")

            if self.witnesses_start_page is not None and self.evidence_start_page is not None and self.witnesses_start_page == self.evidence_start_page:
                witnesses_new_start_page = new_page_num
                evidence_new_start_page = new_page_num
                writer.add_page(reader.pages[self.witnesses_start_page])
                original_to_new_pages.append((self.witnesses_start_page + 1, new_page_num))
                witness_evidence_markers[new_page_num] = []
                published_evidence_markers[new_page_num] = []
                witnesses_new_end_page = new_page_num
                evidence_new_end_page = new_page_num
                new_page_num += 1

                new_page_num = add_page_range(writer, reader, self.witnesses_start_page + 1, self.witnesses_end_page, new_page_num, witness_evidence_markers)
                new_page_num = add_page_range(writer, reader, self.evidence_start_page + 1, self.evidence_end_page, new_page_num, published_evidence_markers)
            else:
                if self.witnesses_start_page is not None:
                    witnesses_new_start_page = new_page_num
                    new_page_num = add_page_range(writer, reader, self.witnesses_start_page, self.witnesses_end_page, new_page_num, witness_evidence_markers)
                    witnesses_new_end_page = new_page_num - 1
                else:
                    witnesses_new_start_page = None
                    witnesses_new_end_page = None

                if self.evidence_start_page is not None:
                    evidence_new_start_page = new_page_num
                    new_page_num = add_page_range(writer, reader, self.evidence_start_page, self.evidence_end_page, new_page_num, published_evidence_markers)
                    evidence_new_end_page = new_page_num - 1
                else:
                    evidence_new_start_page = None
                    evidence_new_end_page = None

            with open(output_pdf, "wb") as output_pdf_file:
                writer.write(output_pdf_file)

        self.debug_message(f"First page removed. Pages up to page {end_page} saved in {output_pdf}")
        if self.witnesses_start_page is not None:
            self.debug_message(f"Witnesses pages: from {self.witnesses_start_page} to {self.witnesses_end_page} appended to {output_pdf}")
            self.debug_message(f"New Witnesses pages: from {witnesses_new_start_page} to {witnesses_new_end_page}")
        if self.evidence_start_page is not None:
            self.debug_message(f"Published written evidence pages: from {self.evidence_start_page} to {self.evidence_end_page} appended to {output_pdf}")
            self.debug_message(f"New Published written evidence pages: from {evidence_new_start_page} to {evidence_new_end_page}")

        return (witnesses_new_start_page, witnesses_new_end_page), (evidence_new_start_page, evidence_new_end_page)

    def search_question_numbers(self, pdf_path):
        """
        Searches for question numbers in the format 'Q<digits>' within the PDF.

        Args:
            pdf_path (str): The path to the input PDF file.

        Returns:
            list: A list of tuples containing question numbers and their corresponding page numbers.
        """

        question_numbers = []
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            matches = re.findall(r'Q\d+', text)
            for match in matches:
                question_numbers.append((match, page_num + 1))

        doc.close()
        return question_numbers

    def rotate_and_resize_pdf(self, pdf_path, page_num, output_path):
        """
        Rotates the specified landscape-oriented page in the given PDF to portrait orientation and resizes the page to A4 dimensions.
        Saves the modified page as a new PDF.

        Args:
            pdf_path (str): The path to the input PDF file.
            output_path (str): The path where the modified PDF will be saved.
            page_num (int): The page number to be modified (0-indexed).
        """

        doc = fitz.open(pdf_path)
        new_doc = fitz.open()
        
        if 0 <= page_num < len(doc):
            page = doc.load_page(page_num)
            # Rotate if the page is landscape
            if page.rect.width > page.rect.height:
                page.set_rotation(270)
            # Resize to A4 dimensions
            page.set_mediabox(fitz.Rect(0, 0, 842, 595))  # A4 size in points (width=595, height=842)
            
            # Insert the modified page into the new document
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            # Save the new document with the single modified page
            new_doc.save(output_path)
            self.debug_message(f"Modified page saved to {output_path}")
        else:
            self.debug_message(f"Page number {page_num} is out of range.")
        
        doc.close()
        new_doc.close()

    def is_page_blank(self, page):
        text_blocks = page.get_text("dict")["blocks"]
        images = page.get_images(full=True)
        return len(text_blocks) == 0 and len(images) == 0

    def check_blank_pages(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        blank_pages = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            is_blank = self.is_page_blank(page)
            blank_pages.append((page_number, is_blank))
        return blank_pages

    def concatenate_pdfs(self, pdf_list, output_path, published_evidence=False, witness_evidence=False):
        writer = PdfWriter()
        page_indices = []
        current_page_index = 0

        question_numbers = []
        pdf_question_ranges = {}
        pdf_start_pages = {}

        a4_width, a4_height = A4

        blank_pages_info = {pdf: self.check_blank_pages(pdf) for pdf in pdf_list}

        for pdf in pdf_list:
            with open(pdf, "rb") as input_pdf:
                reader = PdfReader(input_pdf)

                if published_evidence or witness_evidence:
                    pdf_start_pages[pdf] = current_page_index + 1

                if witness_evidence:
                    current_pdf_questions = self.search_question_numbers(pdf)
                    adjusted_questions = [(q, p + current_page_index) for q, p in current_pdf_questions]
                    question_numbers.extend(adjusted_questions)
                    if adjusted_questions:
                        first_question = adjusted_questions[0][0]
                        last_question = adjusted_questions[-1][0]
                        pdf_question_ranges[pdf] = (first_question, last_question)

                blank_pages = blank_pages_info[pdf]
                for page_number, page in enumerate(reader.pages):
                    is_blank = blank_pages[page_number][1]
                    if not is_blank:
                        page_width = float(page.mediabox.width)
                        page_height = float(page.mediabox.height)

                        self.debug_message(f"\nProcessing page {page_number + 1} of PDF '{pdf}'")
                        self.debug_message(f"Original page size: {page_width} x {page_height}")

                        if (page_width != a4_width) or (page_height != a4_height):
                            self.debug_message(f"Page {page_number + 1} of PDF '{pdf}' is not A4 size.")

                        if (published_evidence or witness_evidence) and page_number == 0:
                            page_indices.append(current_page_index)

                        if page.get('/RotateProcessed') is None:
                            rotation_angle = (page.get('/Rotate') or 0) % 360
                            if page_width > page_height and rotation_angle == 0:
                                self.debug_message("Page needs rotation to portrait orientation")

                                rotated_pdf_path = f"rotated_temp_page_{page_number + 1}.pdf"
                                self.rotate_and_resize_pdf(pdf, page_number, rotated_pdf_path)

                                with open(rotated_pdf_path, "rb") as rotated_pdf:
                                    rotated_reader = PdfReader(rotated_pdf)
                                    for rotated_page in rotated_reader.pages:
                                        rotated_page[NameObject('/RotateProcessed')] = TextStringObject("True")
                                        writer.add_page(rotated_page)

                                os.remove(rotated_pdf_path)

                            else:
                                scale_width = a4_width / page_width
                                scale_height = a4_height / page_height
                                scale_factor = min(scale_width, scale_height)

                                self.debug_message(f"Scaling factor: {scale_factor}")

                                packet = BytesIO()
                                temp_canvas = canvas.Canvas(packet, pagesize=A4)
                                temp_canvas.scale(scale_factor, scale_factor)
                                temp_canvas.drawString(0, 0, "")
                                temp_canvas.save()
                                packet.seek(0)
                                new_pdf = PdfReader(packet)
                                new_page = new_pdf.pages[0]

                                transformation = Transformation().scale(scale_factor)
                                page.add_transformation(transformation)
                                new_page.merge_page(page)

                                new_page[NameObject('/RotateProcessed')] = TextStringObject("True")

                                writer.add_page(new_page)
                        else:
                            writer.add_page(page)

                        current_page_index += 1

        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        if witness_evidence:
            self.debug_message("Question Numbers, their Pages, and Page Numbers:")
            for question, page in question_numbers:
                self.debug_message(f"{question}: {page}")

            self.debug_message("\nPDF Question Ranges:")
            for pdf, (first_question, last_question) in pdf_question_ranges.items():
                self.debug_message(f"{pdf}: {first_question} to {last_question}")

        if published_evidence or witness_evidence:
            self.debug_message("\nPDF Start Pages:")
            for pdf, start_page in pdf_start_pages.items():
                self.debug_message(f"{pdf}: {start_page}")

        if published_evidence and not witness_evidence and (self.witness_pages and self.witness_pages != (None, None)):
            first_pdf_key = next(iter(pdf_start_pages))
            pdf_start_pages.pop(first_pdf_key)
            return pdf_start_pages
        elif witness_evidence and not published_evidence:
            return pdf_question_ranges, pdf_start_pages, question_numbers
        elif published_evidence and not witness_evidence and (self.witness_pages and self.witness_pages == (None, None)):
            return pdf_start_pages
        else:
            return None

    def extract_and_identify_questions(self, trimmed_pdf_path, pdf_question_ranges):
        """
        Extracts question numbers and dates from a trimmed PDF, then identifies the corresponding original PDF for each question.

        Args:
            trimmed_pdf_path (str): Path to the trimmed PDF file.
            pdf_question_ranges (dict): Dictionary mapping PDF paths to their question number ranges.

        Returns:
            pdf_to_questions (dict): A dictionary mapping each PDF path to its corresponding list of extracted question numbers.
        """
        self.debug_message(pdf_question_ranges)

        doc = fitz.open(trimmed_pdf_path)
        date_to_questions = []
        current_questions = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            lines = text.split('\n')
            
            for line in lines:
                if self.contains_date(line):
                    if current_questions:
                        date_to_questions.append(current_questions)
                    current_questions = []
                    self.debug_message(f"Found date: {line.strip()}")
                
                matches = re.findall(r'Q\d+', line)
                if matches:
                    current_questions.extend(matches)
                    self.debug_message(f"Found questions: {matches}")
        
        if current_questions:
            date_to_questions.append(current_questions)

        doc.close()

        self.debug_message(f"Date to Questions:, {date_to_questions}")

        # Convert question ranges to integers and store them
        pdf_ranges_sorted = sorted(pdf_question_ranges.items(), key=lambda item: int(item[1][0][1:]))
        pdf_ranges_sorted_int = [(pdf, (int(first_question[1:]), int(last_question[1:])))
                                for pdf, (first_question, last_question) in pdf_ranges_sorted]

        self.debug_message(f"PDF Ranges (with integer question numbers):, {pdf_ranges_sorted_int}")

        pdf_to_questions = {pdf: [] for pdf, _ in pdf_ranges_sorted_int}

        # Iterate through both lists to map questions to their corresponding PDFs
        for idx, questions in enumerate(date_to_questions):
            if idx < len(pdf_ranges_sorted_int):
                pdf_path, (first_question_number, last_question_number) = pdf_ranges_sorted_int[idx]
                for match in questions:
                    if first_question_number <= int(match[1:]) <= last_question_number:
                        pdf_to_questions[pdf_path].append(match)

        self.debug_message("\nExtracted Questions and their Corresponding PDFs:")
        for pdf, questions in pdf_to_questions.items():
            self.debug_message(f"{pdf}: {questions}")

        self.debug_message(pdf_to_questions)
        return pdf_to_questions
    
    def find_witness_markers(self, questions_in_pdf, witness_start_pages, question_numbers):
        """
        Finds witness markers for each question in the provided PDFs.

        Args:
            questions_in_pdf (dict): Dictionary mapping PDF paths to lists of question numbers.
            witness_start_pages (dict): Dictionary mapping PDF paths to their start pages.
            question_numbers (list): List of tuples with question numbers and their respective page numbers.

        Returns:
            witness_markers (list): List of witness markers as strings in the format "Ev <page number>".
        """
        witness_markers = []

        for pdf_path, questions in questions_in_pdf.items():
            start_page = witness_start_pages[pdf_path]

            for i, question in enumerate(questions):
                if i == 0:  # If it's the first question in the PDF, use the start page
                    marker = start_page
                else:  # Otherwise, find the appropriate page number for the question
                    page_number = next((page for q, page in question_numbers if q == question and page >= start_page), None)
                    marker = page_number if page_number is not None else start_page

                witness_markers.append(f"Ev {marker}")

                self.debug_message(witness_markers)

        return witness_markers

    def add_numbers(self, committee_name, input_pdf, output_pdf):
        """
        Adds page numbers and committee name to each page of a PDF, considering page orientation
        and whether or not a page is odd or even.

        Args:
            committee_name (str): Name of the committee to be included in the text.
            input_pdf (str): Path to the input PDF file.
            output_pdf (str): Path where the modified PDF will be saved.
        """

        with fitz.open(input_pdf) as pdf_file:
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                rotation = page.rotation

                text = f"Ev {page_index + 1} {committee_name}: Evidence"
                text_width = fitz.get_text_length(text, fontsize=8)

                margin_height = 20
                margin_width = 50

                if rotation == 0:
                    x_pos_odd = page.rect.width - margin_width - text_width
                    y_pos_odd = margin_height
                    x_pos_even = margin_width
                    y_pos_even = margin_height
                elif rotation == 270:
                    self.debug_message("page is rotated 270 deg adjusting EV position")
                    x_pos_odd = page.rect.height - margin_height
                    y_pos_odd = page.rect.width - margin_width - text_width
                    x_pos_even = page.rect.height - margin_height 
                    y_pos_even = margin_width
                if (page_index + 1) % 2 == 0:
                    page.insert_text((x_pos_even, y_pos_even), text, fontsize=8, rotate=rotation)
                else:
                    page.insert_text((x_pos_odd, y_pos_odd), f"{committee_name}: Evidence Ev {page_index + 1}", fontsize=8, rotate=rotation)

            pdf_file.save(output_pdf)

    def extract_committee_name(self, pdf_path):
        """
        Extracts the committee name from the first page of a PDF.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: The extracted committee name if found, otherwise None.
        """

        committees = []
        layout_analysis_parameters = LAParams(line_margin=0.2)

        for page_num, page_layout in enumerate(extract_pages(pdf_path, laparams=layout_analysis_parameters), start=1):
            if page_num == 1:
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        for text_line in element:
                            if isinstance(text_line, LTTextLine):
                                text = text_line.get_text()
                                if "Committee" in text:
                                    header = {
                                        "text": text.strip(),
                                        "page": page_num
                                    }
                                    committees.append(header)

        if committees:
            committee_name = committees[0]['text']
            if committee_name.startswith("The "):
                committee_name = committee_name[4:]  # Remove "The " (4 characters)

            self.debug_message(f"Extracted the following committee name: {committee_name} from {pdf_path}")

            return committee_name
        else:
            return None

    def get_page_size(self, input_pdf_path):
        """
        Retrieves the dimensions of the first page of a PDF.

        Args:
            input_pdf_path (str): Path to the input PDF file.

        Returns:
            width (T_num): Width of the first page of the PDF
            height (T_num): Height of the first page of the PDF
        """

        with pdfplumber.open(input_pdf_path) as pdf:
            first_page = pdf.pages[0]
            width = first_page.width
            height = first_page.height
        return width, height

    def extract_lines_from_pdf(self, pdf_path):
        """
        Extracts line coordinates from each page of a PDF.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            lines_by_page (dict): Dictionary mapping page numbers to lists of line coordinates.
        """

        lines_by_page = {}
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                lines_by_page[page_number + 1] = page.lines
        return lines_by_page

    def draw_lines_on_pdf(self, input_pdf_path, output_pdf_path, min_line_width, start_page, x_offset, witness_pages=None, published_pages=None):
        """
        Draws lines on a PDF, optionally handling overlapping pages and customizing line properties.

        Args:
            input_pdf_path (str): Path to the input PDF file.
            output_pdf_path (str): Path where the output PDF with lines will be saved.
            min_line_width (float): Minimum width of lines to be drawn.
            start_page (int): The page number to start drawing lines from.
            x_offset (float): Horizontal offset for drawing lines.
            witness_pages (list, optional): List of witness pages to check for overlap.
            published_pages (list, optional): List of published pages to check for overlap.
        """

        line_color = (0, 0.391, 0.188) # Green
        page_width, page_height = self.get_page_size(input_pdf_path)
        temp_canvas = canvas.Canvas(output_pdf_path, pagesize=(page_width, page_height))

        lines_by_page = self.extract_lines_from_pdf(input_pdf_path)

        overlapping_page = None
        if witness_pages and published_pages:
            if witness_pages[0] == published_pages[0] and witness_pages[1] == published_pages[1]:
                overlapping_page = witness_pages[0]

        with pdfplumber.open(input_pdf_path) as pdf:
            for page_number in range(start_page, len(pdf.pages)):
                if page_number + 1 in lines_by_page:
                    lines = lines_by_page[page_number + 1]
                    if lines:
                        line_drawn = False
                        for i, line in enumerate(lines):
                            if line['width'] > min_line_width:
                                if overlapping_page and page_number + 1 == overlapping_page and not line_drawn:

                                    y0 = page_height - line['top']
                                    y1 = page_height - line['bottom']
                                    temp_canvas.setStrokeColorRGB(line_color[0], line_color[1], line_color[2])
                                    temp_canvas.setLineWidth(1) 
                                    x0 = line['x0'] + x_offset
                                    x1 = line['x1'] + x_offset
                                    temp_canvas.line(x0, y0, x1, y1)

                                    temp_canvas.showPage()
                                    temp_canvas.setStrokeColorRGB(line_color[0], line_color[1], line_color[2])
                                    temp_canvas.setLineWidth(1)
                                    y0 = page_height - line['top']
                                    y1 = page_height - line['bottom']
                                    temp_canvas.line(x0, y0, x1, y1)

                                    line_drawn = True
                                    temp_canvas.showPage()
                                    break
                                elif not overlapping_page:

                                    y0 = page_height - line['top']
                                    y1 = page_height - line['bottom']
                                    temp_canvas.setStrokeColorRGB(line_color[0], line_color[1], line_color[2]) 
                                    temp_canvas.setLineWidth(1) 
                                    x0 = line['x0'] + x_offset
                                    x1 = line['x1'] + x_offset
                                    temp_canvas.line(x0, y0, x1, y1)

                        if not line_drawn:
                            temp_canvas.showPage()

        temp_canvas.save()

    def merge_first_page(self, first_pdf, second_pdf, output_pdf_path, last_page):
        """
        Merges the first page of one PDF with all pages of another PDF, preserving content.

        Args:
            first_pdf (str): Path to the first PDF file.
            second_pdf (str): Path to the second PDF file (overlay).
            output_pdf_path (str): Path where the merged PDF will be saved.
        """

        pdf_reader = PdfReader(first_pdf)
        overlay_reader = PdfReader(second_pdf)
        pdf_writer = PdfWriter()

        for page_number in range(last_page):
            page = pdf_reader.pages[page_number]
            pdf_writer.add_page(page)

        for page_number in range(len(overlay_reader.pages)):
            overlay_page = overlay_reader.pages[page_number]
            pdf_writer.add_page(overlay_page)

        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        self.debug_message(f"Merged the first page of trimmed_pdf.pdf and the lines pdf")

    def contains_date(self, text):
        # Simple regex to match dates like 'Tuesday 26 March 2024'
        date_pattern = r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b'
        return re.search(date_pattern, text) is not None

    def analyze_pdf(self, pdf_path):
        """
        Extracts and categorizes text elements related to witnesses and published evidence from PDF pages.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            witness_text (list): A lists containing witness-related text.
            published_text (list): A list containing published-related text.
        """

        doc = fitz.open(pdf_path)
        all_text_elements = []

        for page_num in range(1, len(doc)):
            page = doc[page_num]
            page_styles = self.get_text_style(page)

            page_styles = page_styles[2:]

            for style in page_styles:
                style['page'] = page_num + 1
                all_text_elements.append(style)

        all_text_elements.sort(key=lambda x: (x['page'], x['origin'][1]))

        witness_found = False
        date_found = False
        published_found = False
        one_found = False

        witness_text = []
        published_text = []

        for style in all_text_elements:
            text = style["text"].strip()
            if "Witnesses" in text:
                witness_found = True
                witness_text.append(style)
            elif "Published written evidence" in text:
                published_found = True
                published_text.append(style)
            elif published_found and text == "1":
                one_found = True
                published_text.append(style)
            elif witness_found and self.contains_date(text):
                date_found = True
                witness_text.append(style)
            elif witness_found and date_found and not published_found:
                witness_text.append(style)
            elif one_found:
                published_text.append(style)

        self.debug_message(witness_text)
        self.debug_message(published_text)
        return witness_text, published_text

    def int_to_rgb(self, color_int):
        b = color_int & 255
        g = (color_int >> 8) & 255
        r = (color_int >> 16) & 255
        return (r, g, b)

    def get_string_width(self, text, font_name, font_size):
        return pdfmetrics.stringWidth(text, font_name, font_size)

    def calculate_tracking_for_lines(self, text_dict_list, max_width=300):
        """
        Calculate the width, remaining space, and tracking for each line of text.

        Args:
            text_dict_list (list): List of dictionaries containing text styles with 'origin', 'page', 'text', 'font', and 'size'.
            max_width (int, optional): Maximum width for each line. Defaults to 300.

        Returns:
            tracking_info (list): List of dictionaries containing page, y-coordinate, text details, and calculated tracking adjustments.
        """

        grouped_lines = {}

        for text_dict in text_dict_list:
            y = text_dict['origin'][1]
            page = text_dict['page']
            key = (page, y)

            if key not in grouped_lines:
                grouped_lines[key] = []

            grouped_lines[key].append(text_dict)

        no_adjust_lines = set()
        for key, texts in grouped_lines.items():
            for text_dict in texts:
                text = text_dict['text']
                if re.match(r'^\s*Q\d+–\d+$', text) or text == "Witnesses" or self.contains_date(text):
                    no_adjust_lines.add(key)
                    break 

        tracking_info = []
        for key, texts in grouped_lines.items():
            page, y = key
            if key in no_adjust_lines:

                for text_dict in texts:
                    tracking_info.append({
                        'page': page,
                        'y': y,
                        'text_dict': text_dict,
                        'tracking': 0 
                    })
                continue

            total_width = 0
            total_text = ''
            space_count = 0

            for text_dict in texts:
                text = text_dict['text']
                font_name = text_dict['font']
                font_size = text_dict['size']

                space_count += text.count(' ')

                total_text += text

                text_width = pdfmetrics.stringWidth(text.replace(' ', ''), font_name, font_size)
                total_width += text_width

            if space_count > 0:
                remaining_space = max_width - total_width
                tracking = remaining_space / space_count
            else:
                tracking = 0

            for text_dict in texts:
                tracking_info.append({
                    'page': page,
                    'y': y,
                    'text_dict': text_dict,
                    'tracking': tracking
                })

        return tracking_info

    def adjust_q_elements(self, text_dict_list, text_y_shift):
        """
        Adjusts the vertical position of elements identified as Q-elements to align with the start of paragraphs.

        Args:
            text_dict_list (list): List of dictionaries containing text styles with 'y', 'page', and 'text_dict'.
            text_y_shift (int): Vertical shift to adjust for differences in paragraph start.

        Returns:
            text_dict_list list[dict]: An updated version of text_dict_list with adjusted q_elements.       
        """

        def find_paragraph_start(q_element_index, elements):
            q_element = elements[q_element_index]
            page = q_element['page']
            current_y = q_element['y']
            last_valid_y = current_y

            for i in range(q_element_index - 1, -1, -1):
                y_difference = current_y - elements[i]['y']
                if elements[i]['page'] == page:
                    if y_difference > 12:
                        last_valid_y = elements[i + 1]['y']
                        return last_valid_y, page
                    current_y = elements[i]['y']
                    last_valid_y = current_y
                else:
                    self.debug_message(f"Reached top of page at index {i} with y={elements[i]['y']} on page {elements[i]['page']}")
                    break

            for i in range(q_element_index - 1, -1, -1):
                if elements[i]['page'] != page:
                    if elements[i]['y'] > 770 - text_y_shift:  # 794 - 24 = 770
                        last_valid_y = elements[i]['y']
                        last_valid_page = elements[i]['page']
                        current_y = elements[i]['y']

                        for j in range(i - 1, -1, -1):
                            if elements[j]['page'] != last_valid_page:
                                break
                            y_difference = current_y - elements[j]['y']
                            if y_difference > 12:
                                last_valid_y = elements[j + 1]['y']

                                return last_valid_y, last_valid_page
                            current_y = elements[j]['y']
                            last_valid_y = current_y 
                        return last_valid_y, last_valid_page
                    else:
                        self.debug_message(f"Breaking at index {i} because of page change from {elements[i]['page']} to {page} and y={elements[i]['y']} is not close enough to bottom")
                        break

            return last_valid_y, page

        q_pattern = re.compile(r'^\s*Q\d+–\d+$')

        for i, element in enumerate(text_dict_list):
            if q_pattern.match(element['text_dict']['text']):
                original_y = element['y']
                new_y, new_page = find_paragraph_start(i, text_dict_list)

                element['y'] = new_y
                element['page'] = new_page
                text_dict = element['text_dict']
                text_dict['origin'] = (425, new_y)
                text_dict['color'] = 0

        return text_dict_list

    def text_on_same_line(self, data):
        """
        Groups text elements by their y-coordinate within each page.

        Args:
            data (list): List of dictionaries containing text styles with 'origin' and 'page'.

        Returns:
            grouped_lines (dict): Dictionary mapping page numbers to dictionaries mapping same y-coordinates to lists of text styles.
        """
        
        grouped_lines = {}
        for entry in data:
            page = entry['page']
            y = entry['origin'][1]
            if page not in grouped_lines:
                grouped_lines[page] = {}
            if y not in grouped_lines[page]:
                grouped_lines[page][y] = []
            grouped_lines[page][y].append(entry)
        return grouped_lines

    def adjust_x_coordinates(self, data):
        text_grouped_by_lines = self.text_on_same_line(data)
        self._adjust_x_coordinates(text_grouped_by_lines)
        return self.flatten_lines(text_grouped_by_lines)

    def _adjust_x_coordinates(self, grouped_lines):
        """
        Adjusts x-coordinates of text elements within lines to align them properly.

        Args:
            grouped_lines (dict): Dictionary mapping page numbers to dictionaries mapping same y-coordinates to lists of text styles.
        """

        for page, elements_by_y in grouped_lines.items():
            for y, elements in elements_by_y.items():
                offset = 0
                for element in elements:
                    original_width = self.get_string_width(element['text'], element['font'], element['size'])
                    reduced_size = element['size'] - 1
                    new_width = self.get_string_width(element['text'], element['font'], reduced_size)
                    diff = original_width - new_width

                    element['origin'] = (element['origin'][0] - offset, element['origin'][1])

                    offset += diff

                    element['size'] = reduced_size

    def flatten_lines(self, grouped_lines):
        """
        Flattens grouped lines of text elements into a single list.

        Args:
            grouped_lines (dict): Dictionary mapping page numbers to dictionaries mapping y-coordinates to lists of text styles.

        Returns:
            flattened_lines (list): Flattened list of text styles.
        """
        
        flattened_lines = []
        for page in sorted(grouped_lines.keys()):
            for y in sorted(grouped_lines[page].keys()):
                flattened_lines.extend(grouped_lines[page][y])
        return flattened_lines

    def get_string_width(self, text, font_name, font_size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        return stringWidth(text, font_name, font_size)

    def witness_evs(self, text_dict_list, witness_markers):
        """
        Inserts witness markers into the text_dict_list at positions identified by Q-elements.

        Args:
            text_dict_list (list[dict]): List of dictionaries containing text styles with 'text_dict', 'y', and 'page'.
            witness_markers (list): List of strings representing witness markers.

        Returns:
            text_dict_list (list[dict]): Updated text_dict_list inserted witness markers.
        """

        number_positions = {}
        q_pattern = re.compile(r'^\s*Q\d+–\d+$')

        for item in text_dict_list:
            text = item['text_dict']['text'].strip()
            self.debug_message(f"Inspecting text: '{text}'")
            if q_pattern.match(text):
                page = item['page']
                y_coordinate = item['y']
                if page not in number_positions:
                    number_positions[page] = []
                number_positions[page].append((text, y_coordinate))
                self.debug_message(f"Found pattern: {text} on page {page} at y: {y_coordinate}")

        evs = []
        x_coordinate = 480 
        marker_index = 0  

        for page, positions in number_positions.items():
            for _, y_coordinate in positions:
                if marker_index < len(witness_markers):
                    marker = witness_markers[marker_index]
                    marker_index += 1
                    new_text_dict = {
                        'text': marker,
                        'font': 'FrutigerLTStd-Roman',
                        'size': 9,
                        'color': 2771610,
                        'origin': (x_coordinate, y_coordinate),
                        'page': page
                    }
                    evs.append({
                        'page': page,
                        'y': y_coordinate,
                        'text_dict': new_text_dict,
                        'tracking': 0
                    })

        text_dict_list.extend(evs)
        text_dict_list.sort(key=lambda x: (x['page'], x['y']))

        return text_dict_list

    def published_evs(self, text_dict_list, published_markers):
        """
        Inserts published evidence markers into the text_dict_list at positions identified by numbered elements.

        Args:
            text_dict_list (list[dict]): List of dictionaries containing text styles with 'text', 'page', and 'origin'.
            published_markers (list): List of strings representing published evidence markers.

        Returns:
            text_dict_list (list[dict]): Updated text_dict_list inserted published evidence markers.
        """

        number_positions = {}
        evidence_code_pattern = re.compile(r'\b[A-Z]+\d+\b')

        for item in text_dict_list:
            text = item['text'].strip()
            if text.isdigit():
                number = int(text)
                page = item['page']
                y_coordinate = item['origin'][1]
                if page not in number_positions:
                    number_positions[page] = {}
                number_positions[page][number] = y_coordinate
                self.debug_message(f"Found number: {number} on page {page} at y: {y_coordinate}")

        page_data = {}
        for item in text_dict_list:
            page = item['page']
            if page not in page_data:
                page_data[page] = []
            page_data[page].append(item)

        new_elements = []
        marker_index = 0

        for page, items in page_data.items():
            current_number = None
            current_y = None
            evidence_count = 0

            for item in items:
                text = item['text'].strip()
                y_coordinate = item['origin'][1]

                if text.isdigit():
                    if current_number is not None and evidence_count > 0:
                        for i in range(evidence_count):
                            if marker_index < len(published_markers):
                                new_elements.append({
                                    'text': published_markers[marker_index],
                                    'font': 'FrutigerLTStd-Roman',
                                    'size': 9,
                                    'color': 2771610,
                                    'origin': (480 + i * 35, current_y),
                                    'page': page
                                })
                                marker_index += 1
                            else:
                                break
                    current_number = int(text)
                    current_y = y_coordinate
                    evidence_count = 0

                elif evidence_code_pattern.fullmatch(text):
                    evidence_count += 1
                    self.debug_message(f"Found evidence code: {text} on page {page} at y: {y_coordinate}")

            if current_number is not None and evidence_count > 0:
                for i in range(evidence_count):
                    if marker_index < len(published_markers):
                        new_elements.append({
                            'text': published_markers[marker_index],
                            'font': 'FrutigerLTStd-Roman',
                            'size': 9,
                            'color': 2771610,
                            'origin': (480 + i * 20, current_y),
                            'page': page
                        })
                        marker_index += 1
                    else:
                        break

        self.debug_message(new_elements)
        text_dict_list.extend(new_elements)
        text_dict_list.sort(key=lambda x: (x['page'], x['origin'][1]))

        return text_dict_list

    def draw_text_with_tracking(self, text_dict_list, input_pdf_path, output_pdf_path, markers, text_y_shift):
        """
        Draws text with tracking adjustments on existing PDF pages and returns updated text dictionaries.

        Args:
            text_dict_list (list): List of dictionaries containing text styles with 'text_dict', 'y', and 'page'.
            input_pdf_path (str): Path to the input PDF file.
            output_pdf_path (str): Path to save the output PDF file.
            markers (list): List of strings representing markers.
            text_y_shift (int): Vertical shift for text elements.

        Returns:
            updated_text_dict (list[dict]): Updated list of dictionaries with modified text dictionaries.
        """

        if not os.path.exists(input_pdf_path):
            self.debug_message(f"Error: Input PDF '{input_pdf_path}' does not exist.")
            return

        existing_pdf = PdfReader(input_pdf_path)
        output = PdfWriter()

        updated_text_dicts = []
        adjusted_x = self.adjust_x_coordinates(text_dict_list)

        tracking_info = self.calculate_tracking_for_lines(adjusted_x)

        tracking_info = self.adjust_q_elements(tracking_info, text_y_shift)
        tracking_info = self.witness_evs(tracking_info, markers)

        tracking_info_by_page = {}
        for info in tracking_info:
            page = info['page']
            if page not in tracking_info_by_page:
                tracking_info_by_page[page] = []
            tracking_info_by_page[page].append(info)

        for page_num in range(len(existing_pdf.pages)):
            current_page = existing_pdf.pages[page_num]
            packet = BytesIO()
            temp_canvas = canvas.Canvas(packet, pagesize=A4)

            width, height = A4

            if page_num + 1 in tracking_info_by_page:
                page_tracking_info = tracking_info_by_page[page_num + 1]

                x_positions = {}
                for info in page_tracking_info:
                    entry = info['text_dict']
                    tracking_value = info['tracking']
                    original_text = entry['text']

                    temp_canvas.setFont(entry['font'], entry['size'])

                    r, g, b = self.int_to_rgb(entry['color'])
                    temp_canvas.setFillColor(Color(r / 255, g / 255, b / 255))

                    x, y = entry['origin']
                    y = height - y

                    current_x = x_positions.get(y, x)

                    non_movable = re.match(r'^\s*Q\d+–\d+$', original_text) or original_text == "Witnesses" or self.contains_date(original_text) or original_text in markers
                    if non_movable:
                        temp_canvas.drawString(x, y, original_text)

                        x_positions[y] = x + temp_canvas.stringWidth(original_text)
                    elif tracking_value == 0:

                        temp_canvas.drawString(current_x, y, original_text)
                        current_x += temp_canvas.stringWidth(original_text)

                        x_positions[y] = current_x
                    else:

                        for char in original_text:
                            temp_canvas.drawString(current_x, y, char)
                            current_x += temp_canvas.stringWidth(char) + (tracking_value if char == ' ' else 0)

                        x_positions[y] = current_x

                    entry['origin'] = (x_positions[y], entry['origin'][1])
                    updated_text_dicts.append(entry)

                temp_canvas.save()

                packet.seek(0)

                new_pdf = PdfReader(packet)

                if len(new_pdf.pages) > 0:
                    new_page = new_pdf.pages[0]
                    current_page.merge_page(new_page)

            output.add_page(current_page)

        with open(output_pdf_path, "wb") as output_file:
            output.write(output_file)

        return updated_text_dicts

    def draw_text(self, text_dict_list, input_pdf_path, output_pdf_path, text_shift=0, markers=None):
        """
        Draws text on existing PDF pages and returns updated text dictionaries.

        Args:
            text_dict_list (list): List of dictionaries containing text styles with 'text', 'page', and 'origin'.
            input_pdf_path (str): Path to the input PDF file.
            output_pdf_path (str): Path to save the output PDF file.
            text_shift (int, optional): Horizontal shift for text elements (default is 0).
            markers (list, optional): List of strings representing markers.

        Returns:
            text_dict_list list[dict]: Updated list of dictionaries with modified text dictionaries.
        """

        if not os.path.exists(input_pdf_path):
            self.debug_message(f"Error: Input PDF '{input_pdf_path}' does not exist.")
            return

        if text_shift is not None:
            if isinstance(text_shift, (int, float)):
                for entry in text_dict_list:
                    x, y = entry['origin']
                    x += text_shift
                    entry['origin'] = (x, y)
            else:
                raise TypeError("text_shift must be a number (int or float)")

        existing_pdf = PdfReader(input_pdf_path)
        output = PdfWriter()

        text_dict_list = self.adjust_x_coordinates(text_dict_list)
        if markers:
            text_dict_list = self.published_evs(text_dict_list, markers)

        for page_num in range(len(existing_pdf.pages)):
            packet = BytesIO()
            temp_canvas = canvas.Canvas(packet, pagesize=A4)

            width, height = A4

            for entry in text_dict_list:
                if entry['page'] - 1 != page_num:
                    continue

                temp_canvas.setFont(entry['font'], entry['size'])

                r, g, b = entry['color'] >> 16, (entry['color'] >> 8) & 0xFF, entry['color'] & 0xFF
                temp_canvas.setFillColor(Color(r / 255, g / 255, b / 255))

                x, y = entry['origin']
                y = height - y

                temp_canvas.drawString(x, y, entry['text'])

            temp_canvas.save()

            packet.seek(0)

            new_pdf = PdfReader(packet)

            page = existing_pdf.pages[page_num]
            if len(new_pdf.pages) > 0:
                overlay = new_pdf.pages[0]
                page.merge_page(overlay)

            output.add_page(page)

        with open(output_pdf_path, 'wb') as f:
            output.write(f)

        self.debug_message(f"PDF with added text saved to '{output_pdf_path}'.")

        return text_dict_list

    def re_write_pdf(self, text_dict_list, temp_pdf_path, output_pdf_path, witness_pages, published_pages, markers, witness=False, published=False):
        """
        Rewrites the PDF with the provided text dictionaries, optionally adjusting for witness and published evidence.

        Args:
            text_dict_list (list): List of dictionaries containing text styles with 'text', 'page', and 'origin'.
            temp_pdf_path (str): Path to a temporary PDF file for intermediate processing.
            output_pdf_path (str): Path to save the output PDF file.
            witness_pages (tuple): Tuple of witness pages.
            published_pages (tuple): Tuple of published pages.
            markers (list): List of strings representing markers.
            witness (bool, optional): Flag indicating if witness evidence adjustment is needed (default is False).
            published (bool, optional): Flag indicating if published evidence adjustment is needed (default is False).
        """

        stored_y_coord = 101.53961181640625
        witness_text_y_shift = 30

        if published and (witness_pages[0] == published_pages[0]):

            published_pages = tuple(page + 1 for page in published_pages)
            for entry in text_dict_list:
                entry['page'] += 1

        text_dict_list.sort(key=lambda x: (x['page'], x['origin'][1]))

        if published and text_dict_list:
            first_entry_y = text_dict_list[0]['origin'][1]
            shift_amount = first_entry_y - stored_y_coord
            for entry in text_dict_list:
                entry['origin'] = (entry['origin'][0], entry['origin'][1] - shift_amount)

        if not self.register_custom_fonts():
            return

        if witness:
            for entry in text_dict_list:
                if "Witnesses" not in entry['text'] and entry['page'] == witness_pages[0]:
                    x, y = entry['origin']
                    entry['origin'] = (x, y - witness_text_y_shift)

            updated_text_dict = self.draw_text_with_tracking(text_dict_list, temp_pdf_path, output_pdf_path, markers, witness_text_y_shift)

            question_number = {
                'text': 'Question Number',
                'font': 'FrutigerLTStd-Roman',
                'size': 7,
                'color': 0,
                'origin': (416, 141.03961181640625),
                'page': witness_pages[0]
            }
            self.draw_text([question_number], output_pdf_path, output_pdf_path, 0)

        if published:
            for entry in text_dict_list:
                if "Published written evidence" not in entry['text'] and entry['page'] == published_pages[0]:
                    x, y = entry['origin']
                    entry['origin'] = (x, y - 45)

            self.draw_text(text_dict_list, temp_pdf_path, output_pdf_path, 0, markers)

    def get_text_styles_until_font(self, page, stop_font1, stop_font2):
        """
        Extracts text styles from a PDF page until encountering specific font styles.

        Args:
            page (PageObject): Page object from PyMuPDF containing text information.
            stop_font1 (str): First font style to stop collecting text styles.
            stop_font2 (str): Second font style to stop collecting text styles.

        Returns:
            styles list[dict]: List of dictionaries containing text styles with 'text', 'font', 'size', 'color', 'flags', 'origin', and 'page'.
        """

        text_information = []
        encountered_stop_fonts = False
        page_info = page.get_text("dict")["blocks"]

        for section in page_info:
            if "lines" in section:
                for line in section["lines"]:
                    for span in line["spans"]:
                        sanitized_text = self.sanitize_text(span["text"])
                        style = {
                            "text": sanitized_text,
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"],
                            "flags": span["flags"],
                            "origin": span["origin"],
                            "page": page.number + 1
                        }

                        if span["font"] in [stop_font1, stop_font2]:
                            encountered_stop_fonts = True
                            text_information.append(style)
                        else:
                            if encountered_stop_fonts:
                                return text_information
            else:
                self.debug_message("No lines in block:", section)

        return text_information

    def find_hc_text(self, page):
        """
        Finds and returns the first occurrence of "HC <number>" text on a given PDF page.

        Args:
            page (PageObject): Page object from PyMuPDF containing text information.

        Returns:
            sanitized_text (str): Found "HC <number>" text or an empty string if not found.
        """

        hc_pattern = re.compile(r'(HC\s*\d+)')
        page_info = page.get_text("dict")["blocks"]

        for section in page_info:
            if "lines" in section:
                for line in section["lines"]:
                    for span in line["spans"]:
                        sanitized_text = self.sanitize_text(span["text"])
                        match = hc_pattern.search(sanitized_text)
                        if match:
                            sanitized_text = match.group(1)
                            self.debug_message(f"Found HC text: {sanitized_text}")
                            return sanitized_text
        return ""

    def analyze_pdf_until_font(self, pdf_path):
        """
        Analyzes the first page of a PDF until encountering specific font styles, extracting text styles.

        Args:
            pdf_path (str): Path to the PDF file to analyze.

        Returns:
            pdf_styles (list): Tuple containing a list of dictionaries representing text styles.
            HC_text (str): The extracted "HC <number>" text.
        """

        doc = fitz.open(pdf_path)
        pdf_styles = []

        page_num = 0
        page = doc[page_num]

        HC_text = self.find_hc_text(page)

        page_styles = self.get_text_styles_until_font(page, 'FrutigerLTStd-Roman', 'FrutigerLTStd-Bold')
        pdf_styles.extend(page_styles)

        return pdf_styles, HC_text

    def create_first_page(self, pdf_path):
        """
        Analyzes the first page of a PDF, extracts text styles, adds new elements, and returns the modified list of elements.

        Args:
            pdf_path (str): Path to the PDF file to analyze.

        Returns:
            elements (list[dict]): List of dictionaries representing text styles with added elements.
        """

        elements, HC_text = self.analyze_pdf_until_font(pdf_path)

        last_y_position = elements[-1]['origin'][1]

        new_y_position = last_y_position + 40

        new_element = {
            'text': 'Volume II',
            'font': 'FrutigerLTStd-Italic' if self.register_custom_fonts else 'Helvetica-Oblique',
            'size': 17.0,
            'color': 25391,
            'flags': 0,
            'origin': (198.42520141601562, new_y_position),
            'page': 1
        }
        elements.append(new_element)

        last_y_position = elements[-1]['origin'][1]

        new_y_position = last_y_position + 30

        new_element = {
            'text': 'Oral and written evidence',
            'font': 'FrutigerLTStd-Italic' if self.register_custom_fonts else 'Helvetica-Oblique',
            'size': 15.0,
            'color': 25391,
            'flags': 0,
            'origin': (198.42520141601562, new_y_position),
            'page': 1
        }
        elements.append(new_element)

        HC_element = {
            'text': f"{HC_text} - Evidence",
            'font': 'FrutigerLTStd-Roman' if self.register_custom_fonts else 'Helvetica',
            'size': 12,
            'color': 25391,
            'flags': 0,
            'origin': (450, 800),
            'page': 1
        }
        elements.append(HC_element)

        return elements

    def add_annotation(self, page, rect, uri):
        """
        Adds a link annotation to the given page that links to the URI.

        Parameters:
        - page (PageObject): The page to which the annotation is to be added.
        - rect (Rect): The rectangle area for the link annotation.
        - uri (int): Page number we want the annotation to link to.
        """
        
        # Get page width and height
        width = page.rect.width
        height = page.rect.height

        # Add annotation
        annotation = page.insert_link({
            "kind": fitz.LINK_GOTO,
            "page": uri,
            "from": rect,
            "to": fitz.Point(height, 0)
        })
        return annotation

    def create_annotations(self, input_pdf, output_pdf, witness_markers, published_markers):
        """
        Create annotations in a PDF based on the locations and target destinations of the ev markers.

        Args:
            input_pdf (str): Path to the input PDF file.
            output_pdf (str): Path to save the output PDF file with annotations.
            witness_markers (list): List of markers specific to witness evidence.
            published_markers (list): List of markers specific to published evidence.
        """

        all_markers = witness_markers + published_markers

        self.debug_message(all_markers)

        marker_patterns = {marker: re.compile(r'\b' + re.escape(marker) + r'(\b|[.,;!?])') for marker in all_markers}

        document = fitz.open(input_pdf)

        found_markers = {marker: [] for marker in all_markers}

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text_styles = self.get_text_style(page)
            for marker, pattern in marker_patterns.items():
                for style in text_styles:
                    matches = [(m.start(), m.end()) for m in pattern.finditer(style["text"])]
                    for match in matches:
                        found_markers[marker].append({
                            "page": style["page"],
                            "start": match[0],
                            "end": match[1],
                            "origin": style["origin"],
                            "size": style["size"],
                            "text": style["text"]
                        })

        for marker, locations in found_markers.items():
            for i in range(len(locations) - 1):
                source_location = locations[i]
                dest_location = locations[i + 1]

                text_width = (source_location["end"] - source_location["start"]) * source_location["size"] / 2
                text_height = source_location["size"]

                origin_x = source_location["origin"][0]
                origin_y = source_location["origin"][1] - text_height

                rect = fitz.Rect(origin_x, origin_y, origin_x + text_width, origin_y + text_height)

                uri = dest_location['page']

                page = document.load_page(source_location["page"])

                self.debug_message(f"Adding annotation on page {source_location['page']} at {rect} linking to page {uri}")
                self.add_annotation(page, rect, uri)

        document.save(output_pdf)

        self.debug_message(f"Annotations added to: {output_pdf}")

    def create_report(self):
        """
        Calls all the functions to create the report
        """

        self.console_message("    ----- Creating Report -----"); self.console_message("")

        self.console_message("    Using the following folders:")
        self.console_message(f"    Witness Evidence - {self.witness_evidence_folder}")
        self.console_message(f"    Published Written Evidence - {self.published_evidence_folder}")
        self.console_message(f"    Report.pdf - {self.report_pdf}"); self.console_message("")

        self.report_folder = self.report_pdf.rsplit('/', 1)[0]
        
        self.console_message("    Trimming the report to the relevant pages")

        self.witness_pages, self.published_pages = self.trim_pdf(self.report_pdf, "trimmed_pdf.pdf")

        witness_pdfs_list = natsorted([os.path.join(self.witness_evidence_folder, f) for f in os.listdir(self.witness_evidence_folder) if f.endswith('.pdf')])

        self.console_message("    Concatenating Witness Evidence PDFs")

        pdf_question_ranges, witness_start_pages, question_numbers = self.concatenate_pdfs(witness_pdfs_list, "merged_witness_evidence.pdf", witness_evidence=True)

        questions_in_pdf = self.extract_and_identify_questions("trimmed_pdf.pdf", pdf_question_ranges)

        witness_markers = self.find_witness_markers(questions_in_pdf, witness_start_pages, question_numbers)

        published_pdfs_list = natsorted([os.path.join(self.published_evidence_folder, f) for f in os.listdir(self.published_evidence_folder) if f.endswith('.pdf')])

        self.console_message("    Concatenating Published Written Evidence PDFs")

        if (self.witness_pages and self.witness_pages != (None, None)) and (self.published_pages and self.published_pages != (None, None)):
            published_start_pages= self.concatenate_pdfs(["merged_witness_evidence.pdf"] + published_pdfs_list, "merged_evidence.pdf", published_evidence=True)
        elif (self.witness_pages and self.witness_pages == (None, None)):
            published_start_pages= self.concatenate_pdfs(published_pdfs_list, "merged_evidence.pdf", published_evidence=True)
        elif (self.published_pages and self.published_pages == (None, None)):
            published_start_pages= self.concatenate_pdfs(["merged_witness_evidence.pdf"], "merged_evidence.pdf", published_evidence=True)

        published_markers = [f"Ev {str(page)}" for page in sorted(published_start_pages.values())]

        committee_name = self.extract_committee_name("trimmed_pdf.pdf")

        self.console_message(f"    Extracted committe name '{committee_name}'")
        self.console_message("    Adding Ev Page Numbers to evidence")

        self.add_numbers(committee_name,"merged_evidence.pdf", "numbered_evidence.pdf")

        if (self.witness_pages and self.witness_pages != (None, None)) and (self.published_pages and self.published_pages != (None, None)):
            self.draw_lines_on_pdf("trimmed_pdf.pdf", "temp_line_pdf.pdf", 420, self.start_page, 0, self.witness_pages, self.published_pages)
        elif (self.published_pages and self.published_pages == (None, None)):
            self.draw_lines_on_pdf("trimmed_pdf.pdf", "temp_line_pdf.pdf", 420, self.start_page, 0, witness_pages=self.witness_pages)
        elif (self.witness_pages and self.witness_pages == (None, None)):
            self.draw_lines_on_pdf("trimmed_pdf.pdf", "temp_line_pdf.pdf", 420, self.start_page, 0, published_pages=self.published_pages)

        if self.witness_pages and self.witness_pages != (None, None):
            self.merge_first_page("trimmed_pdf.pdf", "temp_line_pdf.pdf", "trimmed_pdf_with_lines.pdf", self.witness_pages[0] - 1)
        else:
            self.merge_first_page("trimmed_pdf.pdf", "temp_line_pdf.pdf", "trimmed_pdf_with_lines.pdf", self.published_pages[0] - 1)

        witness_text, published_text = self.analyze_pdf("trimmed_pdf.pdf")

        self.console_message("    Resizing Contents pages and adding Ev numbers to them")

        if self.published_pages and self.published_pages != (None, None) and self.witness_pages and self.witness_pages != (None, None):
            self.re_write_pdf(witness_text, "trimmed_pdf_with_lines.pdf", "just_witness_pdf.pdf", self.witness_pages, self.published_pages, witness_markers, witness=True)
            self.re_write_pdf(published_text, "just_witness_pdf.pdf", "evidence.pdf", self.witness_pages, self.published_pages, published_markers, published=True)
        elif self.published_pages and self.published_pages != (None, None) and self.witness_pages and self.witness_pages == (None, None):
            self.re_write_pdf(published_text, "trimmed_pdf_with_lines.pdf", "evidence.pdf", self.witness_pages, self.published_pages, published_markers, published=True)
        elif self.witness_pages and self.witness_pages != (None, None) and self.published_pages and self.published_pages == (None, None):
            self.re_write_pdf(witness_text, "trimmed_pdf_with_lines.pdf", "evidence.pdf", self.witness_pages, self.published_pages, witness_markers, witness=True)

        self.console_message("    Creating front page")

        elements = self.create_first_page(self.report_pdf)
        self.draw_lines_on_pdf(self.report_pdf, "front_page_line_pdf.pdf", 10, 0, -70)
        self.draw_text(elements, "front_page_line_pdf.pdf", "front_page.pdf", text_shift=-70)

        self.console_message("    Concatenating contents pages and evidence pages")

        self.concatenate_pdfs(["front_page.pdf", "evidence.pdf", "numbered_evidence.pdf"], f"{self.report_folder}/finished_report.pdf")

        self.console_message("    Annotating Volume II")

        self.create_annotations(f"{self.report_folder}/finished_report.pdf", f"{self.report_folder}/Volume II.pdf", witness_markers, published_markers)

        self.console_message("    Volume II Complete!"); self.console_message("")

        os.remove("evidence.pdf")
        os.remove("numbered_evidence.pdf")
        os.remove("front_page.pdf")
        os.remove("front_page_line_pdf.pdf")
        if self.witness_pages and self.witness_pages != (None, None):
            os.remove("just_witness_pdf.pdf")
        os.remove("merged_witness_evidence.pdf")
        os.remove("merged_evidence.pdf")
        os.remove("temp_line_pdf.pdf")
        os.remove("trimmed_pdf.pdf")
        os.remove("trimmed_pdf_with_lines.pdf")
        os.remove(f"{self.report_folder}/finished_report.pdf")