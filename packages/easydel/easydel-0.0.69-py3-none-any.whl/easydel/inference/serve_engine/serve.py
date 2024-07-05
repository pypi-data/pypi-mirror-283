import asyncio
from asyncio import wait_for, TimeoutError

try:
    import websockets  # type: ignore
except ModuleNotFoundError:
    websockets = None

try:
    import gradio as gr  # type: ignore
except ModuleNotFoundError:
    gr = None


import json
import time
from easydel.etils.etils import get_logger
from easydel.inference.generation_pipeline.pipeline import ChatPipeline
from aiohttp import web


class ApiEngine:

    def __init__(
        self,
        pipeline: ChatPipeline,
        hostname: str = "0.0.0.0",
        port: int = 11550,
    ):
        if websockets is None:
            raise ModuleNotFoundError(
                "you are trying to use ApiEngine and you don't have `websockets` installed (run `pip install websocket websockets`)"
            )
        self._logger = get_logger(__name__)
        self.pipeline = pipeline
        self.hostname: str = hostname
        self.port: int = port

    @property
    def logger(self):
        return self._logger

    @property
    def _address(self):
        return self.hostname + ":" + str(self.port)

    @property
    def _https_address(self):
        return "https://" + self._address

    @property
    def _http_address(self):
        return "http://" + self._address

    @property
    def _ws_address(self):
        return "ws://" + self.hostname + ":" + str(self.port + 1)

    def _jsn(self, dictionary):
        return json.dumps(dictionary)

    async def _conversation_http_get(self, request):
        try:
            conversation = request.query.get("conversation")
            if conversation is None:
                return web.json_response(
                    {
                        "error": "Invalid request: 'conversation' query parameter is required."
                    },
                    status=400,
                )
            start_time = time.time()
            full_response = ""

            for idx, response in enumerate(
                self.pipeline.stream_generate(json.loads(conversation))
            ):
                sequence = self.tokenizer.decode(response)
                full_response += sequence

            elapsed_time = time.time() - start_time
            tokens_per_second = (idx + 1) / elapsed_time if elapsed_time > 0 else 0

            self.logger.info(
                f"HTTP GET generation completed. Time: {elapsed_time}, Tokens/second: {tokens_per_second}, Generated Tokens: {idx + 1}"
            )

            return web.json_response(
                {
                    "response": full_response,
                    "progress": {
                        "tokens_generated": idx + 1,
                        "char_generated": len(full_response),
                        "elapsed_time": elapsed_time,
                        "tokens_per_second": tokens_per_second,
                    },
                }
            )

        except json.JSONDecodeError:
            return web.json_response(
                {"error": "Invalid request: JSON decoding failed."}, status=400
            )

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return web.json_response(
                {"error": f"An error occurred: {str(e)}"}, status=500
            )

    async def _conversation_socketcall(
        self,
        websocket: "websockets.WebSocketServerProtocol",  # type:ignore
    ):
        user_request = json.loads(await wait_for(websocket.recv(), timeout=10))
        conversation = user_request.get("conversation", None)
        if conversation is None:
            await websocket.send(
                self._jsn(
                    {"error": "Invalid request: 'conversation' field is required."}
                )
            )
            return
        # Start tracking time for token generation performance
        start_time = time.time()
        # Initialize sent length
        sent_length = 0
        for idx, sequence in enumerate(
            self.pipeline.stream_generate(conversation=conversation)
        ):
            elapsed_time = time.time() - start_time
            tokens_per_second = (idx + 1) / elapsed_time if elapsed_time > 0 else 0
            sent_length += len(sequence)
            await websocket.send(
                self._jsn(
                    {
                        "response": sequence,
                        "progress": {
                            "step": idx + 1,
                            "tokens_generated": idx + 1,
                            "char_generated": sent_length,
                            "elapsed_time": elapsed_time,
                            "tokens_per_second": tokens_per_second,
                        },
                        "done": False,
                    }
                )
            )

        await websocket.send(self._jsn({"done": True}))
        self.logger.info(
            f"generation completed Time: {elapsed_time}, Tokens/second: {tokens_per_second}, Generated Tokens:{idx + 1}"
        )

    def _request_gradio_components(self) -> None:
        with gr.Blocks(
            title="EasyDeL-API",
            analytics_enabled=False,
            theme=gr.Theme(
                primary_hue=gr.themes.Color(
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                    "#AE5630",
                ),
                neutral_hue=gr.themes.Color(
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                    "#292929",
                ),
            ).set(
                body_background_fill="#191919",
                body_background_fill_dark="#191919",
                block_background_fill="#292929",
                block_background_fill_dark="#292929",
                block_label_background_fill="#292929",
                block_label_background_fill_dark="#292929",
                border_color_primary="#191919",
                border_color_primary_dark="#191919",
                background_fill_primary="#292929",
                background_fill_primary_dark="#292929",
                background_fill_secondary="#26201e",
                background_fill_secondary_dark="#26201e",
                color_accent_soft="#393939",
                color_accent_soft_dark="#393939",
                block_label_text_color="#FFFFFF",
                block_label_text_color_dark="#FFFFFF",
                body_text_color="#FFFFFF",
                body_text_color_dark="#FFFFFF",
                body_text_color_subdued="#FFFFFF",
                body_text_color_subdued_dark="#FFFFFF",
                button_secondary_text_color="#FFFFFF",
                button_secondary_text_color_dark="#FFFFFF",
                button_primary_text_color="#FFFFFF",
                button_primary_text_color_dark="#FFFFFF",
                input_placeholder_color="#FFFFFF",
                input_placeholder_color_dark="#FFFFFF",
                block_title_text_color="#FFFFFF",
                block_title_text_color_dark="#FFFFFF",
            ),
            css="#rtl-textbox{text-align: right;}",
        ) as block:
            conversation = gr.Json(label="Conversation")
            response = gr.Textbox(
                container=False,
                placeholder="Response",
                scale=4,
                elem_id="rtl-textbox",
            )
            sequence_stream = gr.Textbox(
                container=False,
                placeholder="Sequence Stream",
                scale=4,
                elem_id="rtl-textbox",
            )
            token_count = gr.Number(label="Tokens Generated")
            elapsed_time = gr.Number(label="Elapsed Time (s)")
            tokens_per_second = gr.Number(label="Tokens per Second")
            submit = gr.Button(value="Submit", variant="primary", scale=1)
            inputs = [conversation]
            outputs = [
                response,
                sequence_stream,
                token_count,
                elapsed_time,
                tokens_per_second,
            ]

            def generate_request(conversation):
                start_time = time.time()
                full_sequence = ""
                for idx, sequence in enumerate(
                    self.pipeline.stream_generate(conversation=conversation)
                ):
                    full_sequence += sequence

                    elapsed_time = time.time() - start_time
                    tokens_per_second = (
                        (idx + 1) / elapsed_time if elapsed_time > 0 else 0
                    )

                    yield (
                        full_sequence,
                        sequence,
                        idx + 1,
                        round(elapsed_time, 4),
                        round(tokens_per_second, 4),
                    )

                self.logger.info(
                    f"[gradio] generation completed Time: {elapsed_time}, Tokens/second: {tokens_per_second}, Generated Tokens:{idx + 1}"
                )

            submit.click(
                fn=generate_request,
                inputs=inputs,
                outputs=outputs,
            )
        return block

    async def _chose_path(
        self,
        websocket: "websockets.WebSocketServerProtocol",  # type:ignore
        path: str,
    ):
        try:
            if path == "/conversation":
                self.logger.info(
                    f"conversation request from {websocket.remote_address}"
                )
                await self._conversation_socketcall(websocket=websocket)
            elif path == "/":
                await websocket.send(
                    self._jsn(
                        {
                            "status": 200,
                            "msg": "Server is running",
                        }
                    )
                )
            else:
                await websocket.send(
                    self._jsn(
                        {
                            "status": 404,
                            "error": f"Invalid path {path}",
                        }
                    )
                )
        except json.JSONDecodeError:
            await websocket.send(
                self._jsn(
                    {
                        "error": "Invalid request: JSON decoding failed.",
                    }
                )
            )
            self.logger.error("JSON decoding failed.")

        except websockets.ConnectionClosed:
            self.logger.info("Connection Is Closed.")

        except TimeoutError:
            await websocket.send(
                self._jsn(
                    {"error": "Request timed out."},
                )
            )
            self.logger.error("Request timed out.")

        except Exception as e:
            await websocket.send(
                self._jsn(
                    {
                        "error": f"An error occurred: {str(e)}",
                    },
                )
            )
            self.logger.error(
                f"An error occurred: {str(e)}",
            )

    def fire(self):
        async def _run():
            # HTTP Application
            app = web.Application()
            app.router.add_get("/conversation", self._conversation_http_get)

            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, self.hostname, self.port)

            # WebSocket server
            ws_server = websockets.serve(
                self._chose_path,
                self.hostname,
                self.port + 1,
            )

            # Gradio interface
            if gr is not None:
                gradio_app = self._request_gradio_components()
                gradio_server = gradio_app.launch(
                    server_name=self.hostname,
                    server_port=self.port + 2,
                    share=False,
                    prevent_thread_lock=True,
                    quiet=True
                )
            else:
                self.logger.error(
                    "Gradio Server wont be launched, gradio not found! (run `pip install gradio`)."
                )

            # Start all servers
            await asyncio.gather(
                site.start(),
                ws_server,
            )

            self.logger.info(f"HTTP server started on {self._http_address}")
            self.logger.info(f"WebSocket server started on {self._ws_address}")

            if gr is not None:
                self.logger.info(
                    f"Gradio server started on http://{self.hostname}:{self.port + 2}"
                )

            # Keep the servers running
            try:
                await asyncio.Future()
            finally:
                await runner.cleanup()
                await gradio_server.close()

        asyncio.run(_run())
