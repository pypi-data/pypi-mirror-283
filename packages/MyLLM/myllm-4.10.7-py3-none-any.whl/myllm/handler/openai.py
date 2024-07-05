"""
🔗 OpenAI and LocalAI Support

via https://github.com/openai/openai-python
via https://localai.io

"""

from time import sleep

from loguru import logger
from openai import OpenAI

from .client import AIClient


class OpenaiHandler(AIClient):
    """
    MyLLM class for OpenAI and LocalAI

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """
        try:
            super().__init__(**kwargs)
            if self.enabled:
                self.client = OpenAI(
                    api_key=self.llm_provider_key, base_url=self.llm_base_url
                )
            else:
                return None
        except Exception as error:
            logger.error("OpenAI initialization error {}", error)
            return None

    async def chat(self, prompt):
        """
        Asynchronously chats with the client based on the given prompt.

        :param prompt: The prompt for the chat.
        :return: The response from the chat.
        """
        try:
            self.conversation.add_message("user", prompt)
            archived_messages = self.conversation.get_messages()
            # logger.debug("archived_messages {}", archived_messages)

            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=archived_messages,
                stream=self.stream_mode,
            )
            sleep(self.timeout)
            # logger.debug("response {}", response)

            if self.stream_mode:
                # TODO fix this
                logger.debug("stream_mode not supported yet")
                # for chunk in response:
                #     response_content = chunk.choices[0].delta.content
                #     logger.debug("response_content {}", response_content)
                #     self.conversation.add_message("assistant", response_content)

            else:
                response_content = response.choices[0].message.content
                # logger.debug("response_content {}", response_content)
                self.conversation.add_message("assistant", response_content)
            formatted_response = f"{self.llm_prefix} {response_content}"
            # logger.debug("User: {}, AI: {}", prompt, response_content)
            return formatted_response
        except Exception as error:
            logger.error("No response {}", error)
