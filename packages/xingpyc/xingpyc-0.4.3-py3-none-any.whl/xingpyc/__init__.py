from multiprocessing import Process
import asyncio
import os
from websockets.sync.client import connect
from websockets.server import serve
from websocket import WebSocket

import time
import numpy as np
from threading import Thread
from io import BytesIO
import PIL.Image as Image
import uuid
import socket
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

def image_to_png_bytestring(image):
    png_bytestring = BytesIO()
    image.save(png_bytestring, format="PNG")
    png_bytestring.seek(0)
    return png_bytestring.getvalue()

def image_to_webp_bytestring(image,quality=80):
    webp_bytestring = BytesIO()
    image.save(webp_bytestring, format="WEBP", quality=quality)
    webp_bytestring.seek(0)
    return webp_bytestring.getvalue()

def write_progress(task_name, progress):
    with open(f"progress/{task_name}", "w") as f:
        f.write(progress)


def get_device_id_env():
    if os.path.exists(".device_id"):
        device_id = open(".device_id", "r").read()
    else:
        print("Device ID not found, generating new one")
        device_id = str(uuid.uuid4())
        open(".device_id", "w").write(device_id)
    return device_id[0:10]

def get_local_ip():
    try:
        # Create a dummy socket and connect to a remote server to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use a common public server (like Google DNS) to establish a connection
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Unable to get local IP: {e}"

# Redirect sys.stdout to the custom stream
class XClient:
    pc = RTCPeerConnection()
    def __init__(self, async_funcs,sync_funcs, mode: str, ip=None, portOrInfo=None):
        """
        init a ComClient with AI functions
        funcs: a list of AI functions
        """
        self.cloudClient = None
        self.incomingMsg = []
        self.clients = {}
        self.blockbuffers = {}
        # Initialize device ID from environment variable
        self.device_id = get_device_id_env()
        self.ip = ip
        self.portOrInfo = portOrInfo
        self.need_reconnect_cloud = False
        # tasks folder is for placing incoming commands
        if not os.path.exists("tasks"):
            os.mkdir("tasks")
        tasks = os.listdir("tasks")
        for task in tasks:
            os.remove(f"tasks/{task}")
        # results folder is for placing results from various AI functions, no matter binded to XClient or not
        if not os.path.exists("results"):
            os.mkdir("results")
        results = os.listdir("results")
        for result in results:
            os.remove(f"results/{result}")
        if not os.path.exists("progress"):
            os.mkdir("progress")
        progresses = os.listdir("progress")
        for p in progresses:
            os.remove(f"progress/{p}")
        # message loop
        asyncio.get_event_loop().create_task(self.message_loop())

        # listening
        if mode == "server":
            print(
                "\033[93m Server started on " + ip + ":" + str(portOrInfo) + " \033[0m"
            )
            asyncio.get_event_loop().run_until_complete(
                serve(self.asServer_listening, ip, portOrInfo)
            )
        elif mode == "client":
            # for client mode, connect to the cloud server, use sync websocket, async one is not working well for now
            self.need_reconnect_cloud = True

        # for functions registered with XClient, create a process for each processor that will automatically listen according to there function name
        # e.g. if there is a function named "i2i" in the list, a process will be created to listen for "i2i" header tasks in the tasks folder
        for func in async_funcs:
            Process(target=add_listener, args=(func,)).start()

        self.sync_funcs = {func.__name__: func for func in sync_funcs}
            
        asyncio.get_event_loop().run_forever()

    def cloud_connect(self): 
        try:
            print("\033[93m connecting to server \033[0m")
            self.cloudClient = WebSocket()
            self.cloudClient.connect(self.ip)
            self.cloudClient.send_bytes(
                ("login     " + self.device_id + self.portOrInfo).encode("utf-8")
            )
            login_res = self.cloudClient.recv()
            if login_res == b"login success":
                print(
                    "\033[95m===========         Login Success         ============\033[0m"
                )
            Thread(target=self.asClient_listening, args=()).start()
            return True
        except Exception as e:
            print(f"Error in connecting to cloud: {e}")
            return False

    async def message_loop(self, blocksize=100000):
        """
        the looping function for sending and receiving messages
        """
        print("=== message loop started ===")
        print("=== message loop started ===")
        print("=== message loop started ===")
        loopCount = 0
        while True:
            loopCount += 1
            if self.need_reconnect_cloud:
                if self.cloud_connect():
                    self.need_reconnect_cloud = False
                time.sleep(1)
                continue
                
            if loopCount % 300 == 0 and self.cloudClient is not None:
                self.cloudClient.send_bytes("check     0000000000")
                print("check to cloud")

            ### here starts the incoming message processing
            ### here starts the incoming message processing
            ### here starts the incoming message processing
            inputMsg = []
            outputs=[]
            while len(self.incomingMsg) != 0:
                inputMsg.append(self.incomingMsg.pop())
            for client_id, message in inputMsg:

                if type(message) == str:
                    message = message.encode("utf-8")#just in case, happens sometimes

                print(
                    "\033[93mheader:"
                    + message[:10].replace(b" ", b"").decode()
                    + "   id:"
                    + message[10:20].decode()
                    + "   length:"
                    + str(len(message[20:]))
                    + "\033[0m"
                )
                # connect client and save client id
                header = message[:10].replace(b" ", b"").decode()
                task_id = message[10:20]
                if client_id not in self.blockbuffers:
                    self.blockbuffers[client_id] = []
                content = message[20:]
                try:
                    if header == "check":
                        print("connect check received")
                    elif header == "block":
                        # if block, save it to buffer
                        self.blockbuffers[client_id].append(content)
                        print(len(self.blockbuffers[client_id]), "blocks received")
                    else:
                        if client_id in self.blockbuffers:
                            # if there is a block buffer, concat it
                            self.blockbuffers[client_id].append(content)
                            content = b"".join(self.blockbuffers[client_id])
                        # finally write the file to tasks folder for processing from other processes
                        if header in self.sync_funcs:#if it is a sync function
                            func = self.sync_funcs[header]
                            #if async, use await
                            if asyncio.iscoroutinefunction(func):
                                res = await func(content)
                            else:
                                res = func(content)
                            assert type(res) == bytes, "Return type must be bytes"
                            file_str = f"{client_id}.{task_id.decode()}.{header}"
                            outputs.append([file_str, res])
                        else:#if it is not a sync function
                            with open(
                                f"tasks/{client_id}.{task_id.decode()}.{header}", "wb"
                            ) as f:
                                print(
                                    "place task: "
                                    + f"{client_id}.{task_id.decode()}.{header}"
                                )
                                f.write(content)
                        del self.blockbuffers[client_id]  # clean buffer
                except Exception as e:
                    print(f"Error in websocket communication: {e}")
                    continue
            
            ### here starts the progress reporting
            ### here starts the progress reporting
            ### here starts the progress reporting
            if len(os.listdir("progress")) > 0:
                for task_id in os.listdir("progress"):
                    try:
                        progress_content = open(f"progress/{task_id}", "r").read()
                        if len(task_id) != 10:
                            raise "invalid task id length!!"
                        task_id_byte = task_id.encode("utf-8")
                        progress_content = progress_content.encode("utf-8")

                        if client_id == -1:#cloud
                            print("start sending progress to cloud")
                            self.cloudClient.send_bytes(b"progress  " + task_id_byte + progress_content)
                            print("sent progress to cloud")
                        else:#client
                            await websocket.send(b"progress  " + task_id_byte + progress_content)
                        os.remove(f"progress/{task_id}")
                    except Exception as e:
                        print(f"Error in sending message to websocket: {e}")

            ### here starts the result sending
            ### here starts the result sending
            ### here starts the result sending
            if len(os.listdir("results")) > 0:
                for file in os.listdir("results"):
                    try:
                        with open(f"results/{file}", "rb") as f:
                            result_data = f.read()
                            outputs.append([file,result_data])
                        os.remove(f"results/{file}")
                    except Exception as e:
                        print(f"Error in reading result file: {e}")
            
            for file, result_data in outputs:
                try:
                    content = result_data
                    client_id, task_id, header = file.split(".")
                    client_id = int(client_id)
                    header = (header + " " * (10 - len(header))).encode("utf-8")
                    if isinstance(task_id, str):
                        task_id = task_id.encode("utf-8")
                    if isinstance(header, str):
                        header = header.encode("utf-8")
                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    if client_id == -1:
                        print("start sending to cloud")
                        count = 0
                        totalblocks = len(content) // blocksize
                        while len(content) > blocksize:
                            Thread(
                                target=self.cloudClient.send_bytes,
                                args=(
                                    b"block     " + task_id + content[0:blocksize],
                                ),
                            ).start()
                            time.sleep(0.01)
                            content = content[blocksize:]
                            print(f"sent block {count}/{totalblocks}")
                            count += 1
                        self.cloudClient.send_bytes(header + task_id + content)
                        print("sent to cloud")
                    else:
                        websocket = self.clients.get(client_id)
                        while len(content) > 0:
                            if len(content) > blocksize:
                                await websocket.send(
                                    b"block     " + task_id + content[0:blocksize]
                                )
                                content = content[blocksize:]
                            else:
                                await websocket.send(header + task_id + content)
                                content = b""
                            await asyncio.sleep(0.01)
                        await asyncio.sleep(0.01)
                    break  # only send one result at a time
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")
            else:
                await asyncio.sleep(0.01)


    def asClient_listening(self):
        try:
            while True:
                message = self.cloudClient.recv()
                ###### -1 should be client id, change it later
                self.incomingMsg.append((-1, message))
        except Exception as e:
            self.need_reconnect_cloud = True
            print("Connection closed by the server")

    async def asServer_listening(self, websocket):
        client_id = id(websocket)
        print(f"Client {client_id} connected")
        try:
            async for message in websocket:
                self.clients[client_id] = websocket
                self.incomingMsg.append((client_id, message))
        except Exception as e:
            print(f"Error in websocket communication: {e}")


def add_listener(callback, interval=0.1):
    while True:
        taskfiles = os.listdir("tasks")
        time.sleep(interval)
        found = False
        try:
            for file in taskfiles:
                client_id, task_id, header = file.split(".")
                if header == callback.__name__:
                    found = True
                    res = callback("tasks/" + file)
                    assert type(res) == bytes, "Return type must be bytes"
                    if res is not None:
                        with open("results/" + file, "wb") as f:
                            f.write(res)
                    os.remove("tasks/" + file)
        except Exception as e:
            print(f"Error in interpreting task of {callback.__name__}: {e}")


def i2i(imgFile):
    # an example i2i for testing
    print("i2i task received, doing image flipping")
    img = Image.open(imgFile)
    #img = Image.open(BytesIO(imgFile))
    nparray = np.array(img)
    # do something that fake the AI function
    nparray = np.flip(nparray, axis=1)
    img = Image.fromarray(nparray)

    webp_buffer = image_to_webp_bytestring(img)

    return webp_buffer


def stream(_):
    import mss
    sct = mss.mss()
    # an example i2i for testing
    _time = time.time()
    screenshot = sct.grab({"top": 60, "left": 0, "width": 1920//1.3, "height": 1080//1.3})

    # Convert the raw screenshot data to a NumPy array
    img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
    print("capture time:", time.time()-_time)
    bytes = BytesIO()
    img.save(bytes, format='JPEG', quality=90)
    # webp_buffer = image_to_png_bytestring(img)
    print("streaming time:", time.time()-_time)
    return bytes.getvalue()


def config(msgFilePath):
    # for testing
    print("config task received, file:", msgFilePath)
    return b"hello from com test, config received" #some random response

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "1"
import mss
import json
sct = mss.mss()

async def rtc(jsonByte):
    # global pc
    # pc = RTCPeerConnection()
    sdpstr = jsonByte.decode("utf-8")
    offer_sdp = RTCSessionDescription(sdp=sdpstr, type="offer")
    XClient.pc = RTCPeerConnection()
    await XClient.pc.setRemoteDescription(offer_sdp)
    answer = await XClient.pc.createAnswer()
    await XClient.pc.setLocalDescription(answer)
    res = XClient.pc.localDescription
    resJson = json.dumps({"sdp":res.sdp,"type":res.type})
    @XClient.pc.on('datachannel')
    def on_datachannel(channel):
        print("\033[93m","Data channel created:", channel,"\033[0m")

        @channel.on("message")
        def on_message(message):
            print("Received message:", message)
            # Handle received message
            # Send a response
            if message == "test":
                channel.send("test response")
                return
            # an example i2i for testing
            _time = time.time()
            screenshot = sct.grab({"top": 60, "left": 0, "width": 1920, "height": 1080})

            # Convert the raw screenshot data to a NumPy array
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
            print("capture time:", time.time()-_time)
            
            bytesio = BytesIO()
            img.save(bytesio, format='JPEG', quality=90)
            # webp_buffer = image_to_png_bytestring(img)
            print("streaming time:", time.time()-_time)
            channel.send(bytesio.getvalue())
        
        @channel.on("close")
        def on_close():
            print("\033[93m","Data channel closed","\033[0m")
            #XClient.pc = RTCPeerConnection()#reset the peer connection

    return resJson.encode("utf-8")

async def ice(data):
    try:
        # Decode the incoming data
        jsonStr = data.decode("utf-8")
        dict = json.loads(jsonStr)
        ip = dict["ip"]
        protocol = dict["protocol"]
        component = dict["component"]
        foundation = dict["foundation"]
        port = dict["port"]
        priority = dict["priority"]
        candidate_type = dict["type"]
        sdp_mid = dict["sdpMid"]
        sdp_mline_index = dict["sdpMLineIndex"]

        # if len(ip) >20 or protocol!="udp":#ipv6
        #     print("\033[92m", "=========skip ipv6===========", ip, "\033[0m")
        #     return b"skip ipv6"
        

        # Create an ICE candidate object
        ice_candidate = RTCIceCandidate(
            component=component,
            foundation=foundation,
            ip=ip,
            port=port,
            priority=priority,
            protocol=protocol,
            type=candidate_type,
            sdpMid=sdp_mid,
            sdpMLineIndex=sdp_mline_index
        )
        
        # Add the ICE candidate to the peer connection
        await XClient.pc.addIceCandidate(ice_candidate)
        print("\033[92m", "Added ICE candidate:", ice_candidate, "\033[0m")
        return b"done"

    except Exception as e:
        print("\033[91m", "Error adding ICE candidate:", str(e), "\033[0m")
        return b"error"

if __name__ == "__main__":
    TESTING_CLOUD = True
    if TESTING_CLOUD:
        XClient([config,i2i],[rtc,ice], "client", "wss://www.xing.art/com/", "alpha.alpha")
    else:
        XClient([config,i2i],[stream], "server", get_local_ip(), "8088") #for local
