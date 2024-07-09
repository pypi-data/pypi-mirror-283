import paho.mqtt.client as mqtt
import argparse
import os
import logging
import json
import atexit
import sys
import time

from pathlib import Path
from datetime import datetime

import PySimpleGUI as sg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure

class CryoGUI:
    def __init__(self, cfg, logger):
        self._cfg = cfg
        self._logger = logger

        self._temp_pt1000_pcb = 0
        self._temp_pt1000_pcb_c = 0
        self._status_n2valve = False

        self._lastnotify = 0
        self._runactive = False

    def run(self):
        self._mqtt = MQTTPublisher(
            self._logger,
            self._cfg["broker"]["broker"],
            self._cfg["broker"]["port"],
            self._cfg["broker"]["user"],
            self._cfg["broker"]["password"],
            self._cfg["broker"]["basetopic"],
            [
                { 'topic' : 'cryo/temperature/pt1000pcb', 'handler' : [ self._receive_pt1000pcb ] },
                { 'topic' : 'cryo/valve/n2valve', 'handler' : [ self._receive_n2valveupdate ] },
                { 'topic' : 'scan/+/start', 'handler' : [ self._receive_scan_start ] },
                { 'topic' : 'scan/+/done', 'handler' : [ self._receive_scan_done ] }
            ]
        )

        layout = [
            [
                sg.TabGroup([[
                    sg.Tab('Current status', [
                        [
                            sg.Column([
                                [ sg.Text("Current temperature (K):") ],
                                [ sg.Text("Current temperature (C):") ]
                            ], scrollable = False),
                            sg.Column([
                                [ sg.Text("XXXX.XX", key="txtTemp_K") ],
                                [ sg.Text("XXXX.XX", key="txtTemp_C") ]
                            ], scrollable = False)
                        ]
                    ]),
                    sg.Tab('Regulation', [

                    ])
                ]]),
            ],
            [
                sg.Column([
                    [ sg.Text("Status:") ],
                    [ sg.Text("N2 valve status:") ],
                ]),
                sg.Column([
                    [ sg.Text("Unknown", key="txtStatus") ],
                    [ sg.Text("Unknown    ", key="txtStatusN2Valve") ]
                ]),
                sg.Column([
                    [ sg.Button("Open N2 valve", key="btnN2ValveOpen") ],
                    [ sg.Button("Close N2 valve", key="btnN2ValveClose") ]
                ]),
                sg.Column([
                    [ sg.Button("Exit", key="btnExit") ]
                ])
            ]
        ]

        self._window = sg.Window("QUASEM cryogenic status GUI", layout=layout, finalize=True)


        while True:
            event, value = self._window.read(timeout = 1)
            if event in ('btnExit', None):
                break
            if event == 'btnN2ValveOpen':
                self._mqtt.publish_event('cryo/valve/n2valve', { 'request' : True })
            if event == 'btnN2ValveClose':
                self._mqtt.publish_event('cryo/valve/n2valve', { 'request' : False })
            # Check if we got one of the signals and should update ...

            self._window['txtTemp_K'].Update(f"{self._temp_pt1000_pcb:.2f} K")
            self._window['txtTemp_C'].Update(f"{self._temp_pt1000_pcb_c:.2f} C")
            if self._status_n2valve:
                self._window['txtStatusN2Valve'].Update("opened")
            else:
                self._window['txtStatusN2Valve'].Update("closed")

            if not self._runactive:
                if self._lastnotify > (time.time() - 5):
                    self._window["txtStatus"].Update("Online                ")
                else:
                    self._window["txtStatus"].Update("Unknown               ")
            else:
                if self._lastnotify > (time.time() - 5*60):
                    self._window["txtStatus"].Update("Measuring, slow update")
 
    def _receive_scan_start(self, topic, msg):
        self._runactive = True

    def _receive_scan_done(self, topic, msg):
        self._runactive = False

    def _receive_pt1000pcb(self, topic, msg):
        self._lastnotify = time.time()
        self._temp_pt1000_pcb = msg['temperature']
        self._temp_pt1000_pcb_c = msg['temperature_C']
        pass

    def _receive_n2valveupdate(self, topic, msg):
        if "state" in msg:
            self._lastnotify = time.time()
            self._status_n2valve = msg["state"]


# =================

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        if isinstance(obj, datetime):
            return obj.__str__()
        if isinstance(obj, timedelta):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)

# ==================

class MQTTPatternMatcher:
    def __init__(self):
        self._handlers = []
        self._idcounter = 0

    def registerHandler(self, pattern, handler):
        self._idcounter = self._idcounter + 1
        self._handlers.append({ 'id' : self._idcounter, 'pattern' : pattern, 'handler' : handler })
        return self._idcounter

    def removeHandler(self, handlerId):
        newHandlerList = []
        for entry in self._handlers:
            if entry['id'] == handlerId:
                continue
            newHandlerList.append(entry)
        self._handlers = newHandlerList

    def _checkTopicMatch(self, filter, topic):
        filterparts = filter.split("/")
        topicparts = topic.split("/")

        # If last part of topic or filter is empty - drop ...
        if topicparts[-1] == "":
            del topicparts[-1]
        if filterparts[-1] == "":
            del filterparts[-1]

        # If filter is longer than topics we cannot have a match
        if len(filterparts) > len(topicparts):
            return False

        # Check all levels till we have a mistmatch or a multi level wildcard match,
        # continue scanning while we have a correct filter and no multi level match
        for i in range(len(filterparts)):
            if filterparts[i] == '+':
                continue
            if filterparts[i] == '#':
                return True
            if filterparts[i] != topicparts[i]:
                return False

        if len(topicparts) != len(filterparts):
            return False

        # Topic applies
        return True

    def callHandlers(self, topic, message, basetopic = "", stripBaseTopic = True):
        topic_stripped = topic
        if basetopic != "":
            if topic.startswith(basetopic) and stripBaseTopic:
                topic_stripped = topic[len(basetopic):]

        for regHandler in self._handlers:
            if self._checkTopicMatch(regHandler['pattern'], topic):
                if isinstance(regHandler['handler'], list):
                    for handler in regHandler['handler']:
                        handler(topic_stripped, message)
                elif callable(regHandler['handler']):
                    regHandler['handler'](topic_stripped, message)

class MQTTPublisher:
    def __init__(self, logger, broker, port, username, password, basetopic, topichandlers=None):
        self._logger = logger
        logger.debug('MQTT: Starting up')
            
        self._topicHandlers = topichandlers
            
        self._config = {
            'broker'    : broker,
            'port'      : port,
            'username'  : username,
            'password'  : password,
            'basetopic' : basetopic
        }

        logger.debug("MQTT: Configured broker {} : {} (user: {})".format(broker, port, username))

        self._shuttingDown = False

        self._mqtt = mqtt.Client(reconnect_on_failure=True)
        self._mqtt.on_connect = self._mqtt_on_connect
        self._mqtt.on_message = self._mqtt_on_message
        self._mqtt.on_disconnect = self._mqtt_on_disconnect

        if username:
            self._mqtt.username_pw_set(self._config['username'], self._config['password'])
        try:
            self._mqtt.connect(self._config['broker'], self._config['port'])
        except:
            logger.error("Failed to connect to MQTT broker ...")
            self._mqtt = None
            return

        atexit.register(self._shutdown)

        # Start asynchronous loop ...
        self._mqtt.loop_start()

    def _mqtt_on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._logger.debug("MQTT: Connected to broker".format(rc))
#            self.publish_event("mqtt/connect")
        else:
            self._logger.error("MQTT: Failed to connect to broker ({})".format(rc))

        # Here one could also subscribe to various topics ...
        # We use the self._topicHandlers to create our MQTT matcher and
        # then subscribe to the topics requested. These can then be used
        # to react to MQTT messages from the outside
        self._mqttHandler = MQTTPatternMatcher()
        if self._topicHandlers is not None:
            for handler in self._topicHandlers:
                self._mqttHandler.registerHandler(f"{self._config['basetopic'] + handler['topic']}", handler['handler'])
                client.subscribe(self._config['basetopic'] + handler['topic'])
                self._logger.debug(f"Subscribing to {self._config['basetopic'] + handler['topic']}")

    def _mqtt_on_message(self, client, userdata, msg):
        self._logger.debug("MQTT: Received message on {}".format(msg.topic))

        # First try to decode object (if it's JSON)
        try:
            msg.payload = json.loads(str(msg.payload.decode('utf-8', 'ignore')))
        except json.JSONDecodeError:
            pass

        # One could handle messages here (or raise event handlers, etc.) ...
        if self._mqttHandler is not None:
            self._mqttHandler.callHandlers(msg.topic, msg.payload, self._config['basetopic'])

    def _mqtt_on_disconnect(self, client, userdata, rc=0):
        self._logger.error("MQTT: Disconnected ({})".format(rc))
        if self._shuttingDown:
            client.loop_stop()

    def _shutdown(self):
        if self._mqtt:
            try:
                self._shuttingDown = True
                self._mqtt.disconnect()
            except:
                pass
        self._mqtt = None

    def _publish_raw(self, topic, message=None, prependBasetopic=True):
        if self._mqtt:
            if isinstance(message, dict):
                message = json.dumps(message, cls=NumpyArrayEncoder)

            realtopic = self._config['basetopic']+topic

            try:
                if not (message is None):
                    self._mqtt.publish(realtopic, payload=message, qos=0, retain=False)
                else:
                    self._mqtt.publish(realtopic, qos=0, retain=False)

                self._logger.debug("MQTT: Published to {}".format(realtopic))
            except Exception as e:
                self._logger.error("MQTT: Publish failed ({})".format(e))

    def publish_event(self, eventtype, payload=None):
        self._publish_raw(eventtype, payload)


class ModalDialogError:
    def __init__(self):
        pass

    def show(self, title, message):
        layout = [
                [ sg.Text(message) ],
                [ sg.Button("Ok", key="btnOk") ]
            ]
        window = sg.Window(title, layout, finalize=True)
        window.TKroot.transient()
        window.TKroot.grab_set()
        window.TKroot.focus_force()

        while True:
            event, values = window.read()
            if event in ('btnOk', None):
                window.close()
                return None

class WindowConnect:
    def __init__(self, cfg):
        self._cfg = cfg

    def showWindow(self):
        cfg = self._cfg
        layout = [
                [
                    sg.Column([
                        [ sg.Text("MQTT broker:") ],
                        [ sg.Text("MQTT port:") ],
                        [ sg.Text("MQTT user:") ],
                        [ sg.Text("MQTT password:") ],
                        [ sg.Text("Base topic:") ]
                    ]),
                    sg.Column([
                        [ sg.InputText(cfg['broker']['broker'], key="txtBroker") ],
                        [ sg.InputText(cfg['broker']['port'], key="txtPort") ],
                        [ sg.InputText(cfg['broker']['user'], key="txtUser") ],
                        [ sg.InputText(cfg['broker']['password'], key="txtPassword") ],
                        [ sg.InputText(cfg['broker']['basetopic'], key="txtBrokerBasetopic") ]
                    ])
                ],
                [
                    sg.Button("Connect", key="btnConnect"),
                    sg.Button("Exit", key="btnAbort")
                ]
            ]
        window = sg.Window("QUASEM cryogenic infrastructure GUI", layout, finalize=True)

        while True:
            event, values = window.read(timeout = 10)
            if event in ('btnAbort', None):
                return None
            if event == 'btnConnect':
                try:
                    cfg['broker']['port'] = int(values['txtPort'])
                    if (cfg['broker']['port'] < 1) or (cfg['broker']['port'] > 65535):
                        raise ValueError("Invalid port")
                except:
                    ModalDialogError().show("Invalid broker power", "The supplied broker port is invalid")
                cfg['broker']['broker'] = values['txtBroker']
                cfg['broker']['user'] = values['txtUser']
                cfg['broker']['password'] = values['txtPassword']
                cfg['broker']['basetopic'] = values['txtBrokerBasetopic']

                window.close()
                return cfg




def parseArguments():
    ap = argparse.ArgumentParser(description = "QUASEM cryo infrastructure GUI")
    ap.add_argument("--cfg", type=str, required=False, default=None, help="Configuration file to use. Defaults to ~/.config/quasemcryogui.cfg")
    ap.add_argument("--loglevel", type=str, required=False, default="error", help="Loglevel to use (supports debug, info, warning, error and critical; default error")

    args = ap.parse_args()

    loglvls = {
        "DEBUG" : logging.DEBUG,
        "INFO" : logging.INFO,
        "WARNING" : logging.WARNING,
        "ERROR" : logging.ERROR,
        "CRITICAL" : logging.CRITICAL
    }
    if not args.loglevel.upper() in loglvls:
        print(f"Unknown log level {args.loglevel}")
        sys.exit(1)

    logger = logging.getLogger()
    logger.setLevel(loglvls[args.loglevel.upper()])

    return args, logger

def recursiveApplyDictUpdate(original, additional):
    for k in original:
        if k in additional:
            if not isinstance(original[k], dict):
                original[k] = additional[k]
            else:
                # Recurse
                original[k] = recursiveApplyDictUpdate(original[k], additional[k])
    return original

def main():
    args, logger = parseArguments()

    # Load configuration is present
    cfgfile = args.cfg

    cfgsInFile = {}
    if cfgfile is None:
        cfgfile = os.path.join(Path.home(), ".config/quasemcryogui.cfg")
    try:
        with open(cfgfile) as cfgFile:
            cfgsInFile = json.load(cfgFile)
    except Exception as e:
        cfgsInFile = {}
        print("Failed to read configuration file")
        print(e)

    # Build our default configuration form cfgfile and defaults
    cfg = {
        "broker" : {
            "broker" : "",
            "port" : 1883,
            "user" : "",
            "password" : "",
            "basetopic" : ""
        }
    }

    cfg = recursiveApplyDictUpdate(cfg, cfgsInFile)
    connWindow = WindowConnect(cfg)
    cfg = connWindow.showWindow()
    if cfg is None:
        # User has aborted ...
        sys.exit(0)

    if cfg["broker"]["basetopic"][-1] != '/':
        cfg["broker"]["basetopic"] = cfg["broker"]["basetopic"] + "/"

    mainWindow = CryoGUI(cfg, logger)
    mainWindow.run()

if __name__ == "__main__":
    main()
