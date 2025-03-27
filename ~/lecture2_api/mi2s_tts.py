# !/usr/bin/env python
# _*_coding:utf-8_*_

# 給任何使用這支程式的人：這支程式是國台語和客語合成的API的client端。
# 具體上會發送最下方變數 text, language, model 給伺服器，並接收一個回傳的wav檔，output.wav

import socket
import struct
import argparse


class TTSClient:
    def __init__(self):
        self.__host = "140.116.245.157"
        self.__token = "mi2stts"

    def askForService(self, text: str):
        """
        Ask TTS server.
        Params:
            text    :(str) Text to be synthesized.
        """
        if not len(text):
            raise ValueError("Length of text must be bigger than zero")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.__host, self.__port))
            msg = bytes(
                self.__token
                + "@@@"
                + text
                + "@@@"
                + self.__model
                + "@@@"
                + self.__language,
                "utf-8",
            )
            msg = struct.pack(">I", len(msg)) + msg
            sock.sendall(msg)

            with open("output.wav", "wb") as f:
                while True:
                    l = sock.recv(8192)
                    if not l:
                        break
                    f.write(l)
            print("File received complete")

        except Exception as e:
            print(e)

        finally:
            sock.close()

    def set_language(self, language: str, model: str):
        """
        Params:
            language    :(str) chinese or taiwanese or hakka.
            model       :(str) HTS synthesis model name.
        """
        self.__language = language.lower()

        if self.__language == "hakka":
            self.__port = 10010
            self.__model = "hedusi"

        elif self.__language == "taiwanese":
            self.__port = 10012
            if model:
                self.__model = model
            else:
                self.__model = "M12"

        elif self.__language == "chinese":
            self.__port = 10015
            self.__model = "M60"

        else:
            raise ValueError("'language' param must be chinese or taiwanese or hakka.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str,
        default="taiwanese",
        help="Language to be synthesized, chinese or taiwanese or hakka.",
    )
    parser.add_argument(
        "--model", type=str, default="M04", help="HTS synthesis model name."
    )
    parser.add_argument(
        "--text", type=str, default="晚上散步", help="Text to be synthesized."
    )

    args = parser.parse_args()
    tts_client = TTSClient()
    tts_client.set_language(language=args.language, model=args.model)
    tts_client.askForService(args.text)
