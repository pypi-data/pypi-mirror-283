# Copyright (c) 2024 iiPython

# Modules
import json
import signal
from pathlib import Path
from threading import Thread, Event

from watchfiles import watch
from socketify import App, WebSocket, OpCode, CompressOptions

from nova.internal import NovaBuilder

# Main attachment
def attach_hot_reloading(
    app: App,
    builder: NovaBuilder
) -> None:
    async def connect_ws(ws: WebSocket) -> None: 
        ws.subscribe("reload")

    stop_event = Event()
    signal.signal(signal.SIGINT, lambda s, f: stop_event.set())

    def hot_reload_thread(app: App) -> None:
        located_spa = [x for x in builder.plugins if type(x).__name__ == "SPAPlugin"]
        spa_module = located_spa[0] if located_spa else None

        for changes in watch(builder.source, stop_event = stop_event):
            builder.wrapped_build(include_hot_reload = True)

            # Path handling
            def convert_path(path: Path) -> Path:
                if spa_module is not None:
                    relative_spa_dest = spa_module.source.relative_to(builder.destination)
                    if path.is_relative_to(relative_spa_dest):
                        path = path.relative_to(relative_spa_dest)

                return path

            # Calculate the relative paths and send off
            paths = []
            for change in changes:
                relative = Path(change[1]).relative_to(builder.source)
                need_reload = []

                # Check if this change is part of a file dependency (ie. css or js)
                if relative.suffix in builder.file_assocs:
                    check_path = builder.file_assocs[relative.suffix](relative)
                    for path, dependencies in builder.build_dependencies.items():
                        if check_path in dependencies:
                            need_reload.append(path)

                else:
                    def recurse(search_path: str, need_reload: list = []) -> list:
                        for path, dependencies in builder.build_dependencies.items():
                            if search_path in dependencies:
                                need_reload.append(convert_path(path))
                                recurse(str(path), need_reload)

                        return need_reload

                    need_reload = recurse(str(relative))

                if relative.suffix in [".jinja2", ".jinja", ".j2"] and relative not in need_reload:
                    need_reload += [convert_path(relative)]

                for page in need_reload:
                    clean = page.with_suffix("")
                    paths.append(f"/{str(clean.parent) + '/' if str(clean.parent) != '.' else ''}{clean.name if clean.name != 'index' else ''}")

            app.publish("reload", json.dumps({"reload": paths}), OpCode.TEXT)

    Thread(target = hot_reload_thread, args = [app]).start()
    app.ws(
        "/_nova",
        {
            "compression": CompressOptions.SHARED_COMPRESSOR,
            "max_payload_length": 16 * 1024 * 1024,
            "open": connect_ws
        }
    )
