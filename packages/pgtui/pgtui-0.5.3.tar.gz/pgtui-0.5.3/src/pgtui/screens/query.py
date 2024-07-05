import logging
from asyncio import Lock
from datetime import datetime
from typing import Iterable

from psycopg import Error
from psycopg.rows import TupleRow
from rich.text import Text
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Header, TextArea

from pgtui.completer import QueryCompleter
from pgtui.db import execute
from pgtui.entities import DbContext, DbInfo, Result
from pgtui.messages import RunQuery, ShowException
from pgtui.utils.datetime import format_duration
from pgtui.widgets.editor import SqlEditor
from pgtui.widgets.footer import DbFooter
from pgtui.widgets.results import ResultsTable
from pgtui.widgets.status_bar import StatusBar

logger = logging.getLogger(__name__)

MAX_ROWS = 200
"""
Max rows to fetch at once to avoid loading a very large table into DataTable
accidentally.

TODO: make configurable
"""


class QueryScreen(Screen[None]):
    CSS = """
    SqlEditor {
        height: 50%;
    }

    ResultsTable {
        height: 50%;
        border: solid black;
        &:focus {
            border: tall $accent;
        }
    }
    """

    BINDINGS = [
        Binding("f10", "quit", "Exit pgtui"),
    ]

    def __init__(
        self,
        ctx: DbContext,
        db_info: DbInfo,
        completer: QueryCompleter,
        file_path: str | None,
    ):
        super().__init__()
        self.ctx = ctx
        self.db_info = db_info
        self.completer = completer
        self.exec_lock = Lock()
        self.file_path = file_path

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(SqlEditor(self.completer, self.file_path), ResultsTable())
        yield StatusBar()
        yield DbFooter(self.db_info)

    def on_mount(self):
        self.query_one(TextArea).focus()

    async def on_run_query(self, message: RunQuery):
        self.run_query(message.query)

    @work
    async def run_query(self, query: str):
        self.show_status("Running query...")

        if self.exec_lock.locked():
            return

        try:
            async with self.exec_lock:
                result = await self._execute(query)
                self.show_result_table(result)
                self.show_result_status(result)
        except Error as ex:
            logger.info(f"Query failed: {ex}")
            self.show_status("")
            self.post_message(ShowException(ex))

    async def _execute(self, query: str) -> Result:
        start = datetime.now()
        async with execute(self.ctx, query) as cursor:
            columns = cursor.description
            total_count = cursor.rowcount

            if cursor.rowcount > 0:
                logger.info(f"Fetching {MAX_ROWS}/{cursor.rowcount} rows")
                rows = await cursor.fetchmany(MAX_ROWS)
                duration = datetime.now() - start
                logger.info(f"Fetched {len(rows)} rows in {duration} seconds")
                return Result(rows, columns, total_count, len(rows), duration)
            else:
                duration = datetime.now() - start
                return Result([], columns, total_count, 0, duration)

    def show_result_table(self, result: Result):
        column_names = (c.name for c in result.columns) if result.columns else None
        rows = mark_nulls(result.rows)

        with self.app.batch_update():
            self.query(ResultsTable).remove()
            table = ResultsTable(rows, column_names)
            self.mount(table, after=self.query_one(SqlEditor))

    def show_result_status(self, result: Result):
        duration = format_duration(result.duration)
        message = f"Fetched {result.fetched_rows} / {result.total_rows} rows in {duration}"
        self.query_one(StatusBar).set_message(message)

    def show_status(self, message: str):
        self.query_one(StatusBar).set_message(message)

    def action_quit(self):
        self.app.exit()


NULL = Text("<null>", "dim")


def mark_nulls(rows: Iterable[TupleRow]) -> Iterable[TupleRow]:
    """Replaces nulls in db data with a styled <null> marker."""
    return (tuple(cell if cell is not None else NULL for cell in row) for row in rows)
