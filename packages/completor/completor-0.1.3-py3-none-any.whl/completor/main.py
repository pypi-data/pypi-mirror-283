"""Main module of Completor."""

from __future__ import annotations

import logging
import os
import re
import time
from collections.abc import Mapping
from typing import overload

import numpy as np

import completor
from completor import parse
from completor.completion import WellSchedule
from completor.constants import Keywords
from completor.create_output import CreateOutput
from completor.create_wells import CreateWells
from completor.exceptions import CompletorError
from completor.launch_args_parser import get_parser
from completor.logger import handle_error_messages, logger
from completor.read_casefile import ReadCasefile
from completor.utils import abort, clean_file_line, clean_file_lines
from completor.visualization import close_figure, create_pdfpages

try:
    from typing import Literal
except ImportError:
    pass


class FileWriter:
    """Functionality for writing a new schedule file."""

    def __init__(self, file: str, mapper: Mapping[str, str] | None):
        """Initialize the FileWriter.

        Args:
            file: Name of file to be written. Does not check if it already exists.
            mapper: A dictionary for mapping strings.
                Typically used for mapping pre-processor reservoir modelling tools to reservoir simulator well names.
        """
        self.fh = open(file, "w", encoding="utf-8")  # create new output file
        self.mapper = mapper

    @overload
    def write(self, keyword: Literal[None], content: str, chunk: bool = True, end_of_record: bool = False) -> None: ...

    @overload
    def write(
        self, keyword: str, content: list[list[str]], chunk: Literal[True] = True, end_of_record: bool = False
    ) -> None: ...

    @overload
    def write(
        self, keyword: str, content: list[str] | str, chunk: Literal[False] = False, end_of_record: bool = False
    ) -> None: ...

    @overload
    def write(
        self, keyword: str, content: list[list[str]] | list[str] | str, chunk: bool = True, end_of_record: bool = False
    ) -> None: ...

    def write(
        self,
        keyword: str | None,
        content: list[list[str]] | list[str] | str,
        chunk: bool = True,
        end_of_record: bool = False,
    ) -> None:
        """Write the content of a keyword to the output file.

        Args:
            keyword: Reservoir simulator keyword.
            content: Text to be written.
            chunk: Flag for indicating this is a list of records.
            end_of_record: Flag for adding end-of-record ('/').
        """
        txt = ""

        if keyword is None:
            txt = content  # type: ignore  # it's really a formatted string
        else:
            self.fh.write(f"{keyword:s}\n")
            if chunk:
                for recs in content:
                    txt += " " + " ".join(recs) + " /\n"
            else:
                for line in content:
                    if isinstance(line, list):
                        logger.warning(
                            "Chunk is False, but content contains lists of lists, "
                            "instead of a list of strings the lines will be concatenated."
                        )
                        line = " ".join(line)
                    txt += line + "\n"
        if self.mapper:
            txt = self._replace_preprocessing_names(txt)
        if end_of_record:
            txt += "/\n"
        self.fh.write(txt)

    def _replace_preprocessing_names(self, text: str) -> str:
        """Expand start and end marker pairs for well pattern recognition as needed.

        Args:
            text: Text with pre-processor reservoir modelling well names.

        Returns:
            Text with reservoir simulator well names.
        """
        if self.mapper is None:
            raise ValueError(
                f"{self._replace_preprocessing_names.__name__} requires a file containing two "
                "columns with input and output names given by the MAPFILE keyword in "
                f"case file to be set when creating {self.__class__.__name__}."
            )
        start_marks = ["'", " ", "\n", "\t"]
        end_marks = ["'", " ", " ", " "]
        for key, value in self.mapper.items():
            for start, end in zip(start_marks, end_marks):
                my_key = start + str(key) + start
                if my_key in text:
                    my_value = start + str(value) + end
                    text = text.replace(my_key, my_value)
        return text

    def close(self) -> None:
        """Close FileWriter."""
        self.fh.close()


class ProgressStatus:
    """Bookmark the reading progress of a schedule file.

    See https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    for improved functionality.
    """

    def __init__(self, num_lines: int, percent: float):
        """Initialize ProgressStatus.

        Args:
            num_lines: Number of lines in schedule file.
            percent: Indicates schedule file processing progress (in percent).
        """
        self.percent = percent
        self.nlines = num_lines
        self.prev_n = 0

    def update(self, line_number: int) -> None:
        """Update logger information.

        Args:
            line_number: Input schedule file line number.

        Returns:
            Logger info message.
        """
        # If the divisor, or numerator is a float, the integer division gives a float
        n = int((line_number / self.nlines * 100) // self.percent)
        if n > self.prev_n:
            logger.info("=" * 80)
            logger.info("Done processing %i %% of schedule/data file", n * self.percent)
            logger.info("=" * 80)
            self.prev_n = n


def get_content_and_path(case_content: str, file_path: str | None, keyword: str) -> tuple[str | None, str | None]:
    """Get the contents of a file from a path defined by user or case file.

    The method prioritizes paths given as input argument over the paths found in the case file.

    Args:
        case_content: The case file content.
        file_path: Path to file if given.
        keyword: Reservoir simulator keyword.

    Returns:
        File content, file path.

    Raises:
        CompletorError: If the keyword cannot be found.
        CompletorError: If the file cannot be found.
    """
    if file_path is None:
        # Find the path/name of file from case file
        case_file_lines = clean_file_lines(case_content.splitlines())
        start_idx, end_idx = parse.locate_keyword(case_file_lines, keyword)
        # If the keyword is defined correctly
        if end_idx == start_idx + 2:
            # preprocess the text, remove leading/trailing whitespace and quotes
            file_path = " ".join(case_file_lines[start_idx + 1].strip("'").strip(" ").split())
            file_path = re.sub("[\"']+", "", file_path)

        else:
            # OUTFILE is optional, if it's needed but not supplied the error is caught in ReadCasefile:check_pvt_file()
            if keyword == "OUTFILE":
                return None, None
            raise CompletorError(f"The keyword {keyword} is not defined correctly in the casefile")
    if keyword != "OUTFILE":
        try:
            with open(file_path, encoding="utf-8") as file:
                file_content = file.read()
        except FileNotFoundError as e:
            raise CompletorError(f"Could not find the file: '{file_path}'!") from e
        except (PermissionError, IsADirectoryError) as e:
            raise CompletorError("Could not read SCHFILE, this is likely because the path is missing quotes.") from e
        return file_content, file_path
    return None, file_path


# noinspection TimingAttack
# caused by `if token == '...'` and token is interpreted as a security token / JWT
# or otherwise sensitive, but in this context, `token` refers to a token of parsed
# text / semantic token
def create(
    input_file: str,
    schedule_file: str,
    new_file: str,
    show_fig: bool = False,
    percent: float = 5.0,
    paths: tuple[str, str] | None = None,
) -> (
    tuple[list[tuple[str, list[list[str]]]], ReadCasefile, WellSchedule, CreateWells, CreateOutput]
    | tuple[list[tuple[str, list[list[str]]]], ReadCasefile, WellSchedule, CreateWells]
):
    """Create a new Completor schedule file from input case- and schedule files.

    Args:
        input_file: Input case file.
        schedule_file: Input schedule file.
        new_file: Output schedule file.
        show_fig: Flag indicating if a figure is to be shown.
        percent: ProgressStatus percentage steps to be shown (in percent, %).
        paths: Optional additional paths.

    Returns:
        Completor schedule file.
    """
    case = ReadCasefile(case_file=input_file, schedule_file=schedule_file, output_file=new_file)
    wells = CreateWells(case)
    schedule = WellSchedule(wells.active_wells)  # container for MSW-data

    lines = schedule_file.splitlines()

    clean_lines_map = {}
    for line_number, line in enumerate(lines):
        line = clean_file_line(line, remove_quotation_marks=True)
        if line:
            clean_lines_map[line_number] = line

    outfile = FileWriter(new_file, case.mapper)
    chunks = []  # for debug..
    figno = 0
    written = set()  # Keep track of which MSW's has been written
    line_number = 0
    progress_status = ProgressStatus(len(lines), percent)

    pdf_file = None
    if show_fig:
        figure_no = 1
        fnm = f"Well_schematic_{figure_no:03d}.pdf"
        while os.path.isfile(fnm):
            figure_no += 1
            fnm = f"Well_schematic_{figure_no:03d}.pdf"
        pdf_file = create_pdfpages(fnm)
    # loop lines
    while line_number < len(lines):
        progress_status.update(line_number)
        line = lines[line_number]
        keyword = line[:8].rstrip()  # look for keywords

        # most lines will just be duplicated
        if keyword not in Keywords.main_keywords:
            outfile.write(None, f"{line}\n")
        else:
            # This is a (potential) MSW keyword.
            logger.debug(keyword)

            well_name = _get_well_name(clean_lines_map, line_number)
            if keyword in Keywords.segments:  # check if it is an active well
                logger.debug(well_name)
                if well_name not in list(schedule.active_wells):
                    outfile.write(keyword, "")
                    line_number += 1
                    continue  # not an active well

            # first, collect data for this keyword into a 'chunk'
            chunk_str = ""
            raw = []  # only used for WELSPECS which we dont modify
            # concatenate and look for 'end of records' => //
            while not re.search(r"/\s*/$", chunk_str):
                line_number += 1
                raw.append(lines[line_number])
                if line_number in clean_lines_map:
                    chunk_str += clean_lines_map[line_number]
            chunk = _format_chunk(chunk_str)
            chunks.append((keyword, chunk))  # for debug ...

            # use data to update our schedule
            if keyword == Keywords.WELSPECS:
                schedule.set_welspecs(chunk)  # update with new data
                outfile.write(keyword, raw, chunk=False)  # but write it back 'untouched'
                line_number += 1  # ready for next line
                continue

            elif keyword == Keywords.COMPDAT:
                remains = schedule.handle_compdat(chunk)  # update with new data
                if remains:
                    # Add single quotes to non-active well names
                    for remain in remains:
                        remain[0] = "'" + remain[0] + "'"
                    outfile.write(keyword, remains, end_of_record=True)  # write any 'none-active' wells here
                line_number += 1  # ready for next line
                continue

            elif keyword == Keywords.WELSEGS:
                schedule.set_welsegs(chunk)  # update with new data

            elif keyword == Keywords.COMPSEGS:
                # this is COMPSEGS'. will now update and write out new data
                schedule.set_compsegs(chunk)

                try:
                    case.check_input(well_name, schedule)
                except NameError as err:
                    # This might mean that `Keywords.segments` has changed to
                    # not include `Keywords.COMPSEGS`
                    raise SystemError(
                        "Well name not defined, even though it should be defined when "
                        f"token ({keyword} is one of "
                        f"{', '.join(Keywords.segments)})"
                    ) from err

                if well_name not in written:
                    write_welsegs = True  # will only write WELSEGS once
                    written.add(well_name)
                else:
                    write_welsegs = False
                figno += 1
                logger.debug("Writing new MSW info for well %s", well_name)
                wells.update(well_name, schedule)
                output = CreateOutput(
                    case,
                    schedule,
                    wells,
                    well_name,
                    schedule.get_well_number(well_name),
                    completor.__version__,
                    show_fig,
                    pdf_file,
                    write_welsegs,
                    paths,
                )
                outfile.write(None, output.finalprint)
            else:
                raise ValueError(f"The keyword '{keyword}' has not been implemented in Completor, but should have been")

        line_number += 1  # ready for next line
        logger.debug(line_number)
    outfile.close()
    close_figure()
    if pdf_file is not None:
        pdf_file.close()

    try:
        return chunks, case, schedule, wells, output  # for debug ...
    except NameError:
        if len(schedule.active_wells) == 0:
            return chunks, case, schedule, wells
        else:
            raise ValueError(
                "Inconsistent case and input schedule files. "
                "Check well names and WELSPECS, COMPDAT, WELSEGS and COMPSEGS."
            )


def main() -> None:
    """Generate a Completor output schedule file from the input given from user.

    Also set the correct loglevel based on user input. Defaults to WARNING if not set.

    Raises:
        CompletorError: If input schedule file is not defined as input or in case file.
    """
    parser = get_parser()
    inputs = parser.parse_args()

    if inputs.loglevel is not None:
        loglevel = inputs.loglevel
    else:
        loglevel = logging.WARNING
    # Loglevel NOTSET (0) gets overwritten by higher up loggers to WARNING, setting loglevel to 1 is a lazy workaround.
    loglevel = 1 if loglevel == 0 else loglevel

    logger.setLevel(loglevel)

    # Open the case file
    if inputs.inputfile is not None:
        with open(inputs.inputfile, encoding="utf-8") as file:
            case_file_content = file.read()
    else:
        raise CompletorError("Need input case file to run Completor")

    schedule_file_content, inputs.schedulefile = get_content_and_path(
        case_file_content, inputs.schedulefile, Keywords.SCHFILE
    )

    if isinstance(schedule_file_content, str):
        parse.read_schedule_keywords(clean_file_lines(schedule_file_content.splitlines()), Keywords.main_keywords)

    _, inputs.outputfile = get_content_and_path(case_file_content, inputs.outputfile, Keywords.OUTFILE)

    if inputs.outputfile is None:
        if inputs.schedulefile is None:
            raise ValueError("No schedule provided, or none where found " "in the case file (keyword 'SCHFILE')")
        inputs.outputfile = inputs.schedulefile.split(".")[0] + "_advanced.wells"

    paths_input_schedule = (inputs.inputfile, inputs.schedulefile)

    logger.debug("Running Completor %s. An advanced well modelling tool.", completor.__version__)
    logger.debug("-" * 60)
    start_a = time.time()

    handle_error_messages(create)(
        case_file_content, schedule_file_content, inputs.outputfile, inputs.figure, paths=paths_input_schedule
    )

    logger.debug("Total runtime: %d", (time.time() - start_a))
    logger.debug("-" * 60)


def _get_well_name(schedule_lines: dict[int, str], i: int) -> str:
    """Get the well name from line number

    Args:
        schedule_lines: Dictionary of lines in schedule file.
        i: Line index.

    Returns:
        Well name.
    """
    keys = np.array(sorted(list(schedule_lines.keys())))
    j = np.where(keys == i)[0][0]
    next_line = schedule_lines[int(keys[j + 1])]
    return next_line.split()[0]


def _format_chunk(chunk_str: str) -> list[list[str]]:
    """Format the data-records and resolve the repeat-mechanism.

    E.g. 3* == 1* 1* 1*, 3*250 == 250 250 250.

    Args:
        chunk_str: A chunk data-record.

    Returns:
        Expanded values.
    """
    chunk = re.split(r"\s+/", chunk_str)[:-1]
    expanded_data = []
    for line in chunk:
        new_record = ""
        for record in line.split():
            if not record[0].isdigit():
                new_record += record + " "
                continue
            if "*" not in record:
                new_record += record + " "
                continue

            # need to handle things like 3* or 3*250
            multiplier, number = record.split("*")
            new_record += f"{number if number else '1*'} " * int(multiplier)
        if new_record:
            expanded_data.append(new_record.split())
    return expanded_data


if __name__ == "__main__":
    try:
        main()
    except CompletorError as e:
        raise abort(str(e)) from e
