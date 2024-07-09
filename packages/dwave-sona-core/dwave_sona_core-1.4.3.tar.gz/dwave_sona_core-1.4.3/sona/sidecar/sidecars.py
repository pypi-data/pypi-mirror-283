import asyncio
import datetime
import time
from asyncio.log import logger
from pathlib import Path

from sona.core.messages import Context, File, Job, Result, State
from sona.core.storages import StorageBase
from sona.settings import settings
from sona.web.webrtc.sessions import MediaInferencerSessionState
from sona.worker.producers import ProducerBase

SHARED_PATH = settings.SONA_STREAM_SIDECAR_SHARED_PATH
SUPERVISOR_TOPICS = settings.SONA_STREAM_SIDECAR_SUPERVISOR_TOPICS


class Scanner:
    def __init__(self, producer: ProducerBase, storage: StorageBase):
        self.today = datetime.date.today().strftime("%Y%m%d")
        self.producer = producer
        self.storage = storage

    async def scan_files(self):
        while True:
            state_dir = Path(SHARED_PATH)
            with open(state_dir / "__metadata", "r") as f:
                system_setup_time = int(f.read())

            for file in Path(SHARED_PATH).glob("*.json"):
                with open(file, "r") as f:
                    state = MediaInferencerSessionState.model_validate_json(f.read())
                    if state.is_expired():
                        await self.on_expired(file, state)
                    elif state.is_stop():
                        await self.on_stop(file, state)
                    elif state.is_failed(system_setup_time):
                        await self.on_failed(file, state)
                    else:
                        await self.on_running(file, state)

            await asyncio.sleep(1)

    async def on_expired(self, file: Path, state: MediaInferencerSessionState):
        logger.info(f"Session expired: {state}")
        Path(state.media_path).unlink(missing_ok=True)
        file.unlink(missing_ok=True)

    async def on_running(self, file: Path, state: MediaInferencerSessionState):
        logger.info(f"Session running: {state}")

        # Avoid pass `None` value from gateway
        application = state.options.get("application", "common") or "common"
        ctx = Context(
            id=state.track_id,
            application=application,
            supervisors=SUPERVISOR_TOPICS,
            jobs=[Job(name="stream", params=state.options)],
            states=[
                State(
                    job_name="stream",
                    timestamp=state.create_time,
                    exec_time=time.time_ns() - state.create_time,
                )
            ],
        )
        for topic in ctx.supervisors:
            self.producer.emit(topic, ctx.to_message())

    async def on_stop(self, file: Path, state: MediaInferencerSessionState):
        logger.info(f"Session stop: {state}")

        # Avoid pass `None` value from gateway
        application = state.options.get("application", "common") or "common"
        raw_file = File(label="raw", path=state.media_path)
        ctx = Context(
            id=state.track_id,
            application=application,
            supervisors=SUPERVISOR_TOPICS,
            jobs=[Job(name="stream", params=state.options)],
            results={"stream": Result(files=[raw_file])},
            states=[
                State(
                    job_name="stream",
                    timestamp=state.create_time,
                    exec_time=state.update_time - state.create_time,
                )
            ],
        )
        self.storage.push(ctx, raw_file)
        for topic in ctx.supervisors:
            self.producer.emit(topic, ctx.to_message())

        Path(state.media_path).unlink(missing_ok=True)
        file.unlink(missing_ok=True)

    async def on_failed(self, file: Path, state: MediaInferencerSessionState):
        logger.info(f"Session failed: {state}")

        # Avoid pass `None` value from gateway
        application = state.options.get("application", "common") or "common"
        ctx = Context(
            id=state.track_id,
            application=application,
            supervisors=SUPERVISOR_TOPICS,
            jobs=[Job(name="stream", params=state.options)],
            states=[
                State(
                    job_name="stream",
                    timestamp=state.create_time,
                    exec_time=state.update_time - state.create_time,
                    exception={
                        "message": "Service has been restarted with unknown error",
                        "traceback": "",
                    },
                )
            ],
        )
        for topic in ctx.supervisors:
            self.producer.emit(topic, ctx.to_message())

        Path(state.media_path).unlink(missing_ok=True)
        file.unlink(missing_ok=True)
