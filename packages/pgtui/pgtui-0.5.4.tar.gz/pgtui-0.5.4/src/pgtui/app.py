from textual.app import App

from pgtui import __version__
from pgtui.completer import QueryCompleter
from pgtui.db import fetch_db_info
from pgtui.entities import DbContext
from pgtui.messages import ShowException
from pgtui.screens.loading import LoadingScreen
from pgtui.screens.query import QueryScreen
from pgtui.widgets.dialog import MessageDialog


class PgTuiApp(App[None]):
    TITLE = "pgtui"
    SUB_TITLE = __version__
    CSS_PATH = "app.css"

    def __init__(
        self,
        ctx: DbContext,
        completer: QueryCompleter,
        file_path: str | None,
    ):
        super().__init__()
        self.ctx = ctx
        self.completer = completer
        self.file_path = file_path

    async def on_mount(self):
        await self.push_screen(LoadingScreen())
        db_info = await fetch_db_info(self.ctx)

        await self.switch_screen(  # type: ignore
            QueryScreen(
                self.ctx,
                db_info,
                self.completer,
                self.file_path,
            )
        )

    def on_show_exception(self, message: ShowException):
        body = str(message.exception)
        self.push_screen(MessageDialog("Error", body, error=True))
